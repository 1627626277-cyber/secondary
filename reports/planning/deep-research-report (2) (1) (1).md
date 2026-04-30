# 多发性骨髓瘤空间转录组公共数据库整合与假设生成研究修订稿

## 执行摘要

本次重写在作者视角下，将研究**严格定位**为：**“公共数据库整合分析 + 假设生成（hypothesis generation）”**。在稿内将明确声明：本研究不属于**配对/同批（paired/batched）设计**下的强验证研究，也**未开展任何湿实验验证**；因此所有结论必须以“趋势支持、一致性观察、可检验假设”为边界表述，而非“独立外部验证/强验证/机制闭环证明”。这一定位与数据事实一致：GSE269875 的 GEO Series 记录明确包含两种物种（*Homo sapiens* 与 *Mus musculus*）且为 Visium 空间转录组（NextSeq 2000；两平台：GPL30172/73），必须先做物种拆分后才能进入主分析链。 citeturn1search0

你已明确宣布**第三阶段（m6A 数据整合）立即终止**：本修订稿将 **Stage 3（m6A integration）从研究设计、方法、结果、讨论、图表与补充材料中完全删除**；同时依据你的要求，**Nanopore 相关内容也将全文彻底删除**（不保留 supporting evidence，不保留流程图/表格/附录脚本）。本稿将增加两条 reviewer 常见质疑的“硬证据链”：其一是 **GSE269875 的人/鼠样本可复现拆分与序列层面物种归属鉴别**；其二是 **空间解卷积引入成熟基线方法 RCTD（spacexr）做一致性验证**并以相关、CCC 与 Bland–Altman 等统计量呈现稳健性。RCTD 的原始方法论文指出空间测量常为多细胞混合、需要结合 scRNA 参考并校正平台差异来分解细胞组成，非常契合“跨平台公共数据整合”的叙事。 citeturn0search1turn12search4turn4search0

---

## 研究定位与删减决策

**研究定位（稿内必须三处重复一致口径：摘要末句 + 引言末段 + 讨论首段，可直接粘贴）**  
> 本研究定位为**公共数据库整合分析与假设生成研究**。我们整合公开的单细胞转录组（GSE223060）与空间转录组（GSE269875）数据，开展空间细胞组成推断与稳健性检验，以提出可检验的生物学假设与候选分子线索。由于两数据集并非配对同批样本，且本研究未开展湿实验验证，相关发现仅构成**趋势支持与假设生成证据**，不构成严格意义上的外部强验证或机制因果证明。 citeturn1search0turn4search5turn12search6

**主线与补充线定义（强制执行）**  
1) **主分析主线仅保留 human mainline**：GSE269875 中 *Homo sapiens* 空间样本进入主结果链。GSE269875 的 Series 明确同时存在人/鼠样本，且分别对应不同平台（GPL30173：human；GPL30172：mouse）。 citeturn1search0  
2) **mouse 样本不混入主链**：mouse 只允许作为独立 supplement（完全分开统计、分开作图、分开讨论）；若目标是最大限度降低 reviewer 对“跨物种混杂”的攻击面，建议本轮投稿在正文与补充材料中都**不展开** mouse 结果，仅在方法中说明“已做物种拆分与剔除/隔离”。 citeturn1search0turn1search1

**删减决策（你已批准并需在“修订说明/变更记录”中明示）**  
- **Stage 3（m6A integration）终止并删除**：所有与第三阶段相关的图、表、补充分析、结论链条一律删除；正文中不再出现“第三阶段/多组学整合闭环”等措辞。  
- **Nanopore 完全删除**：不保留 supporting evidence；摘要、结果、讨论、图注、流程图、补充脚本及文件名中不得出现 “Nanopore/ONT/FAST5/direct RNA/long-read”等残留字样（见文末红线清单）。  

---

## 数据集关系核查与“非配对/非同批”证据链

### 你需要做的“非配对/非同批”核查项

下列核查建议在**方法（Data provenance & cohort comparability）**与**补充材料（Checklist + evidence table）**中呈现，形成“我们核查了什么 → 证据是什么 → 因此结论如何降级”的闭环。

**核查维度与可引用字段（建议逐条勾选并截图/导出文本留档）**  
1) **Series 层级时间线与提交方**：  
- GSE269875：Public on **Jun 09, 2025**；Submission date **Jun 14, 2024**；Contact 为 Laura Sudupe（KAUST）。 citeturn1search0  
- GSE223060：Public on **Jan 17, 2023**；Submission date **Jan 17, 2023**；Contact 为 Ravi Vij（Washington University in St. Louis）。 citeturn4search5turn12search6  
这在结构上已构成“不同研究团队、不同时间、不同提交与实验链”的强证据，**不可能是同一批次/同一实验条件的配对数据**。 citeturn1search0turn4search5  

