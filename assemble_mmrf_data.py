#!/usr/bin/env python3
"""
MMRF CoMMpass Data Assembly Script
====================================
Integrates data from multiple sources:
1. GDC API (open access) - clinical, RNA-seq, somatic mutations, copy number
2. Published literature - baseline characteristics, FISH frequencies, treatment response
3. AWS S3 (open access) - RNA-seq gene expression

Usage:
    pip install requests pandas numpy tqdm --break-system-packages
    python assemble_mmrf_data.py --output ./mmrf_output --synthetic-patients 500
"""

import argparse
import json
import os
import subprocess
import sys
import time
import tempfile
import warnings
from collections import OrderedDict

import numpy as np
import pandas as pd

warnings.filterwarnings("ignore")

# ============================================================
# SECTION 1: Published CoMMpass Baseline Characteristics
# Source: Skerget et al. 2024, Nature Genetics, n=1,143
# PMID: 39160255, PMCID: PMC11387199
# ============================================================

PUBLISHED_CLINICAL = {
    "cohort_size": 1143,
    "median_age": 63,
    "age_range": (27, 93),
    "male_pct": 60.4,
    "female_pct": 39.6,
    "iss_i_pct": 35.1,
    "iss_ii_pct": 35.1,
    "iss_iii_pct": 27.2,
    "iss_unknown_pct": 2.6,
    "median_os_months": 103.6,
    "median_os_iss3_months": 53.9,
    "hrd_pct": 57.2,   # hyperdiploid
    "nhrd_pct": 42.8,  # non-hyperdiploid
}

PUBLISHED_FISH = {
    "del17p13": {"n_tested": 871, "n_positive": 109, "pct": 12.5},
    "t4_14":    {"n_tested": 851, "n_positive": 109, "pct": 12.8},  # t(4;14) NSD2/WHSC1/MMSET
    "del13q14": {"n_tested": 871, "n_positive": 453, "pct": 52.0},
    "gain1q21": {"n_tested": 871, "n_positive": 307, "pct": 35.2},
    "del1p22":  {"n_tested": 871, "n_positive": 212, "pct": 24.3},
    "t14_16":   {"n_tested": 851, "n_positive": 31,  "pct": 3.6},  # from ASH 2024 abstract
    "t14_20":   {"n_tested": 851, "n_positive": 20,  "pct": 2.4},  # from ASH 2024 abstract
    "high_risk": {"n_tested": 832, "n_positive": 247, "pct": 29.7},  # >=1 HR feature
}

PUBLISHED_MUTATIONS = {
    "TP53":  {"pct": 7.9, "source": "ASH 2024, IA19"},
    "KRAS":  {"pct": 22.0, "source": "Walker BA et al. 2018"},
    "NRAS":  {"pct": 20.0, "source": "Walker BA et al. 2018"},
    "BRAF":  {"pct": 7.0, "source": "Walker BA et al. 2018"},
    "DIS3":  {"pct": 11.0, "source": "Walker BA et al. 2018"},
    "FAM46C": {"pct": 10.0, "source": "Walker BA et al. 2018"},
}

PUBLISHED_RESPONSE = {
    "first_line_cr_pct": 12.0,
    "first_line_vgpr_pct": 25.0,
    "first_line_pr_pct": 35.0,
    "first_line_sd_pct": 15.0,
    "first_line_pd_pct": 8.0,
    "first_line_unknown_pct": 5.0,
    "primary_refractory_pct": 58.0,
    "asct_rate_pct": 45.0,
}

PUBLISHED_TREATMENT = {
    "common_regimens": [
        ("VRd", 35.0),      # bortezomib + lenalidomide + dexamethasone
        ("Rd", 18.0),       # lenalidomide + dexamethasone
        ("VCd", 12.0),      # bortezomib + cyclophosphamide + dexamethasone
        ("Vd", 10.0),       # bortezomib + dexamethasone
        ("KRd", 8.0),       # carfilzomib + lenalidomide + dexamethasone
        ("DRd", 7.0),       # daratumumab + lenalidomide + dexamethasone
        ("other", 10.0),
    ],
    "drug_classes_used": {
        "proteasome_inhibitor": 90.0,
        "IMiD": 92.0,
        "alkylating_agent": 35.0,
        "anti_CD38": 25.0,
        "steroid": 98.0,
    }
}


# ============================================================
# SECTION 2: GDC API Data Downloader
# ============================================================

GDC_API = "https://api.gdc.cancer.gov"


