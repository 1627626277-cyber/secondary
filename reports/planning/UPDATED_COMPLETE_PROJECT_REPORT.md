# 多发性骨髓瘤空间转录组公共数据库整合项目新版完整报告

**项目目录**：`D:\二区`  
**当前日期**：2026-04-28  
**目标定位**：SCI 二区偏生物信息学、转化医学、肿瘤数据分析方向  
**研究类型**：公共数据库整合分析 + 空间转录组再分析 + 稳健性证据链 + 假设生成

---

## 1. 总体结论

本项目可以继续推进，且已经完成了从“研究构想”到“可执行工程项目”的第一轮落地。

当前已经完成：

- GSE269875 元数据解析。
- 人/鼠样本主线拆分。
- 增强版样本清单构建。
- Windows 原生工具链下载与部署。
- D 盘空间检查。
- hMM1 pilot 样本确定。

当前尚未完成：

- `hg38.fa` 与 `mm10.fa` 参考基因组准备。
- `makeblastdb` 数据库构建。
- `SRX24927515` 单样本 SRA 下载与 FASTQ 转换。
- Magic-BLAST 人/鼠双参考物种 QC。
- 后续 9 个人类样本批量 QC。
- 空间解卷积与 RCTD/基线方法一致性分析。

因此，项目目前处于：

> **数据治理完成，Windows 工具链基本完成，准备进入参考基因组准备与 hMM1 单样本 pilot 阶段。**

---

## 2. 投稿目标与论文定位

本项目不应定位为机制验证型论文，而应定位为：

> **多发性骨髓瘤骨髓微环境空间转录组公共数据再分析与假设生成研究。**

适合冲击的期刊方向：

- 生物信息学应用类期刊。
- 转化医学数据分析类期刊。
- 肿瘤微环境数据挖掘类期刊。
- 空间组学再分析类期刊。

不建议主攻：

- 强机制验证型肿瘤期刊。
- 要求湿实验闭环验证的实验肿瘤学期刊。
- 高影响力一区综合期刊。

核心表述边界：

- 可以写：趋势支持、一致性观察、候选空间生态位、可检验假设。
- 不应写：强验证、机制闭环、因果证明、湿实验验证、配对队列验证。

---

## 3. 原始研究计划评审

原 report 中的战略调整是合理的：

1. **删除 Stage 3 m6A integration**  
   这是正确选择。m6A 整合会显著增加审稿风险，且当前数据链不足以支撑机制闭环。

2. **删除 Nanopore 相关内容**  
   这是正确选择。Nanopore 如果不能形成完整证据链，保留反而会成为 reviewer 攻击点。

3. **主线只保留 human mainline**  
   必须执行。GSE269875 同时包含人和鼠，若混合分析，将是致命审稿风险。

4. **加入物种拆分与序列层面 QC**  
   必须执行。这是本项目能否以 Q2 生信/转化方向投稿的第一道质量门槛。

5. **加入 RCTD 或成熟基线方法做稳健性比较**  
   必须执行。这能回应“结果是否依赖单一算法”的审稿问题。

---

## 4. 当前文件与工程状态

`D:\二区` 当前主要文件包括：