2) **平台与测序仪（批次核心信息）**：  
- GSE269875：NextSeq 2000（human 与 mouse 分属 GPL30173/30172）。 citeturn1search0turn1search1  
- GSE223060：Illumina HiSeq 4000（GSM 示例显示 instrument model HiSeq 4000；平台 GPL20301）。 citeturn4search5turn12search6  
平台/仪器差异意味着文库化学、读长结构、建库与计数流程均可能不同，不能写作“同批验证”。 citeturn1search1turn12search6  

3) **数据类型与处理流程（决定不可“同质验证”）**：  
- GSE269875（示例 GSM8329284）明确描述：用 10x Genomics **Space Ranger** 生成 FASTQ 并对 **mm10** 比对计数（mouse）。 citeturn1search1  
- GSE223060（示例 GSM6939049）明确描述：单细胞数据以 **Cell Ranger v3.0.0** 对人类参考（GRCh38/hg38）生成基因×细胞 UMI 矩阵，后续在 Seurat 中 QC 与校正。 citeturn12search6  
“空间 spot 混合测量 vs 单细胞”是不同测量体系，整合只能用于推断与一致性观察，不能宣称“严格验证”。  

4) **样本命名与 ID 体系（患者/样本配对的直接证据）**：  
- GSE269875 的样本命名包含 YFP1/2、MM1–4、hHBM1–3、hMM1–6。 citeturn1search0  
- GSE223060 的样本命名包含 MMRF_**** 等体系（Series 样本列表开头即显示）。 citeturn4search5  
两者样本 ID 结构不同且无明显可对齐字段，默认判定为**非配对**；如 reviewer 追问，补充材料提供“无 shared sample ID / 无 shared BioProject / 无 shared submitter”的证据表即可。 citeturn1search0turn4search5  

5) **原始数据分发方式（进一步支持非同批）**：  
- GSE269875 明确“Raw data are available in SRA”。 citeturn1search0  
- GSE223060 的 GSM 示例页写明“Raw data not provided for this record；Processed data provided as supplementary file”，与其人类隐私属性相符。 citeturn12search6  
这意味着可用的原始层级与处理策略天然不同，进一步削弱“同批验证”的叙事空间。  

### 用于重写摘要/引言/讨论的精准句子（可直接粘贴）

**摘要末句（替换所有“验证/confirmed/validated”措辞）**  
> 我们在独立公共数据之间进行整合分析与一致性观察：跨数据集一致方向的发现被视为**支持性趋势证据**，用于提出可检验假设；鉴于数据并非配对同批样本且缺乏湿实验验证，本文结论不构成严格外部强验证。 citeturn1search0turn4search5  

**引言末段（把研究目标从“验证机制”改成“建立可复现流程与候选假设”）**  
> 因公开数据在平台、处理流程与样本来源上存在天然异质性，我们将研究目标限定为：构建可复现的数据治理与空间推断流程，识别具有一致趋势的候选细胞状态与分子特征，并以稳健性分析筛选优先级最高、最值得后续实验验证的假设。 citeturn0search1  

**讨论首段（先降调，主动抢占 reviewer 质疑点）**  
> 本研究的主要贡献在于公共数据库整合框架与稳健性证据链：我们对 GSE269875 进行了严格的物种拆分与可追溯记录，并在主解卷积之外引入成熟基线方法 RCTD 进行一致性检验。受限于非配对同批设计与缺乏湿实验验证，本文所有发现应被解读为假设生成性结果，为后续独立队列与实验体系提供线索与优先级。 citeturn1search0turn0search1turn4search0  

---

## GSE269875 人/鼠样本拆分与物种归属鉴别的可复现流程

GSE269875 的 Series 页面已明确“Organisms: *Homo sapiens; Mus musculus*”，并给出 15 个 GSM。该系列同时提供处理后数据包（`GSE269875_RAW.tar`，含 CSV/JPG/JSON/MTX/PNG/TSV）与 SRA 原始数据入口。 citeturn1search0

下面流程以“可复现、可审计、可落地”为原则：**先元数据拆分（低成本）→ 再用序列证据复核（高可信）→ 输出 manifest 与剔除日志（可追溯）**。

### 元数据层拆分：下载 Series Matrix / SOFT / 纯文本记录

GEO 官方说明：可从 Series 页面底部下载 family（SOFT/MINiML/Series Matrix），也可通过 FTP；并支持构造 URL 以纯文本方式检索记录。 citeturn3search2turn10search0  
SOFT 格式为 GEO 的线性文本格式，官方说明其已在 2024 年初停止用于提交/更新，但仍持续提供下载，因此适合程序化解析。 citeturn12search0  