class SimpleResponse:
    def __init__(self, text, status_code=200):
        self.text = text
        self.status_code = status_code

    def raise_for_status(self):
        if not (200 <= self.status_code < 300):
            raise RuntimeError(f"HTTP status {self.status_code}")


def gdc_request_with_curl(endpoint, method="GET", json_data=None, params=None):
    """Windows-safe GDC request fallback using curl.exe with --ssl-no-revoke."""
    url = f"{GDC_API}/{endpoint}"
    cmd = [
        "curl.exe",
        "-sS",
        "-L",
        "--ssl-no-revoke",
        "--connect-timeout",
        "30",
        "--max-time",
        "180",
    ]
    temp_path = None
    try:
        if method == "GET":
            cmd.extend(["-G", url])
            if params:
                for key, value in params.items():
                    cmd.extend(["--data-urlencode", f"{key}={value}"])
        else:
            with tempfile.NamedTemporaryFile("w", delete=False, encoding="utf-8", suffix=".json") as handle:
                json.dump(json_data or {}, handle)
                temp_path = handle.name
            cmd.extend(["-X", "POST", "-H", "Content-Type: application/json", "--data-binary", f"@{temp_path}", url])

        result = subprocess.run(cmd, capture_output=True, text=True, timeout=240)
        if result.returncode != 0:
            print(f"  curl fallback failed: {result.stderr.strip()}")
            return None
        if not result.stdout.strip():
            print("  curl fallback returned empty response")
            return None
        return SimpleResponse(result.stdout)
    finally:
        if temp_path and os.path.exists(temp_path):
            try:
                os.remove(temp_path)
            except OSError:
                pass


def gdc_request(endpoint, method="GET", json_data=None, params=None, retries=3):
    """Make a request to the GDC API with retries."""
    import requests
    url = f"{GDC_API}/{endpoint}"
    for attempt in range(retries):
        try:
            if method == "GET":
                resp = requests.get(url, params=params, timeout=30)
            else:
                resp = requests.post(url, json=json_data, params=params, timeout=60)
            resp.raise_for_status()
            return resp
        except Exception as e:
            if attempt == retries - 1:
                print(f"  GDC API request failed after {retries} attempts: {e}")
                print("  Trying curl.exe fallback...")
                return gdc_request_with_curl(endpoint, method=method, json_data=json_data, params=params)
            time.sleep(2 ** attempt)
    return None


def download_clinical_data(output_dir):
    """Download clinical data from GDC for MMRF-COMMPASS."""
    print("\n[1/5] Downloading clinical data from GDC...")
    clinical_fields = ",".join([
        "case_id",
        "submitter_id",
        "demographic.age_at_index",
        "demographic.days_to_death",
        "demographic.ethnicity",
        "demographic.gender",
        "demographic.race",
        "demographic.vital_status",
        "diagnoses.days_to_last_follow_up",
        "diagnoses.days_to_last_known_disease_status",
        "diagnoses.iss_stage",
        "diagnoses.last_known_disease_status",
        "diagnoses.primary_diagnosis",
        "diagnoses.progression_or_recurrence",
        "diagnoses.site_of_resection_or_biopsy",
        "diagnoses.tissue_or_organ_of_origin",
        "diagnoses.treatments.treatment_type",
        "diagnoses.treatments.treatment_or_therapy",
        "diagnoses.treatments.therapeutic_agents",
        "diagnoses.treatments.treatment_outcome",
        "diagnoses.treatments.days_to_treatment_start",
        "diagnoses.treatments.days_to_treatment_end",
    ])
    filters = {
        "filters": {
            "op": "in",
            "content": {
                "field": "project.project_id",
                "value": ["MMRF-COMMPASS"]
            }
        },
        "fields": clinical_fields,
        "format": "TSV",
        "size": 2000
    }
    resp = gdc_request("cases", method="POST", json_data=filters)
    if resp and resp.text.strip():
        path = os.path.join(output_dir, "mmrf_clinical_gdc.tsv")
        with open(path, "w", encoding="utf-8") as f:
            f.write(resp.text)
        print(f"  Saved: {path}")
    else:
        print("  GDC clinical endpoint unreachable - will use published data instead")

    biospec_filters = {
        "filters": {
            "op": "in",
            "content": {
                "field": "project.project_id",
                "value": ["MMRF-COMMPASS"]
            }
        },
        "fields": "case_id,samples.sample_id,samples.portions.analytes.aliquots",
        "format": "TSV",
        "size": 5000
    }
    biospec_resp = gdc_request("cases", method="POST", json_data=biospec_filters)
    if biospec_resp and biospec_resp.text.strip():
        path = os.path.join(output_dir, "mmrf_biospecimen_gdc.tsv")
        with open(path, "w", encoding="utf-8") as f:
            f.write(biospec_resp.text)
        print(f"  Saved: {path}")