- `deep-research-report (2) (1) (1).md`
- `GSE269875_family.soft.gz`
- `sample_manifest.tsv`
- `gse269875_manifest_enriched.tsv`
- `PROJECT_LOG.md`
- `NEXT_STEP_PILOT_RUNBOOK.md`
- `ENVIRONMENT_SETUP_NOTES.md`
- `scripts\`
- `tools\`
- `downloads\`

增强版 manifest 已确认 15 个样本：

| 类别 | 数量 | 说明 |
|---|---:|---|
| Human mainline | 9 | 进入主分析候选 |
| Mouse isolated/supplement | 6 | 不进入人类主线 |

人类主线样本：

| GSM | Title | Role | SRX |
|---|---|---|---|
| GSM8329290 | hHBM1 | human control | SRX24927512 |
| GSM8329291 | hHBM2 | human control | SRX24927513 |
| GSM8329292 | hHBM3 | human control | SRX24927514 |
| GSM8329293 | hMM1 | human MM pilot | SRX24927515 |
| GSM8329294 | hMM2 | human MM | SRX24927516 |
| GSM8329295 | hMM3 | human MM | SRX24927517 |
| GSM8329296 | hMM4 | human MM | SRX24927518 |
| GSM8329297 | hMM5 | human MM | SRX24927519 |
| GSM8329298 | hMM6 | human MM | SRX24927520 |

重要纠错：

> `GSM8329291` 是 `hHBM2`，不是 `hMM1`。  
> 正确的第一疾病 pilot 是 `GSM8329293 / hMM1 / SRX24927515`。

---

## 5. D 盘工具链检查结果

工具已经复制到 D 盘，但 `scripts\set_D_project_toolchain_path.bat` 中的路径与实际目录不完全一致，因此该脚本当前不能正确设置 PATH。

实际可用路径为：

```text
D:\二区\tools\sratoolkit_extract\sratoolkit.3.4.1-win64\bin
D:\二区\tools\ncbi-magicblast-1.7.2\bin
```

已验证可用：

```text
prefetch 3.4.1
fasterq-dump 3.4.1
vdb-dump 3.4.1
magicblast 1.7.2
makeblastdb 2.14.0+
```

建议手动修正 PATH：

```bat
set PATH=D:\二区\tools\sratoolkit_extract\sratoolkit.3.4.1-win64\bin;D:\二区\tools\ncbi-magicblast-1.7.2\bin;%PATH%
```

然后验证：

```bat
prefetch --version
fasterq-dump --version
vdb-dump --version
magicblast -version
makeblastdb -version
```

---

## 6. 磁盘空间评估

当前 D 盘剩余空间约：

```text
410.57 GiB
```

评估结论：

- 可以进行单样本 hMM1 pilot。
- 不建议一次性下载和解压 9 个人类样本。
- 后续应采用“一个样本一个样本串行处理”的方式。
- `sra_cache`、`fastq`、`tmp_fasterq` 必须放在 D 盘，不能放 C 盘。

安全阈值：

| 状态 | 判断 |
|---|---|
| > 400 GiB | 单样本 pilot 较安全 |
| 300-400 GiB | 可跑单样本，但必须使用 `--disk-limit` |
| < 300 GiB | 不建议完整 `fasterq-dump` |

---

## 7. 当前最大阻塞

当前最大阻塞不是工具，而是参考基因组：

缺失：

```text
D:\二区\hg38.fa
D:\二区\mm10.fa
D:\二区\blastdb\
```

需要完成：

1. 下载或准备 `hg38.fa`。
2. 下载或准备 `mm10.fa`。
3. 用 `makeblastdb` 构建两个 BLAST 数据库。

建库命令：

```bat
cd /d D:\二区
mkdir blastdb
set PATH=D:\二区\tools\sratoolkit_extract\sratoolkit.3.4.1-win64\bin;D:\二区\tools\ncbi-magicblast-1.7.2\bin;%PATH%

