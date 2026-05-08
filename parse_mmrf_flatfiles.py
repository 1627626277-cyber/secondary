#!/usr/bin/env python3
"""
MMRF CoMMpass FlatFile Parser
==============================
Parses MMRF Researcher Gateway flatfiles into structured clinical tables.
Supports IA15, IA19, IA20 data releases.

Usage:
    python parse_mmrf_flatfiles.py --input /path/to/CoMMpass_IA19_FlatFiles --output ./parsed_output

MMRF FlatFiles expected in input directory:
    - MMRF_CoMMpass_IA{XX}_PER_PATIENT.csv
    - MMRF_CoMMpass_IA{XX}_PER_PATIENT_VISIT.csv
    - MMRF_CoMMpass_IA{XX}_STAND_ALONE_TRTRESP.csv
    - MMRF_OS_PFS_ASCT.csv
    - MMRF_OS_PFS_non-ASCT.csv
"""

import argparse
import os
import sys
import warnings
import numpy as np
import pandas as pd
warnings.filterwarnings("ignore")

PER_PATIENT_COLS = {
    "PUBLIC_ID": "patient_id", "D_PT_age": "age_at_diagnosis",
    "D_PT_gender": "sex", "D_PT_race": "race", "D_PT_ethnicity": "ethnicity",
    "R_ISS": "r_iss_stage", "D_PT_iss": "iss_stage",
    "D_PT_lstalive": "last_alive_day", "D_PT_lastdy": "last_follow_up_day",
    "D_PT_deathdy": "death_day", "ecog": "ecog_ps", "line1sct": "first_line_asct",
}

LAB_COLS = {
    "PUBLIC_ID": "patient_id", "VISIT": "visit_number", "VISITDY": "visit_day",
    "D_LAB_chem_albumin": "albumin_g_dl", "D_LAB_chem_calcium": "calcium_mg_dl",
    "D_LAB_chem_creatinine": "creatinine_mg_dl",
    "D_LAB_serum_beta2_microglobulin": "beta2_mg_mg_l",
    "D_LAB_serum_ldh": "ldh_u_l", "D_LAB_cbc_hemoglobin": "hemoglobin_g_dl",
    "D_LAB_cbc_wbc": "wbc_per_ul", "D_LAB_serum_igg": "igg_mg_dl",
    "D_LAB_serum_iga": "iga_mg_dl", "D_LAB_serum_igm": "igm_mg_dl",
    "D_LAB_serum_kappa": "kappa_mg_l", "D_LAB_serum_lambda": "lambda_mg_l",
    "D_LAB_serum_m_protein": "m_protein_g_dl",
    "AT_RESPONSEASSES": "response_assessment_day",
    "AT_TREATMENTRESP": "treatment_response",
}

TRTRESP_COLS = {
    "public_id": "patient_id", "line": "treatment_line",
    "trtshnm": "regimen_short_name", "trtclass": "regimen_class",
    "trtstdy": "treatment_start_day", "trtendy": "treatment_end_day",
    "bestresp": "best_response", "bmtx_day": "asct_day", "bmtx_rec": "asct_recorded",
}