def download_rnaseq_metadata(output_dir):
    """Download RNA-seq gene expression quantification file metadata."""
    print("\n[2/5] Downloading RNA-seq metadata from GDC...")
    filters = {
        "filters": {
            "op": "and",
            "content": [
                {"op": "in", "content": {"field": "cases.project.project_id", "value": ["MMRF-COMMPASS"]}},
                {"op": "in", "content": {"field": "files.data_category", "value": ["Transcriptome Profiling"]}},
                {"op": "in", "content": {"field": "files.data_type", "value": ["Gene Expression Quantification"]}},
                {"op": "in", "content": {"field": "files.experimental_strategy", "value": ["RNA-Seq"]}},
            ]
        },
        "fields": "file_id,file_name,cases.case_id,cases.submitter_id,data_type,data_category,file_size",
        "format": "TSV",
        "size": 5000
    }
    resp = gdc_request("files", method="POST", json_data=filters)
    if resp and resp.text.strip():
        path = os.path.join(output_dir, "mmrf_rnaseq_files_gdc.tsv")
        with open(path, "w", encoding="utf-8") as f:
            f.write(resp.text)
        print(f"  Saved: {path}")
    else:
        print("  GDC file endpoint unreachable")


def download_mutation_maf(output_dir):
    """Download somatic mutation MAF files list."""
    print("\n[3/5] Downloading somatic mutation metadata from GDC...")
    filters = {
        "filters": {
            "op": "and",
            "content": [
                {"op": "in", "content": {"field": "cases.project.project_id", "value": ["MMRF-COMMPASS"]}},
                {"op": "in", "content": {"field": "files.data_category", "value": ["Simple Nucleotide Variation"]}},
                {"op": "in", "content": {"field": "files.data_type", "value": ["Masked Somatic Mutation"]}},
            ]
        },
        "fields": "file_id,file_name,cases.submitter_id,file_size",
        "format": "TSV",
        "size": 5000
    }
    resp = gdc_request("files", method="POST", json_data=filters)
    if resp and resp.text.strip():
        path = os.path.join(output_dir, "mmrf_mutations_gdc.tsv")
        with open(path, "w", encoding="utf-8") as f:
            f.write(resp.text)
        print(f"  Saved: {path}")
    else:
        print("  GDC mutation endpoint unreachable")


def download_copy_number(output_dir):
    """Download copy number segment files list."""
    print("\n[4/5] Downloading copy number metadata from GDC...")
    filters = {
        "filters": {
            "op": "and",
            "content": [
                {"op": "in", "content": {"field": "cases.project.project_id", "value": ["MMRF-COMMPASS"]}},
                {"op": "in", "content": {"field": "files.data_category", "value": ["Copy Number Variation"]}},
            ]
        },
        "fields": "file_id,file_name,cases.submitter_id,file_size",
        "format": "TSV",
        "size": 5000
    }
    resp = gdc_request("files", method="POST", json_data=filters)
    if resp and resp.text.strip():
        path = os.path.join(output_dir, "mmrf_copynumber_gdc.tsv")
        with open(path, "w", encoding="utf-8") as f:
            f.write(resp.text)
        print(f"  Saved: {path}")
    else:
        print("  GDC copy number endpoint unreachable")


# ============================================================
# SECTION 3: Published Data Tables Generator
# ============================================================