**命令：通过 FTP 下载 Series Matrix 与 family SOFT**  
```bash
# Series Matrix（常含 !Sample_ 注释行）
wget -O GSE269875_series_matrix.txt.gz \
  "https://ftp.ncbi.nlm.nih.gov/geo/series/GSE269nnn/GSE269875/matrix/GSE269875_series_matrix.txt.gz"

# family SOFT（含 GSE + 所有 GSM + 平台等元数据）
wget -O GSE269875_family.soft.gz \
  "https://ftp.ncbi.nlm.nih.gov/geo/series/GSE269nnn/GSE269875/soft/GSE269875_family.soft.gz"
```
（GEO 官方明确 FTP 路径结构例如 `.../geo/series/GSE1nnn/GSExxxx/matrix/`。） citeturn3search2turn10search0  

**命令：构造 URL 获取“纯文本 full 视图”（适合写入日志与审计）**  
```bash
# GEO 官方给出 acc/targ/view/form 组成规则
# 例：拉取一条记录的 full text（建议用于关键 GSM 的审计快照）
perl -MLWP::Simple -e "getprint 'https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE269875&targ=self&view=full&form=text'" \
  > GSE269875_full.txt
```
（该构造 URL 机制由 GEO 官方文档说明。） citeturn10search0turn3search2  

### Python 伪代码：解析 Series Matrix / SOFT 并生成样本清单

目标输出文件：`sample_manifest.tsv`（每行一个 GSM，包含物种、组织、平台、批次字段、以及后续序列鉴别结果列）。

**Python 伪代码：Series Matrix 解析（低依赖）**  
```python
import gzip
import pandas as pd

def parse_series_matrix(path_gz: str) -> pd.DataFrame:
    with gzip.open(path_gz, "rt", encoding="utf-8", errors="ignore") as f:
        lines = f.readlines()

    # 提取所有 !Sample_ 注释行
    sample_lines = [ln for ln in lines if ln.startswith("!Sample_")]

    rows = []
    for ln in sample_lines:
        parts = ln.rstrip("\n").split("\t")
        key = parts[0].replace("!Sample_", "")
        vals = parts[1:]
        rows.append((key, vals))

    kv = dict(rows)
    gsm = kv.get("geo_accession", [])
    meta = pd.DataFrame({"GSM": gsm})

    # 常见字段：title, organism_ch1, source_name_ch1, characteristics_ch1, platform_id 等
    for k, vals in rows:
        if len(vals) == len(meta):
            meta[k] = vals

    return meta

meta = parse_series_matrix("GSE269875_series_matrix.txt.gz")
meta.to_csv("sample_manifest.tsv", sep="\t", index=False)
```

**SOFT 解析提示（用于补齐 submission_date / last_update_date / contact / platform 等）**  
SOFT 文档明确 family SOFT 包含 `_submission_date`、`_last_update_date`、`_contact_*` 等属性字段，适合补齐审计列并写入 manifest。 citeturn12search0  

### “human mainline vs mouse supplement”元数据判定规则

以 reviewer 可接受的方式写入 Methods：**先按 GEO 的 Organism + 平台拆分，再进入序列复核**。GSE269875 Series 已明确两平台：GPL30172（mouse）与 GPL30173（human）。 citeturn1search0  

**建议规则（写入 Methods）**  
- 若 `organism == "Homo sapiens"` 且 `platform_id == "GPL30173"` → `species_geo = human`，候选进入主线  
- 若 `organism == "Mus musculus"` 且 `platform_id == "GPL30172"` → `species_geo = mouse`，进入 supplement/隔离库  
- 任一字段缺失或不一致 → 标记 `metadata_flag = TRUE`，必须进行序列级复核（见下）  

### SRA 下载与 FASTQ 生成：prefetch + fasterq-dump（含磁盘风险提示）

GSE269875 明确原始数据在 SRA，并在 GSM 页面“Relations”中给出 SRX（如 GSM8329284 → SRX24927506）。 citeturn1search0turn1search1  
NCBI sra-tools 官方 wiki 强调：`fasterq-dump` 会创建临时目录，最坏情况下临时空间可达最终输出文件大小的约 10 倍，因此需提前规划输出目录和临时目录（可用 `-t` 指定）。 citeturn2search0  

**示例命令（推荐写入脚本 `03_fetch_sra_fastq.sh`）**  
```bash
# 1) 下载 SRA（建议指定缓存目录，便于断点续传与清理）
prefetch SRX24927506 --output-directory ./sra_cache

# 2) 导出 FASTQ（建议：输出盘与临时盘分离；临时盘尽量 SSD）
fasterq-dump ./sra_cache/SRX24927506 \
  --split-files \
  --threads 8 \
  --outdir ./fastq \
  --temp ./tmp_fasterq
```

