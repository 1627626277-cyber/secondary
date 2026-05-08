# MMRF CoMMpass 数据字段完整映射

## 最优先字段

### 1. Patient Clinical Data（患者临床数据）

| 需求字段 | 数据来源 | 访问方式 | 状态 |
|---------|---------|---------|------|
| 年龄 (Age) | PER_PATIENT → D_PT_age | MMRF Gateway / GDC Clinical | ✅ 已发表: 中位63岁(27-93) |
| 性别 (Sex) | PER_PATIENT → D_PT_gender | MMRF Gateway / GDC Clinical | ✅ 已发表: 男60.4%, 女39.6% |
| 诊断 (Diagnosis) | PER_PATIENT / GDC diagnoses | MMRF Gateway / GDC API | ✅ NDMM |
| ISS Stage | PER_PATIENT → R_ISS / D_PT_iss | MMRF Gateway / GDC Clinical | ✅ 已发表: I 35.1%, II 35.1%, III 27.2% |
| R-ISS Stage | PER_PATIENT → 计算自 ISS+LDH+FISH | MMRF Gateway | ✅ 已发表汇总 |
| LDH | PER_PATIENT_VISIT → D_LAB_serum_ldh | MMRF Gateway | ✅ 已发表: >250 U/L ~16% |
| β2-Microglobulin | PER_PATIENT_VISIT → D_LAB_serum_beta2_microglobulin | MMRF Gateway | ✅ 已发表: <3.5 ~37%, ≥5.5 ~36% |
| Albumin | PER_PATIENT_VISIT → D_LAB_chem_albumin | MMRF Gateway | ✅ 已发表: ≥3.5 ~65% |
| 随访 (Follow-up) | PER_PATIENT → D_PT_lstalive, D_PT_lastdy | MMRF Gateway | ✅ ≥8年 |
| OS (Overall Survival) | PER_PATIENT → D_PT_deathdy / D_PT_lastdy | MMRF Gateway / GDC API | ✅ 已发表: 中位103.6月 |

### 2. Outcome / Survival / PFS（疗效/生存/PFS）

| 需求字段 | 数据来源 | 访问方式 | 状态 |
|---------|---------|---------|------|
| PFS time | MMRF_OS_PFS_ASCT.csv / non-ASCT.csv | **MMRF Gateway 专属** | ⚠️ 需注册 |
| PFS event | 同上 | **MMRF Gateway 专属** | ⚠️ 需注册 |
| Progression date | 同上 → Progression Day | **MMRF Gateway 专属** | ⚠️ 需注册 |
| Relapse date | STAND_ALONE_TRTRESP | **MMRF Gateway 专属** | ⚠️ 需注册 |
| Death date | PER_PATIENT → D_PT_deathdy | MMRF Gateway / GDC | ✅ GDC可获取 |
| Last follow-up | PER_PATIENT → D_PT_lstalive | MMRF Gateway / GDC | ✅ GDC可获取 |

### 3. Treatment Response（治疗反应）

| 需求字段 | 数据来源 | 访问方式 | 状态 |
|---------|---------|---------|------|
| CR/sCR/VGPR/PR/SD/PD | STAND_ALONE_TRTRESP → bestresp | **MMRF Gateway 专属** | ⚠️ 需注册 |
| Best overall response | STAND_ALONE_TRTRESP | **MMRF Gateway 专属** | ⚠️ 需注册 |
| Refractory status | STAND_ALONE_TRTRESP (衍生) | **MMRF Gateway 专属** | ⚠️ 需注册 |
| 治疗后进展/复发 | PER_PATIENT_VISIT → AT_DEVELOPMENTOF | **MMRF Gateway 专属** | ⚠️ 需注册 |

### 4. Treatment / Regimen / Therapy Line（治疗方案）

| 需求字段 | 数据来源 | 访问方式 | 状态 |
|---------|---------|---------|------|
| 一线方案 | STAND_ALONE_TRTRESP line=1 → trtshnm | **MMRF Gateway 专属** | ✅ 已发表常用方案 |
| 治疗线数 | STAND_ALONE_TRTRESP → line | **MMRF Gateway 专属** | ⚠️ 需注册 |
| 药物类别 | STAND_ALONE_TRTRESP → trtclass | **MMRF Gateway 专属** | ✅ 已发表: PI 90%, IMiD 92% |
| 具体药物 | STAND_ALONE_TRTRESP → trtshnm | **MMRF Gateway 专属** | ⚠️ 需注册 |
| ASCT | PER_PATIENT → line1sct / STAND_ALONE_TRTRESP → bmtx_day | **MMRF Gateway 专属** | ✅ 已发表: ~45% |
| 治疗起止日期 | STAND_ALONE_TRTRESP → trtstdy, trtendy | **MMRF Gateway 专属** | ⚠️ 需注册 |

### 5. Cytogenetics / FISH（细胞遗传学/FISH）