makeblastdb -in hg38.fa -dbtype nucl -parse_seqids -out blastdb\hg38 -title hg38
makeblastdb -in mm10.fa -dbtype nucl -parse_seqids -out blastdb\mm10 -title mm10
```

---

## 8. 下一步执行计划

### Step 1：修正 D 盘 PATH

在 Anaconda Prompt 中执行：

```bat
cd /d D:\二区
set PATH=D:\二区\tools\sratoolkit_extract\sratoolkit.3.4.1-win64\bin;D:\二区\tools\ncbi-magicblast-1.7.2\bin;%PATH%
```

验证：

```bat
prefetch --version
fasterq-dump --version
vdb-dump --version
magicblast -version
makeblastdb -version
```

### Step 2：准备参考基因组

需要准备：

```text
D:\二区\hg38.fa
D:\二区\mm10.fa
```

建议优先使用 primary assembly 或常规主参考版本，不要一开始加入过多 patch/alt contig，以降低数据库体积和运行压力。

### Step 3：构建 Magic-BLAST 数据库

```bat
cd /d D:\二区
mkdir blastdb
makeblastdb -in hg38.fa -dbtype nucl -parse_seqids -out blastdb\hg38 -title hg38
makeblastdb -in mm10.fa -dbtype nucl -parse_seqids -out blastdb\mm10 -title mm10
```

### Step 4：运行 hMM1 单样本 pilot

目标：

```text
GSM8329293 / hMM1 / SRX24927515
```

下载与 FASTQ 转换：

```bat
cd /d D:\二区
mkdir sra_cache fastq tmp_fasterq qc_species_hMM1

prefetch SRX24927515 --output-directory sra_cache --max-size 100G

fasterq-dump SRX24927515 ^
  --split-files ^
  --outdir fastq ^
  --temp tmp_fasterq ^
  --threads 8 ^
  --progress ^
  --disk-limit 300GB
```

人类参考比对：

```bat
magicblast ^
  -query fastq\SRX24927515_1.fastq ^
  -query_mate fastq\SRX24927515_2.fastq ^
  -db blastdb\hg38 ^
  -infmt fastq ^
  -outfmt tabular ^
  -num_threads 8 ^
  -out qc_species_hMM1\hMM1_hg38_magicblast.tsv
```

小鼠参考比对：

```bat
magicblast ^
  -query fastq\SRX24927515_1.fastq ^
  -query_mate fastq\SRX24927515_2.fastq ^
  -db blastdb\mm10 ^
  -infmt fastq ^
  -outfmt tabular ^
  -num_threads 8 ^
  -out qc_species_hMM1\hMM1_mm10_magicblast.tsv