**资源受限时的“最小化下载”策略（写入 Methods 的 Practical note）**  
- 先用 `vdb-dump --info` 估算 accession 大小，再决定是否全量导出；并在脚本中加入 `--size-check only` 或 `--disk-limit` 以避免磁盘爆炸（这些能力由 sra-tools wiki 明确说明）。 citeturn2search0  
- 仅为“物种鉴别”时，可对 FASTQ 抽样（例如抽取前/随机的 `{N}` 对 read pairs）再进行 Kraken2/minimap2，以换取更低成本（稿内明确“该步骤用于物种归属 QC，而非下游表达定量”）。  

### 序列级物种归属鉴别：两条可复现管线（Kraken2 与 minimap2）

#### 管线一：Kraken2（最小 human+mouse 数据库）

Kraken2 的原始论文指出其通过 minimizer 等设计降低 Kraken 经典 k-mer 方法的内存负担并提升速度，是成熟的分类框架。 citeturn0search0turn0search2  
但“包含完整真核基因组”的数据库仍可能产生较高 CPU 内存占用；因此你需要把它定位为“用于物种归属 QC 的最小数据库”。（显存不参与；这是 CPU 内存问题。）

**最小数据库构建思路（示例；你需在补充脚本中固定版本与参考来源）**  
```bash
# 建议用独立目录，便于复现与缓存
DB=kraken_hs_mm
mkdir -p $DB

# 1) 下载 taxonomy
kraken2-build --download-taxonomy --db $DB

# 2) 添加自定义参考（推荐在 fasta header 中加入 taxid）
# >kraken:taxid|9606|chr1  ...
# >kraken:taxid|10090|chr1 ...
kraken2-build --add-to-library GRCh38.taxid9606.fa --db $DB
kraken2-build --add-to-library mm10.taxid10090.fa   --db $DB

# 3) 构建
kraken2-build --build --db $DB
```

**分类与决策阈值（写入 Methods，保证可审计）**  
```bash
kraken2 --db kraken_hs_mm --threads 8 \
  --paired sample_R1.fastq sample_R2.fastq \
  --report sample.kraken2.report \
  --output sample.kraken2.out
```

建议在稿内固定阈值（示例，可按你真实数据调整，但要“事前声明”）：  
- `P(human) ≥ 0.95 且 P(mouse) ≤ 0.05` → `species_seq = human`  
- `P(mouse) ≥ 0.95 且 P(human) ≤ 0.05` → `species_seq = mouse`  
- 其他情况 → `species_seq = ambiguous`（疑似污染/混合/低质量/数据库或参数问题），主线必须剔除或单列说明。  

#### 管线二：minimap2（hg38 vs mm10 双参考比对，更直观、成本更可控）

minimap2 论文明确其可用于**≥100bp 的高准确短读段**比对，因此可用于 Visium/Illumina FASTQ 的快速物种判定（这一步是 QC，不是最终表达定量）。 citeturn3search0turn3search1  

**示例命令（推荐写入脚本 `04_species_assignment_minimap2.sh`）**  
```bash
# 一次性建索引
minimap2 -d GRCh38.mmi GRCh38.fa
minimap2 -d mm10.mmi   mm10.fa

# short reads 参数：-x sr
minimap2 -ax sr -t 8 GRCh38.mmi sample_R1.fastq sample_R2.fastq | \
  samtools flagstat - > mapstat_hg38.txt

minimap2 -ax sr -t 8 mm10.mmi sample_R1.fastq sample_R2.fastq | \
  samtools flagstat - > mapstat_mm10.txt
```

**判定阈值（建议与 Kraken2 逻辑一致，写入 Methods）**  
- 若 `hg38_mapped_ratio ≥ 0.95` 且 `mm10_mapped_ratio ≤ 0.05` → `species_seq = human`  
- 若 `mm10_mapped_ratio ≥ 0.95` 且 `hg38_mapped_ratio ≤ 0.05` → `species_seq = mouse`  
- 否则 → `species_seq = ambiguous`（需剔除或隔离，并在日志解释）

**为何建议 minimap2 作为首选 QC**  
在单机资源受限环境下，minimap2 的双比对更易解释、数据库准备更可控；而 Kraken2 的数据库构建与内存占用不确定性更高（尤其在包含真核参考时）。minimap2 的适用性与性能特征由其原始方法论文描述。 citeturn3search0turn0search0  

### QC 检查与必需输出文件

**最低 QC 集合（建议写入 Methods，并在 supplement 给出阈值与通过率）**  
- 元数据一致性：`organism` vs `platform` 一致；GSE269875 明确 human/mouse 对应不同平台（GPL30173/72）。 citeturn1search0  
- 序列归属一致性：`species_geo` 与 `species_seq` 一致（minimap2 或 Kraken2）；若不一致则剔除/隔离。  
- SRA/FASTQ 完整性：fasterq-dump 输出文件大小非零、read 数合理；并记录使用的临时目录与磁盘限制参数（sra-tools 指出临时目录与磁盘检查机制）。 citeturn2search0  
- （可选）基础 read QC：FastQC/MultiQC（轻量、CPU 友好），用于识别污染或严重质量问题（可放补充材料，不强制写入主文）。

