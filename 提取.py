import os
import pandas as pd
import GEOparse

# 1. 设定你的工作路径
base_path = r'D:\二区'
os.chdir(base_path)

# 2. 检查你下载的是哪个文件
soft_file = 'GSE269875_family.soft.gz'
matrix_file = 'GSE269875_series_matrix.txt.gz'


def create_manifest(gse):
    print("正在提取元数据并根据研究计划分类...")
    metadata_list = []
    for gsm_name, gsm in gse.gsms.items():
        metadata_list.append({
            "GSM": gsm_name,
            "sample_title": gsm.metadata.get('title', [''])[0],
            "species_geo": gsm.metadata.get('organism_ch1', [''])[0],
            "platform": gsm.metadata.get('platform_id', [''])[0],
            "tissue": gsm.metadata.get('source_name_ch1', [''])[0]
        })

    df = pd.DataFrame(metadata_list)

    # 严格遵循修订稿要求：
    # Human Mainline (主线): Homo sapiens + GPL30173
    # Mouse Supplement (补充): Mus musculus + GPL30172
    df['include_mainline'] = (df['species_geo'] == 'Homo sapiens') & (df['platform'] == 'GPL30173')

    output_file = 'sample_manifest.tsv'
    df.to_csv(output_file, sep="\t", index=False)

    print("-" * 30)
    print(f"成功！作战地图已生成: {os.path.join(base_path, output_file)}")
    print(f"人类主线样本数 (Human Mainline): {df['include_mainline'].sum()}")
    print(f"小鼠补充样本数 (Mouse Supplement): {len(df) - df['include_mainline'].sum()}")
    return df


# 3. 优先尝试解析 SOFT 文件
if os.path.exists(soft_file):
    print(f"检测到本地 SOFT 文件，正在解析: {soft_file}")
    gse = GEOparse.get_GEO(filepath=soft_file)
    create_manifest(gse)
elif os.path.exists(matrix_file):
    print(f"检测到本地 Matrix 文件，正在解析: {matrix_file}")
    # 注意：Matrix 文件的解析逻辑略有不同，若需使用请告知
    print("建议优先使用 SOFT 文件以获得完整元数据。")
else:
    print("错误：在 D:\二区 没找到下载好的 .gz 文件，请检查文件名！")