```

### Step 5：判定 hMM1 是否通过

预期结果：

- hg38 命中明显占优。
- mm10 命中极低。

若通过：

- 将 hMM1 标记为 `species_seq_qc = pass_human`。
- 继续跑 hHBM1 作为健康对照 pilot。
- 再扩展到剩余 7 个人类样本。

若不通过：

- 暂停所有下游分析。
- 检查 FASTQ、参考库、命令参数、GEO 元数据是否存在异常。

---

## 9. 论文结果框架

后续论文建议按照以下结果链展开：

1. 数据来源与研究定位  
   GSE269875 + GSE223060，公共数据库整合，假设生成。

2. 样本治理与人/鼠拆分  
   展示 9 human mainline + 6 mouse isolated。

3. 序列层面物种 QC  
   展示 Magic-BLAST 人/鼠双参考结果。

4. human mainline 空间转录组 QC  
   包括 spot、UMI、基因数、组织图像与空间坐标完整性。

5. scRNA 参考构建  
   基于 GSE223060，说明非配对、非同批。

6. 空间解卷积主分析  
   识别 MM 骨髓微环境候选细胞组成与空间模式。

7. RCTD 或成熟基线一致性比较  
   用于证明结论不完全依赖单一算法。

8. 候选空间生态位与分子线索  
   保持假设生成表述，不写机制闭环。

9. 局限性与未来验证  
   明确无湿实验、非配对、样本量有限。

---

## 10. SCI 二区可行性判断

若完成以下最低闭环，本项目具备冲击 SCI 二区偏生信/转化医学/肿瘤数据分析期刊的基础：

- 9 个 human mainline 样本全部完成物种 QC。
- 主分析完全排除 mouse 混入。
- 空间解卷积结果有清晰生物学故事。
- 至少一个成熟 baseline 方法完成一致性验证。
- 图表质量达到投稿标准。
- 讨论中主动承认非配对、无湿实验、假设生成边界。

当前离可投稿还有较大距离，但路径是清晰的。

当前完成度估计：

```text
工程准备：约 35%
可投稿数据结果：约 10%
整体论文完成：约 15%
```

---

## 11. 最优先任务

下一步只做一件事：

> **准备 `hg38.fa` 与 `mm10.fa`，然后构建 Magic-BLAST 数据库。**

完成后立即进入：

> **`SRX24927515 / hMM1` 单样本 pilot。**

这一步跑通后，项目才算真正进入可扩展分析阶段。


---

## 12. hMM1 单样本 Pilot 已完成

Pilot 样本：`GSM8329293 / hMM1`  
SRA experiment：`SRX24927515`  
实际 run accession：`SRR29414112`

执行内容：

- 使用 SRA Toolkit 下载 `SRR29414112`。
- 使用 `fastq-dump --split-files -X 1000000` 抽取前 1,000,000 spots。
- 确认 `SRR29414112_4.fastq` 为 50 bp transcript read，用于物种 QC。
- 使用 Magic-BLAST 分别比对 hg38 与 mm10。

结果：

| 指标 | hg38 / human | mm10 / mouse |
|---|---:|---:|
| sampled reads | 1,000,000 | 1,000,000 |
| reads with any hit | 370,748 | 69,886 |
| hit rate | 37.07% | 6.99% |

交叉分类：

| 分类 | read 数 | 比例 |
|---|---:|---:|
| human-only | 301,832 | 30.18% |
| mouse-only | 970 | 0.10% |
| both | 68,916 | 6.89% |
| neither | 628,282 | 62.83% |

关键比值：

- human hit / mouse hit = 5.31
- human-only / mouse-only = 311.17

判定：

> `GSM8329293 / hMM1 / SRR29414112` 通过 sampled Magic-BLAST 物种 QC，可保留在人类主线中。

说明：

该结果用于物种归属 QC，不用于表达定量。由于使用的是 50 bp transcript read 的抽样比对，绝对 hit rate 不应按全基因组 DNA 比对阈值解释；重点是 human-only 与 mouse-only 的相对优势。当前 mouse-only 比例仅 0.10%，支持 hMM1 为 human mainline 样本。

下一步：

1. 对一个健康对照样本执行相同 sampled QC，建议 `GSM8329290 / hHBM1 / SRX24927512`。
2. 若 hHBM1 通过，再对剩余 7 个人类样本批量执行同一流程。
3. 生成 `species_filter_log.md`，作为论文补充材料中的审计证据。

---

## 13. hHBM1 健康对照 sampled species QC 已完成

样本：GSM8329290 / hHBM1  
SRA experiment：SRX24927512  
实际 run：SRR29414117; SRR29414118

执行内容：

- 两个 run 均已下载并通过 db-validate。
- 每个 run 使用 astq-dump --split-files -X 1000000 抽取前 1,000,000 spots。
- 确认 read 4 为 50 bp transcript read，用于物种 QC。
- 使用 Magic-BLAST 分别比对 hg38 与 mm10。

聚合结果：

| 指标 | 数值 |
|---|---:|
| sampled transcript reads | 2,000,000 |
| human hit | 1,934,721 (96.74%) |
| mouse hit | 349,020 (17.45%) |
| human-only | 1,585,826 (79.29%) |
| mouse-only | 125 (0.01%) |
| both | 348,895 (17.44%) |
| neither | 65,154 (3.26%) |
| human hit / mouse hit | 5.54 |
| human-only / mouse-only | 12,686.61 |

判定：

> GSM8329290 / hHBM1 通过 sampled Magic-BLAST human species QC，可保留在人类主线中。

当前物种 QC 已完成 2/9：

- hMM1 疾病 pilot：通过。
- hHBM1 健康对照 pilot：通过。

下一步：对剩余 7 个人类主线样本执行同一 sampled QC，并生成正式 species_filter_log.md 作为补充材料证据链。