**文件与格式模板（建议直接作为补充材料附录）**

`sample_manifest.tsv`（每行一个 GSM，空缺用 `NA`；所有下游脚本以此为“唯一真相”）：  
```text
GSE	GSM	title	organism_geo	platform_id	instrument_model	technique	tissue	source_name	submission_date	last_update_date	SRX_or_SRR	species_seq	method_seqQC	metadata_flag	seq_flag	include_mainline	batch_id	notes
GSE269875	GSM832929{X}	{...}	Homo sapiens	GPL30173	NextSeq 2000	{Visium...}	Bone marrow	Bone marrow	{...}	{...}	{SRX...}	human	minimap2	{TRUE/FALSE}	{TRUE/FALSE}	Yes	{...}	{...}
```

`species_filter_log.md`（剔除/隔离的审计日志模板）：  
```markdown
# GSE269875 物种拆分与剔除日志

## 结论
- human mainline 纳入：{n_human_main} 个样本（GSM 列表：{...}）
- mouse supplement：{n_mouse} 个样本（GSM 列表：{...}）
- ambiguous/剔除：{n_ambig} 个样本（GSM 列表：{...}）

## 剔除规则（固定阈值）
- metadata_flag = TRUE 或 species_seq = ambiguous 或 species_geo != species_seq → 不进入主线

## 样本级记录
- GSM{...}: 原因：{元数据不一致/双参考比对率均低/疑似混合...}；证据文件：{mapstat_hg38.txt, mapstat_mm10.txt 或 sample.kraken2.report}
```

**样本计数汇报表模板（必须按物种/组织/批次）**  
> 批次（batch）建议至少由 `platform_id + instrument_model + technique(+ space ranger/cell ranger version 如可得)` 拼接构成；GSE269875 的示例 GSM 已给出平台与仪器/技术字段（如 GSM8329284 为 NextSeq 2000、Visium FFPE_mouse_V1、mm10）。 citeturn1search1turn1search0  

| 物种（GEO） | 物种（序列QC） | 是否纳入主线 | 样本数 | 组织/来源 | 平台ID | 仪器 | 技术/化学版本 | 批次ID（拼接规则） | 备注 |
|---|---|---|---:|---|---|---|---|---|---|
| Homo sapiens | human | Yes | {n_human_main} | {Bone marrow} | GPL30173 | NextSeq 2000 | {Visium ... human} | {platform+instrument+technique} |  |
| Mus musculus | mouse | No（supp） | {n_mouse} | Bone marrow | GPL30172 | NextSeq 2000 | Visium FFPE_mouse_V1 | {platform+instrument+technique} | 不进入主结果链 citeturn1search1 |
| {NA} | ambiguous | No | {n_ambig} | {…} | {…} | {…} | {…} | {…} | 详见 species_filter_log.md |

---

## 空间解卷积：引入成熟基线 RCTD 的一致性验证框架

### 为什么选 RCTD 作为 baseline

RCTD 原始论文将空间转录组的单点测量视为多细胞混合，并提出使用 scRNA-seq 学到的细胞类型表达谱来分解混合，同时“校正跨测序技术差异”，这恰好对应你当前研究的核心风险点：跨研究、跨平台、非同批的公共数据整合。 citeturn0search1  
在实现层面，Bioconductor 的 spacexr 包明确其为 RCTD 的 Bioconductor 适配版本，并说明其学习细胞类型 profile、识别空间像素中的细胞类型并考虑平台效应。 citeturn12search4turn12search1  

### RCTD 实现要点与关键参数（写入 Methods，补充材料给 sessionInfo）

Bioconductor vignette 明确：运行分两步——`createRctd` 预处理（基因/像素过滤、差异基因、建立 cell type profiles）与 `runRctd` 解卷积；并说明三种模式：`doublet`（高分辨）、`multi`（适合 Visium 等低分辨，可设 `max_multi_types`）、`full`（无限制）。 citeturn4search0turn12search2  

**建议你在 Visium 上优先用 `multi` 做 baseline**：因为 vignette 明确 “multi” 更适合 Visium 这类低分辨 spot（每 spot 可能含多类细胞）。 citeturn4search0turn12search8  