class MMRFParser:
    def __init__(self, input_dir, ia_version="IA19"):
        self.input_dir = input_dir
        self.ia_version = ia_version.upper()
        self.flatfile_dir = os.path.join(input_dir, f"CoMMpass_{self.ia_version}_FlatFiles")

    def load_files(self):
        print(f"Loading MMRF {self.ia_version} flatfiles from: {self.flatfile_dir}")
        per_patient_path = os.path.join(self.flatfile_dir, f"MMRF_CoMMpass_{self.ia_version}_PER_PATIENT.csv")
        per_patient_visit_path = os.path.join(self.flatfile_dir, f"MMRF_CoMMpass_{self.ia_version}_PER_PATIENT_VISIT.csv")
        trtresp_path = os.path.join(self.flatfile_dir, f"MMRF_CoMMpass_{self.ia_version}_STAND_ALONE_TRTRESP.csv")
        os_pfs_asct_path = os.path.join(self.input_dir, "MMRF_OS_PFS_ASCT.csv")
        os_pfs_nonasct_path = os.path.join(self.input_dir, "MMRF_OS_PFS_non-ASCT.csv")

        self.df_per_patient = pd.read_csv(per_patient_path, encoding="latin-1") if os.path.exists(per_patient_path) else None
        self.df_visit = pd.read_csv(per_patient_visit_path, encoding="latin-1") if os.path.exists(per_patient_visit_path) else None
        self.df_trtresp = pd.read_csv(trtresp_path, encoding="latin-1") if os.path.exists(trtresp_path) else None
        self.df_os_pfs_asct = pd.read_csv(os_pfs_asct_path, encoding="latin-1") if os.path.exists(os_pfs_asct_path) else None
        self.df_os_pfs_nonasct = pd.read_csv(os_pfs_nonasct_path, encoding="latin-1") if os.path.exists(os_pfs_nonasct_path) else None

        loaded = sum([self.df_per_patient is not None, self.df_visit is not None, self.df_trtresp is not None, self.df_os_pfs_asct is not None, self.df_os_pfs_nonasct is not None])
        print(f"  Loaded {loaded}/5 files")
        return loaded

    def extract_clinical_data(self):
        print("\n[1/6] Extracting baseline clinical data...")
        if self.df_per_patient is None:
            return None
        cols_available = {k: v for k, v in PER_PATIENT_COLS.items() if k in self.df_per_patient.columns}
        df = self.df_per_patient[list(cols_available.keys())].copy()
        df.rename(columns=cols_available, inplace=True)
        if "sex" in df.columns:
            df["sex"] = df["sex"].map({"M": "Male", "F": "Female", "Male": "Male", "Female": "Female"})
        if "death_day" in df.columns and "last_follow_up_day" in df.columns:
            df["os_days"] = df["death_day"].fillna(df["last_follow_up_day"])
            df["os_event"] = df["death_day"].notna().astype(int)
            df["os_months"] = df["os_days"] / 30.44
        print(f"  Extracted {len(df)} patients with {len(df.columns)} fields")
        return df

    def extract_fish_cytogenetics(self):
        print("\n[2/6] Extracting FISH cytogenetics...")
        if self.df_per_patient is None:
            return None
        fish_patterns = {
            "del17p": ["CYTO_del_17p13", "FISH_del_17p13", "del17p"],
            "t4_14": ["CYTO_t_4_14", "FISH_t_4_14", "t_4_14"],
            "t14_16": ["CYTO_t_14_16", "FISH_t_14_16", "t_14_16"],
            "gain1q": ["CYTO_gain_1q21", "FISH_gain_1q21", "gain1q"],
            "del13q": ["CYTO_del_13q14", "FISH_del_13q14", "del13q"],
        }
        available_cols = set(self.df_per_patient.columns)
        fish_data = {"patient_id": self.df_per_patient["PUBLIC_ID"]}
        for abn_name, search_cols in fish_patterns.items():
            found = next((col for col in search_cols if col in available_cols), None)
            fish_data[abn_name] = self.df_per_patient[found] if found else np.nan
        df_fish = pd.DataFrame(fish_data)
        hr_cols = [c for c in ["del17p", "t4_14", "t14_16"] if c in df_fish.columns]
        if hr_cols:
            df_fish["high_risk_cytogenetics"] = df_fish[hr_cols].apply(lambda row: 1 if any(row.astype(str).str.contains("YES|1|Positive", case=False, na=False)) else 0, axis=1)
        return df_fish

    def extract_labs(self):
        print("\n[3/6] Extracting longitudinal lab data...")
        if self.df_visit is None:
            return None, None
        cols_available = {k: v for k, v in LAB_COLS.items() if k in self.df_visit.columns}
        df = self.df_visit[list(cols_available.keys())].copy()
        df.rename(columns=cols_available, inplace=True)
        df_bl = df[df["visit_number"] == 0].copy()
        return df, df_bl

    def extract_treatment_response(self):
        print("\n[4/6] Extracting treatment/response data...")
        if self.df_trtresp is None:
            return None, None
        cols_available = {k: v for k, v in TRTRESP_COLS.items() if k in self.df_trtresp.columns}
        df = self.df_trtresp[list(cols_available.keys())].copy()
        df.rename(columns=cols_available, inplace=True)
        fl = df[df["treatment_line"] == 1].copy()
        fl_summary = fl.groupby("patient_id").agg({"regimen_short_name": "first", "regimen_class": "first", "best_response": "first", "treatment_start_day": "min", "treatment_end_day": "max"}).reset_index()
        return fl_summary, df.groupby("patient_id")["treatment_line"].nunique().reset_index()

    def extract_survival(self):
        print("\n[5/6] Extracting survival/PFS data...")
        pfs_records = []
        if self.df_os_pfs_nonasct is not None:
            df = self.df_os_pfs_nonasct.rename(columns={"Patient": "patient_id", "Progression": "progression", "Dead": "dead", "Progression Day": "pfs_days", "Last Alive/Dead": "last_follow_up_days"})
            df["asct_group"] = "non-ASCT"
            pfs_records.append(df[["patient_id", "pfs_days", "progression", "last_follow_up_days", "dead", "asct_group"]])
        if self.df_os_pfs_asct is not None:
            df = self.df_os_pfs_asct.rename(columns={"Patient": "patient_id", "Post-ASCT Progression Day": "pfs_days", "Post-ASCT Progression": "progression", "Dead": "dead", "Last Alive/Dead": "last_follow_up_days"})
            df["asct_group"] = "ASCT"
            pfs_records.append(df[["patient_id", "pfs_days", "progression", "last_follow_up_days", "dead", "asct_group"]])
        if pfs_records:
            df_pfs = pd.concat(pfs_records, ignore_index=True)
            df_pfs["pfs_event"] = df_pfs["progression"].map(lambda x: 1 if str(x).lower() == "yes" else 0)
            df_pfs["os_event"] = df_pfs["dead"].map(lambda x: 1 if str(x).lower() == "yes" else 0)
            df_pfs["pfs_months"] = df_pfs["pfs_days"] / 30.44
            return df_pfs
        return None

    def extract_sample_mapping(self):
        print("\n[6/6] Extracting sample/patient mapping...")
        if self.df_visit is None:
            return None
        df = self.df_visit[["PUBLIC_ID", "VISIT", "VISITDY"]].copy()
        df.columns = ["patient_id", "visit_number", "visit_day"]
        df["sample_id"] = df.apply(lambda r: f"SAMPLE_{r['patient_id']}_V{r['visit_number']}", axis=1)
        df["aliquot_id"] = df["sample_id"] + "_ALQ001"
        df["is_baseline"] = df["visit_number"] == 0
        return df

    def run_all(self, output_dir):
        os.makedirs(output_dir, exist_ok=True)
        if self.load_files() == 0:
            print("\nNo flatfiles found. Register at https://research.themmrf.org/ to download.")
            return

        outputs = {
            "patient_clinical_data.csv": self.extract_clinical_data(),
            "patient_fish_cytogenetics.csv": self.extract_fish_cytogenetics(),
            "patient_labs_longitudinal.csv": self.extract_labs()[0] if self.extract_labs()[0] is not None else None,
            "patient_labs_baseline.csv": self.extract_labs()[1] if self.extract_labs()[1] is not None else None,
            "patient_treatment_response.csv": self.extract_treatment_response()[0],
            "patient_survival_pfs.csv": self.extract_survival(),
            "sample_patient_mapping.csv": self.extract_sample_mapping(),
        }

        for fname, df in outputs.items():
            if df is not None:
                path = os.path.join(output_dir, fname)
                df.to_csv(path, index=False, encoding="utf-8")
                print(f"  Saved: {path} ({len(df)} rows)")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", "-i", required=True)
    parser.add_argument("--output", "-o", default="./mmrf_parsed")
    parser.add_argument("--ia-version", default="IA19")
    args = parser.parse_args()
    mmrf = MMRFParser(args.input, args.ia_version)
    mmrf.run_all(args.output)

if __name__ == "__main__":
    main()