def generate_published_clinical_table(output_dir):
    """Generate summary tables from published literature."""
    print("\n[5/5] Generating published clinical data tables...")

    demo_rows = [
        {"Characteristic": "Number of Patients", "Value": "1,143", "Source": "Skerget et al. 2024, Nat Genet"},
        {"Characteristic": "Median Age at Diagnosis (years)", "Value": "63 (range 27-93)", "Source": "Skerget et al. 2024, Nat Genet"},
        {"Characteristic": "Male", "Value": "690 (60.4%)", "Source": "Skerget et al. 2024, Nat Genet"},
        {"Characteristic": "Female", "Value": "453 (39.6%)", "Source": "Skerget et al. 2024, Nat Genet"},
        {"Characteristic": "ISS Stage I", "Value": "401 (35.1%)", "Source": "Skerget et al. 2024, Nat Genet"},
        {"Characteristic": "ISS Stage II", "Value": "401 (35.1%)", "Source": "Skerget et al. 2024, Nat Genet"},
        {"Characteristic": "ISS Stage III", "Value": "311 (27.2%)", "Source": "Skerget et al. 2024, Nat Genet"},
        {"Characteristic": "Median OS", "Value": "103.6 months", "Source": "Skerget et al. 2024, Nat Genet"},
        {"Characteristic": "Median OS (ISS III)", "Value": "53.9 months", "Source": "Skerget et al. 2024, Nat Genet"},
        {"Characteristic": "Albumin >=3.5 g/dL", "Value": "~65%", "Source": "PMC11078818 n=796"},
        {"Characteristic": "Beta2-Microglobulin <3.5 mg/L", "Value": "~37%", "Source": "PMC11078818 n=796"},
        {"Characteristic": "Beta2-Microglobulin >=5.5 mg/L", "Value": "~36%", "Source": "PMC11078818 n=796"},
        {"Characteristic": "LDH <=250 U/L", "Value": "~84%", "Source": "PMC11078818 n=796"},
        {"Characteristic": "LDH >250 U/L", "Value": "~16%", "Source": "PMC11078818 n=796"},
    ]
    df_demo = pd.DataFrame(demo_rows)
    path = os.path.join(output_dir, "published_baseline_demographics.csv")
    df_demo.to_csv(path, index=False, encoding="utf-8")
    print(f"  Saved: {path}")

    fish_rows = []
    for abn, data in PUBLISHED_FISH.items():
        fish_rows.append({
            "Abnormality": abn,
            "N_Tested": data["n_tested"],
            "N_Positive": data["n_positive"],
            "Frequency_pct": data["pct"],
            "Source": "Skerget et al. 2024, Nat Genet" if abn not in ("t14_16", "t14_20") else "ASH 2024 abstract (IA19)"
        })
    df_fish = pd.DataFrame(fish_rows)
    path = os.path.join(output_dir, "published_fish_cytogenetics.csv")
    df_fish.to_csv(path, index=False, encoding="utf-8")
    print(f"  Saved: {path}")

    mut_rows = []
    for gene, data in PUBLISHED_MUTATIONS.items():
        mut_rows.append({"Gene": gene, "Frequency_pct": data["pct"], "Source": data["source"]})
    df_mut = pd.DataFrame(mut_rows)
    path = os.path.join(output_dir, "published_mutation_frequencies.csv")
    df_mut.to_csv(path, index=False, encoding="utf-8")
    print(f"  Saved: {path}")

    resp_rows = [
        {"Response": "CR/sCR", "Frequency_pct": 12.0, "Source": "Approx. from CoMMpass reports"},
        {"Response": "VGPR", "Frequency_pct": 25.0, "Source": "Approx. from CoMMpass reports"},
        {"Response": "PR", "Frequency_pct": 35.0, "Source": "Approx. from CoMMpass reports"},
        {"Response": "SD", "Frequency_pct": 15.0, "Source": "Approx. from CoMMpass reports"},
        {"Response": "PD", "Frequency_pct": 8.0, "Source": "Approx. from CoMMpass reports"},
        {"Response": "Primary Refractory", "Frequency_pct": 58.0, "Source": "ASH 2024, IA19"},
        {"Response": "ASCT Received", "Frequency_pct": 45.0, "Source": "Approx. from CoMMpass reports"},
    ]
    df_resp = pd.DataFrame(resp_rows)
    path = os.path.join(output_dir, "published_treatment_response.csv")
    df_resp.to_csv(path, index=False, encoding="utf-8")
    print(f"  Saved: {path}")

    tx_rows = []
    for regimen, pct in PUBLISHED_TREATMENT["common_regimens"]:
        tx_rows.append({"Regimen": regimen, "Frequency_pct": pct, "Source": "Approx. from CoMMpass analysis"})
    df_tx = pd.DataFrame(tx_rows)
    path = os.path.join(output_dir, "published_treatment_regimens.csv")
    df_tx.to_csv(path, index=False, encoding="utf-8")
    print(f"  Saved: {path}")


# ============================================================
# SECTION 4: Synthetic Patient Data Generator (for prototyping)
# ============================================================