**R 示例代码（可直接放补充脚本 `06_run_rctd_baseline.R`）**  
```r
# 安装与载入（Bioconductor vignette 给出安装方式）
if (!require("BiocManager", quietly = TRUE)) install.packages("BiocManager")
BiocManager::install("spacexr")

library(spacexr)

# 输入：
# spatial_spe: human mainline 的空间数据（SpatialExperiment/SummarizedExperiment）
# reference_se: 基于 GSE223060 构建的 scRNA 参考（含 counts + cell_type 注释）

rctd_obj <- createRctd(
  spatial_spe,
  reference_se,
  # 关键参数：vignette 指出这些用于平台效应归一化与过滤
  gene_cutoff = 0.000125,
  fc_cutoff   = 0.5,
  UMI_min     = 100,
  UMI_max     = 20000
)

res_spe <- runRctd(
  rctd_obj,
  rctd_mode = "multi",
  max_cores = 4,
  max_multi_types = 6
)

# 输出：res_spe assays 中包含 weights / weights_full 等；列为 spots，行为 cell types
```
（参数含义与 mode 适用性由 RCTD vignette 说明；spacexr 包描述亦说明其校正平台效应并识别空间像素细胞类型。） citeturn4search0turn12search1turn12search2  

### 主方法 vs RCTD 的一致性比较：指标、统计检验与图表

你需要把 “我们不是靠单一算法得出结论” 量化成 reviewer 可接受的统计证据。建议同时做 spot-level 与 sample/region-level 两层。

**指标（每个细胞类型一组）**  
- Pearson 与 Spearman：衡量趋势一致。  
- Lin’s concordance correlation coefficient（CCC）：用于评估可重复性的一致性指标；Lin 的原始论文提出该系数用于评价 reproducibility。 citeturn4search4  
- Bland–Altman：评估两方法差值的系统性偏差（bias）与一致性界限（LOA）。Bland 与 Altman 的经典论文强调：相关系数常被误用于一致性评估，应该分析差值与一致性范围。 citeturn3search7  

**统计检验（轻量、适合单机）**  
- 对每个细胞类型的 spot-level 差值 `d_i = p_i(main) - p_i(RCTD)`：  
  - 若差值近似正态：配对 t 检验（检验 bias 是否显著偏离 0）。  
  - 若非正态/重尾：Wilcoxon 符号秩检验。  
- 对 sample-level 聚合（每张切片/每个样本的平均细胞比例）：比较两方法在样本维度的 Spearman/CCC，并报告是否保持“差异方向一致”。  

**建议图（主文放关键 2–3 类细胞，其余进补充）**  
- 相关散点图：每个细胞类型一张（可挑 Top `{k}` 关键细胞类型）。  
- Bland–Altman 图：每个关键细胞类型一张（至少 `{2–3}` 张）。  
- 热图：cell type × sample 的方法间相关/差值。  
- 空间并排图：同一张切片上主方法与 RCTD 的 cell-type map 并排，强调宏观空间趋势一致。

**一致性汇总表模板（Markdown，可直接贴入补充材料）**  
| 细胞类型 | 方法A（主方法）均值±SD | 方法B（RCTD）均值±SD | Pearson r | Spearman ρ | CCC | Bland–Altman bias | LOA 下限 | LOA 上限 | bias 检验P值 | 结论一致性判定 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| {celltype1} | { } | { } | { } | { } | { } | { } | { } | { } | { } | {通过/不通过} |
| {celltype2} | { } | { } | { } | { } | { } | { } | { } | { } | { } | {通过/不通过} |

---

## 湿实验不可行与算力约束下的可行稳健性设计

### 结论强度如何因“无湿实验”而改变

你必须把“无湿实验”从一句话升级为“结论边界的主轴”，并且把它写成主动、审慎、专业的措辞：

> 本研究未开展湿实验验证，因此所有结论限于计算分析与公开数据整合层面。我们将跨数据集的一致方向性结果解释为趋势支持与假设生成证据，而非对机制的强因果证明；关键分子标志物与细胞互作假设仍需在未来通过独立空间队列与实验体系进一步验证。  

这样写的目的不是“自我削弱”，而是让 reviewer 无法以“缺乏湿实验”直接否定整篇工作——因为你已经把工作目标限定为“提出可检验假设 + 给出稳健性证据链”。

### 单张 50–60 系列 GPU（显存/算力不确定）条件下的优先级分析清单

你要求的硬约束是：单卡 RTX 50–60 系列 GPU，**显存/算力未知 → 必须标注 unspecified**。因此我们将策略定为：尽量让关键步骤跑在 CPU（更稳、可复现），GPU 只用于你现有的主模型（若存在），且不做大规模超参搜索。

同时，下载与 FASTQ 展开往往比模型推理更“吃资源”。sra-tools 明确 `fasterq-dump` 临时目录可能需到最终输出的约 10 倍空间，因此磁盘与 I/O 往往是瓶颈。 citeturn2search0  

**建议优先级与资源估算（粗范围；未知处标注 unspecified）**  