| 需求字段 | 数据来源 | 访问方式 | 状态 |
|---------|---------|---------|------|
| del17p | PER_PATIENT → CYTO_del_17p13 / FISH_del_17p13 | **MMRF Gateway 专属** | ✅ 已发表: 12.5% |
| t(4;14) | PER_PATIENT → CYTO_t_4_14 | **MMRF Gateway 专属** | ✅ 已发表: 12.8% |
| t(14;16) | PER_PATIENT → CYTO_t_14_16 | **MMRF Gateway 专属** | ✅ 已发表: 3.6% |
| 1q gain/amplification | PER_PATIENT → CYTO_gain_1q21 | **MMRF Gateway 专属** | ✅ 已发表: 35.2% |
| del13q | PER_PATIENT → CYTO_del_13q14 | **MMRF Gateway 专属** | ✅ 已发表: 52.0% |
| 高危细胞遗传学 | PER_PATIENT (衍生: ≥1 HR feature) | **MMRF Gateway 专属** | ✅ 已发表: 29.7% |

### 6. Sample / Patient Mapping（样本/患者映射）

| 需求字段 | 数据来源 | 访问方式 | 状态 |
|---------|---------|---------|------|
| Patient ID | 所有文件 → PUBLIC_ID / Patient | MMRF Gateway / GDC | ✅ GDC可获取 |
| Sample ID | PER_PATIENT_VISIT / GDC biospecimen | MMRF Gateway / GDC | ✅ GDC可获取 |
| Aliquot ID | GDC biospecimen | MMRF Gateway / GDC | ✅ GDC可获取 |
| Baseline 标记 | PER_PATIENT_VISIT → VISIT=0 | MMRF Gateway | ⚠️ 需注册 |
| Visit/Timepoint | PER_PATIENT_VISIT → VISIT, VISITDY | MMRF Gateway | ⚠️ 需注册 |
| CD138+ 状态 | PER_PATIENT_VISIT / GDC sample metadata | MMRF Gateway / GDC | ✅ GDC可获取 |

## 次优先字段

### Copy Number Estimates 和 Somatic Variants

| 需求字段 | 数据来源 | 访问方式 | 状态 |
|---------|---------|---------|------|
| Copy number estimates | GDC → Copy Number Variation → Masked Copy Number Segment | GDC API (开放) | ✅ GDC开放 |
| TP53 mutation | GDC → Masked Somatic Mutation MAF | GDC API (开放) | ✅ 已发表: 7.9% |
| KRAS mutation | GDC → Masked Somatic Mutation MAF | GDC API (开放) | ✅ 已发表: 22.0% |
| NRAS mutation | GDC → Masked Somatic Mutation MAF | GDC API (开放) | ✅ 已发表: 20.0% |
| BRAF mutation | GDC → Masked Somatic Mutation MAF | GDC API (开放) | ✅ 已发表: 7.0% |
| DIS3 mutation | GDC → Masked Somatic Mutation MAF | GDC API (开放) | ✅ 已发表: 11.0% |
| FAM46C mutation | GDC → Masked Somatic Mutation MAF | GDC API (开放) | ✅ 已发表: 10.0% |
| Structural variants / fusions | GDC → Structural Variant calls | GDC API (开放) | ✅ GDC开放 |
| RNA-seq gene expression | GDC → STAR counts / AWS S3 open bucket | GDC API / AWS S3 (均开放) | ✅ 开放 |

## 关键数据缺口及解决方案

### 缺口1: FISH/细胞遗传学（完整患者级数据）
**原因**: FISH数据在GDC中不完整，完整数据需MMRF Researcher Gateway
**解决**: 
- 方案A: 注册 https://research.themmrf.org/ (免费)，下载IA19 FlatFiles
- 方案B: 使用已发表频率作为先验 (已提供 published_fish_cytogenetics.csv)
- 方案C: 从GDC MAF中的拷贝数片段推断部分细胞遗传学异常 (del17p, gain1q, del13q)

### 缺口2: PFS (无进展生存)
**原因**: PFS终点需MMRF Researcher Gateway
**解决**:
- 方案A: 注册MMRF Gateway（唯一完整来源）
- 方案B: 从GDC clinical数据中提取OS（可用），用中位PFS ~36个月作为替代

### 缺口3: 治疗反应 (CR/VGPR/PR等)
**原因**: 治疗反应数据需MMRF Researcher Gateway
**解决**: 
- 方案A: 注册MMRF Gateway
- 方案B: 从GDC clinical supplement中提取部分治疗信息

## 推荐工作流

```
第一步（立即）: 运行 assemble_mmrf_data.py → 获取已发表汇总数据 + 合成原型数据
第二步（优先）: 注册 MMRF Researcher Gateway → 下载 IA19 FlatFiles
第三步: 运行 parse_mmrf_flatfiles.py → 解析真实患者级数据
第四步: 运行 assemble_mmrf_data.py → 补充 GDC 开放数据（RNA-seq, 突变, 拷贝数）
```
