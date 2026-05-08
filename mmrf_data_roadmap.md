# MMRF CoMMpass 数据获取完整路线图

## 项目背景

MMRF CoMMpass (NCT01454297) 是一项国际前瞻性观察性研究，纳入 **1,143 名新诊断多发性骨髓瘤患者**，随访 ≥8 年。肿瘤样本在诊断时和进展时进行全基因组测序、全外显子组测序和RNA测序。

## 数据可用性总结

| 数据类别 | GDC (开放) | MMRF Researcher Gateway (免费注册) | dbGaP (机构IRB) | 已发表文献 |
|----------|-----------|----------------------------------|-----------------|-----------|
| 基础临床数据 (年龄/性别/ISS/LDH/β2-MG/albumin) | ✅ 部分 | ✅ 完整 | ✅ | ✅ |
| 生存数据 (OS) | ✅ | ✅ | ✅ | ✅ 汇总 |
| PFS | ❌ | ✅ | ✅ | ✅ 汇总 |
| 治疗反应 (CR/VGPR/PR/SD/PD) | ❌ | ✅ | ✅ | ✅ 汇总 |
| 治疗方案 (一线方案/药物/ASCT) | ✅ 部分 | ✅ 完整 | ✅ | ✅ 汇总 |
| FISH/细胞遗传学 (del17p/t(4;14)/t(14;16)/1q gain/del13q) | ❌ | ✅ | ✅ | ✅ 汇总 |
| Sample/Patient Mapping | ✅ | ✅ | ✅ | ✅ |
| 体细胞突变 (TP53/KRAS/NRAS/BRAF/DIS3/FAM46C) | ✅ MAF | ✅ | ✅ | ✅ 汇总 |
| RNA-seq 基因表达 | ✅ STAR counts | ✅ | ✅ BAM/FASTQ | ❌ |
| Copy Number | ✅ | ✅ | ✅ | ✅ |

## 已发表文献关键数据 (Skerget et al. 2024, Nature Genetics, n=1,143)

### 基线人口学特征
- **中位年龄**: 63 岁 (范围 27-93)
- **性别**: 男性 60.4%, 女性 39.6%
- **ISS I期**: 35.1%, **ISS II期**: 35.1%, **ISS III期**: 27.2%
- **中位OS**: 103.6 个月 (ISS III: 53.9 个月)

### 细胞遗传学异常频率 (FISH)
- **del(17p13)**: 109/871 (12.5%)
- **t(4;14) - NSD2/WHSC1/MMSET**: 109/851 (12.8%)
- **del(13q14)**: 453/871 (52.0%)
- **gain(1q21)**: 307/871 (35.2%)
- **del(1p22)**: 212/871 (24.3%)
- **高危细胞遗传学** (≥1 of: del17p13, t(14;16), t(14;20), t(8;14), t(4;14)): 247/832 (29.7%)
- **超二倍体 (HRD)**: 57.2%, **非超二倍体 (NHRD)**: 42.8%

### 其他已发表频率 (ASH 2024, IA19)
- **t(14;16)**: 3.6%, **t(14;20)**: 2.4%
- **TP53突变**: 7.9%
- **≥2个高危特征**: 26.1%

### 治疗反应 (一线)
- **一线治疗有效率 (≥PR)**: 约 33-36%
- **原发难治**: 约 55-62%

## 数据获取途径

### 途径1: MMRF Researcher Gateway (推荐，最完整)
- 网址: https://research.themmrf.org/
- 免费注册，下载 IA19/IA20 FlatFiles
- 包含所有需求字段

### 途径2: NCI GDC API (开放，部分数据)
- API: https://api.gdc.cancer.gov/
- 项目ID: MMRF-COMMPASS
- 可获取临床TSV、RNA-seq、突变MAF、拷贝数
- 缺失: FISH、PFS、治疗反应

### 途径3: AWS S3 (开放，RNA-seq)
- s3://gdc-mmrf-commpass-phs000748-2-open/
- RNA-seq STAR counts

### 途径4: R Bioconductor
```r
BiocManager::install("TCGAbiolinks")
clinical <- GDCquery_clinic(project = "MMRF-COMMPASS", type = "clinical")
```