| 优先级 | 模块 | 目标 | 推荐工具/设置 | 预计时间（粗） | 内存/显存（粗） |
|---:|---|---|---|---|---|
| 最高 | GSE269875 物种拆分 + 序列QC | 消除“物种混杂”致命风险 | 元数据拆分 + minimap2 双参考；必要时 Kraken2 | {数小时–2天，取决于下载量} | CPU 内存 {16–64GB}；显存：unspecified（通常不需）；磁盘：高风险（fasterq 临时目录最坏≈10×输出） citeturn2search0turn3search0 |
| 最高 | RCTD baseline | 方法稳健性证据链 | spacexr：`rctd_mode="multi"`，`max_cores≥4` citeturn4search0turn12search8 | {数小时–1天} | CPU 内存 {16–64GB}；显存：unspecified（一般不需） |
| 高 | 一致性统计与图 | 把稳健性量化呈现 | Pearson/Spearman/CCC/Bland–Altman | {1–6小时} | 低 |
| 中 | 敏感性分析 | 证明关键结论不依赖单一阈值 | 改动 `{UMI_min/UMI_max/gene_cutoff}` 2–3 组重跑 | {0.5–1天} | 中 |
| 中 | 区域/生态位稳健性 | 用不同分区/阈值检验趋势 | 轻量分区策略 + 复算区域均值/差异方向 | {数小时} | 低 |
| 可选 | Kraken2 复核 | 对少量样本做第二证据链 | 最小 DB + 抽样 reads | {数小时} | CPU 内存：unspecified（与 DB 大小相关） citeturn0search0 |

**轻量化工具/参数建议（明确写入补充材料）**  
- 物种判定优先 minimap2（数据库小、解释直观）；Kraken2 仅作为抽样复核，且使用最小 human+mouse DB。 citeturn3search0turn0search0  
- 使用处理后数据包（`GSE269875_RAW.tar`）完成主分析，原始 reads 仅用于物种 QC（避免把“下载/展开”变成项目瓶颈）。 citeturn1search0turn2search0  
- `fasterq-dump` 明确指定 `--temp` 与输出盘分离，并使用 `--size-check`/`--disk-limit` 防止磁盘不足失败。 citeturn2search0  

---

## 修订后的 Results/Discussion 提纲、图表脚本与红线自检清单

### Results 建议提纲（每节首句都强调 human mainline 与假设生成边界）

**Results 章节开场句（可直接粘贴）**  
> 我们首先对 GSE269875 进行物种来源拆分与可追溯质量控制，仅保留经元数据与序列层面一致确认的人类空间样本作为主分析主线（human mainline），以避免跨物种混杂对下游推断造成偏差。 citeturn1search0turn3search0  

**Results 小节骨架（用占位符 `{}` 填入你真实发现；不写任何虚构数字）**  
- 数据治理与物种拆分结果：human mainline `{n}`、mouse `{m}`、剔除/ambiguous `{k}`，并引用 `sample_manifest.tsv` 与 `species_filter_log.md`。 citeturn1search0  
- 参考构建（GSE223060）：说明其为人类 scRNA 数据（GPL20301；HiSeq 4000），用于构建细胞类型参考表达谱，不作为配对验证。 citeturn4search5turn12search6  
- 空间解卷积主结果（human mainline）：呈现关键细胞类型在空间中的候选分布/梯度趋势（仅描述“模式/趋势”，避免因果）。  
- 基线一致性验证（主方法 vs RCTD）：报告 Pearson/Spearman/CCC/Bland–Altman 的 `{}` 结果，并说明只保留跨方法一致结论。 citeturn4search4turn3search7turn4search0  
- 跨数据集一致性观察（趋势支持而非验证）：明确两数据集非同批，所有跨集结论为假设生成证据。 citeturn1search0turn4search5  

### Discussion 建议提纲（第一段先降调，主动承认边界）

**Discussion 第一段（可直接粘贴）**  
> 本研究通过整合公开单细胞与空间转录组数据，构建了可复现的数据治理、空间细胞组成推断与稳健性评估流程，并提出与多发性骨髓瘤骨髓微环境相关的候选空间生态位与分子线索。鉴于缺乏配对同批队列与湿实验验证，我们将跨数据集结果解释为趋势支持与假设生成证据；对于在不同算法间不一致的发现，我们采取保守解释，仅保留稳健一致的结论。 citeturn1search0turn0search1turn4search0  

**Discussion 必须包含的三个模块**  
- 主要发现（仅限“空间模式/候选线索/可检验假设”）  
- 稳健性证据链（强调“主方法 + RCTD baseline + 一致性统计”） citeturn0search1turn3search7turn4search4  
- 局限性与未来工作（非配对同批、无湿实验、算力限制；提出下一步实验验证建议）

### 推荐图表与脚本清单（用于补充材料与可复现交付）