def generate_synthetic_patients(n_patients, output_dir, seed=42):
    """Generate synthetic patient-level data matching published CoMMpass distributions."""
    print(f"\n[+] Generating synthetic patient data (n={n_patients}) based on published distributions...")
    np.random.seed(seed)

    patients = []
    for i in range(1, n_patients + 1):
        patient_id = f"MMRF_{i:04d}"
        is_male = np.random.random() < PUBLISHED_CLINICAL["male_pct"] / 100
        age = int(np.clip(np.random.normal(PUBLISHED_CLINICAL["median_age"], 11), 27, 93))

        iss_roll = np.random.random() * 100
        if iss_roll < PUBLISHED_CLINICAL["iss_i_pct"]:
            iss = "I"
        elif iss_roll < PUBLISHED_CLINICAL["iss_i_pct"] + PUBLISHED_CLINICAL["iss_ii_pct"]:
            iss = "II"
        elif iss_roll < PUBLISHED_CLINICAL["iss_i_pct"] + PUBLISHED_CLINICAL["iss_ii_pct"] + PUBLISHED_CLINICAL["iss_iii_pct"]:
            iss = "III"
        else:
            iss = "Unknown"

        if iss == "I":
            r_iss = np.random.choice(["I", "II"], p=[0.7, 0.3])
        elif iss == "II":
            r_iss = np.random.choice(["I", "II", "III"], p=[0.2, 0.5, 0.3])
        else:
            r_iss = np.random.choice(["II", "III"], p=[0.4, 0.6])

        ldh = np.clip(np.random.lognormal(np.log(200), 0.3), 50, 1000)
        ldh_elevated = ldh > 250
        beta2_mg = np.clip(np.random.lognormal(np.log(4.0), 0.6), 0.5, 50)
        albumin = np.clip(np.random.normal(3.5, 0.5), 1.5, 5.5)

        del17p = 1 if np.random.random() < PUBLISHED_FISH["del17p13"]["pct"] / 100 else 0
        t4_14 = 1 if np.random.random() < PUBLISHED_FISH["t4_14"]["pct"] / 100 else 0
        t14_16 = 1 if np.random.random() < PUBLISHED_FISH["t14_16"]["pct"] / 100 else 0
        gain1q = 1 if np.random.random() < PUBLISHED_FISH["gain1q21"]["pct"] / 100 else 0
        del13q = 1 if np.random.random() < PUBLISHED_FISH["del13q14"]["pct"] / 100 else 0
        high_risk_cyto = 1 if (del17p or t4_14 or t14_16) else 0

        tp53_mut = 1 if np.random.random() < PUBLISHED_MUTATIONS["TP53"]["pct"] / 100 else 0
        kras_mut = 1 if np.random.random() < PUBLISHED_MUTATIONS["KRAS"]["pct"] / 100 else 0
        nras_mut = 1 if np.random.random() < PUBLISHED_MUTATIONS["NRAS"]["pct"] / 100 else 0
        braf_mut = 1 if np.random.random() < PUBLISHED_MUTATIONS["BRAF"]["pct"] / 100 else 0
        dis3_mut = 1 if np.random.random() < PUBLISHED_MUTATIONS["DIS3"]["pct"] / 100 else 0
        fam46c_mut = 1 if np.random.random() < PUBLISHED_MUTATIONS["FAM46C"]["pct"] / 100 else 0

        first_line_regimens = [r[0] for r in PUBLISHED_TREATMENT["common_regimens"]]
        first_line_probs = [r[1]/100 for r in PUBLISHED_TREATMENT["common_regimens"]]
        first_line_regimen = np.random.choice(first_line_regimens, p=first_line_probs)

        received_asct = 1 if np.random.random() < PUBLISHED_RESPONSE["asct_rate_pct"] / 100 else 0

        resp_roll = np.random.random() * 100
        if resp_roll < 12:
            best_response = "CR"
        elif resp_roll < 37:
            best_response = "VGPR"
        elif resp_roll < 72:
            best_response = "PR"
        elif resp_roll < 87:
            best_response = "SD"
        elif resp_roll < 95:
            best_response = "PD"
        else:
            best_response = "Unknown"

        refractory = 1 if np.random.random() < PUBLISHED_RESPONSE["primary_refractory_pct"] / 100 else 0
        os_months = np.clip(np.random.exponential(PUBLISHED_CLINICAL["median_os_months"] / np.log(2)), 0.5, 150)
        os_event = 1 if np.random.random() < 0.4 else 0
        pfs_months = np.clip(np.random.exponential(40 / np.log(2)), 0.5, 120)
        pfs_event = 1 if np.random.random() < 0.65 else 0

        patients.append({
            "patient_id": patient_id, "age": age,
            "sex": "Male" if is_male else "Female",
            "iss_stage": iss, "r_iss_stage": r_iss,
            "ldh_u_l": round(ldh, 1), "ldh_elevated": ldh_elevated,
            "beta2_microglobulin_mg_l": round(beta2_mg, 1),
            "albumin_g_dl": round(albumin, 1),
            "del17p": del17p, "t4_14": t4_14, "t14_16": t14_16,
            "gain1q21": gain1q, "del13q14": del13q,
            "high_risk_cytogenetics": high_risk_cyto,
            "tp53_mutation": tp53_mut, "kras_mutation": kras_mut,
            "nras_mutation": nras_mut, "braf_mutation": braf_mut,
            "dis3_mutation": dis3_mut, "fam46c_mutation": fam46c_mut,
            "first_line_regimen": first_line_regimen,
            "received_asct": received_asct,
            "best_response": best_response,
            "primary_refractory": refractory,
            "os_months": round(os_months, 1), "os_event": os_event,
            "pfs_months": round(pfs_months, 1), "pfs_event": pfs_event,
            "treatment_lines": int(np.random.choice([1, 2, 3, 4], p=[0.55, 0.22, 0.13, 0.10])),
        })

    df = pd.DataFrame(patients)

    sample_rows = []
    for _, row in df.iterrows():
        pid = row["patient_id"]
        sample_id = f"SAMPLE_{pid}"
        sample_rows.append({
            "patient_id": pid, "sample_id": sample_id,
            "aliquot_id": f"{sample_id}_ALQ001",
            "is_baseline": True, "visit_timepoint": "Baseline",
            "cd138_positive": np.random.choice([True, False], p=[0.90, 0.10]),
        })
    df_samples = pd.DataFrame(sample_rows)

    patient_path = os.path.join(output_dir, "synthetic_patient_data_prototype.csv")
    sample_path = os.path.join(output_dir, "synthetic_sample_mapping_prototype.csv")
    df.to_csv(patient_path, index=False, encoding="utf-8")
    df_samples.to_csv(sample_path, index=False, encoding="utf-8")
    print(f"  Saved: {patient_path}")
    print(f"  Saved: {sample_path}")
    print(f"\n  Synthetic data distribution check (n={n_patients}):")
    print(f"    Male: {df['sex'].eq('Male').mean()*100:.1f}% (expected ~{PUBLISHED_CLINICAL['male_pct']}%)")
    print(f"    Age median: {df['age'].median():.0f} (expected {PUBLISHED_CLINICAL['median_age']})")
    print(f"    ISS I: {df['iss_stage'].eq('I').mean()*100:.1f}% (expected ~{PUBLISHED_CLINICAL['iss_i_pct']}%)")
    print(f"    del17p: {df['del17p'].mean()*100:.1f}% (expected ~{PUBLISHED_FISH['del17p13']['pct']}%)")
    print(f"    High-risk cyto: {df['high_risk_cytogenetics'].mean()*100:.1f}% (expected ~{PUBLISHED_FISH['high_risk']['pct']}%)")
    return df


def main():
    parser = argparse.ArgumentParser(description="Assemble MMRF CoMMpass data from multiple sources")
    parser.add_argument("--output", "-o", default="./mmrf_output", help="Output directory")
    parser.add_argument("--synthetic-patients", type=int, default=500)
    parser.add_argument("--skip-gdc", action="store_true")
    parser.add_argument("--skip-synthetic", action="store_true")
    args = parser.parse_args()

    os.makedirs(args.output, exist_ok=True)
    print("=" * 70)
    print("MMRF CoMMpass Data Assembly")
    print("=" * 70)

    if not args.skip_gdc:
        download_clinical_data(args.output)
        download_rnaseq_metadata(args.output)
        download_mutation_maf(args.output)
        download_copy_number(args.output)

    generate_published_clinical_table(args.output)

    if not args.skip_synthetic:
        generate_synthetic_patients(args.synthetic_patients, args.output)

    print("\n" + "=" * 70)
    print("Complete! Next: register at https://research.themmrf.org/ for real patient data")
    print("Important: synthetic prototype outputs are for pipeline testing only, not manuscript results.")


if __name__ == "__main__":
    main()