**主文推荐图（控制在 5–7 张）**  
- 图：整体流程图（包含物种拆分）  
- 图：human mainline 的空间 QC 概览（reads/UMI/基因数阈值与过滤后分布）  
- 图：主方法解卷积空间图（关键细胞类型 `{}`）  
- 图：主方法 vs RCTD 一致性（散点 + Bland–Altman） citeturn3search7  
- 图：空间并排图（同切片主方法 vs RCTD）  

**补充表**  
- 表：物种/组织/批次样本计数表（模板见上）  
- 表：一致性汇总表（模板见上）  
- 表：剔除/ambiguous 样本清单与证据文件路径（来自 `species_filter_log.md`）

**脚本文件建议（按执行顺序命名，便于 reviewer 复现）**  
- `01_fetch_geo_metadata.sh`（FTP 下载 matrix/soft；或构造 URL 拉 full text） citeturn10search0turn3search2  
- `02_parse_geo_metadata.py`（生成 `sample_manifest.tsv`）  
- `03_fetch_sra_fastq.sh`（prefetch + fasterq-dump；磁盘保护参数） citeturn2search0  
- `04_species_assignment_minimap2.sh`（hg38 vs mm10 双比对 + 阈值判定） citeturn3search0  
- `05_run_main_deconv.{py|R}`（你的主方法）  
- `06_run_rctd_baseline.R`（spacexr RCTD baseline） citeturn4search0turn12search1  
- `07_concordance_metrics.py`（Pearson/Spearman/CCC/Bland–Altman + 作图） citeturn4search4turn3search7  
- `08_make_tables.R`（输出主文表格与 supplement 表格）

### Mermaid 流程图（主文或补充材料直接粘贴）

```mermaid
flowchart TD
  A[下载公开数据<br/>GSE269875 / GSE223060] --> B[解析GEO元数据<br/>Series Matrix + family SOFT]
  B --> C[生成样本清单 sample_manifest.tsv<br/>提取 organism/platform/technique/批次字段]
  C --> D{GSE269875 是否包含多物种?}
  D -->|是| E[按元数据初筛<br/>human候选主线 vs mouse隔离]
  E --> F[序列级物种QC<br/>minimap2( hg38 vs mm10 )<br/>或 Kraken2 最小DB]
  F --> G[输出：species_filter_log.md<br/>剔除 ambiguous/不一致样本]
  G --> H[定义 human mainline 数据集<br/>仅人类样本进入主链]
  H --> I[构建 scRNA 参考<br/>基于 GSE223060]
  I --> J[空间解卷积：主方法]
  I --> K[空间解卷积：基线 RCTD/spacexr]
  J --> L[一致性评估<br/>Pearson/Spearman/CCC/Bland–Altman]
  K --> L
  L --> M[稳健结论汇总<br/>仅保留跨方法一致结果]
  M --> N[论文表述落地：<br/>公共数据库整合 + 假设生成<br/>明确非配对同批/无湿实验/算力限制]
```

### 终稿红线自检清单（投稿前必须逐条过一遍）

- [ ] 全稿研究定位为“公共数据库整合分析 + 假设生成”；不出现“强验证/严格外部验证/机制闭环证明”等表述。 citeturn1search0turn4search5  
- [ ] GSE269875 在进入任何主分析前已完成物种拆分；主文所有结果均明确为 **human mainline**；mouse 不混写、不混图、不混统计。 citeturn1search0  
- [ ] 明确写出并展示 GSE223060 与 GSE269875 非配对/非同批的证据链（时间、平台、仪器、处理流程、样本 ID）。 citeturn1search0turn4search5turn12search6  
- [ ] 空间解卷积包含至少一个成熟 baseline（RCTD/spacexr）并给出一致性量化与 Bland–Altman 图。 citeturn0search1turn4search0turn3search7  
- [ ] **Stage 3（m6A integration）完全删除**：正文、补充、图表、脚本、文件名均无残留。  
- [ ] **Nanopore 完全删除**：正文、补充、图表、脚本、文件名均无残留（无 “Nanopore/ONT/FAST5/long-read” 等字样）。  
- [ ] 明确写出“无湿实验验证”的结论边界；明确写出“单卡 50–60 系列 GPU（显存/算力 unspecified）”导致的方法学取舍（不做大规模超参搜索与超大模型训练）。 citeturn2search0  

以上即为“第三阶段终止后”的**重写版可投稿骨架 + 可复现证据链 + reviewer 友好措辞包**。你如果希望我把它进一步“变成一篇完整的可直接投稿正文（含 Methods/Results/Discussion 连贯段落）”，请把你现有主方法名称与已有结果的关键要点（只需文字描述，不必给数值）发我，我会在不虚构任何数值的前提下，用 `{}` 占位符把全文润色成提交版。