import os
import requests
import zipfile
import shutil

def download_paracrawl_data(output_dir):
    # 创建输出目录
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 下载ParaCrawl数据
    url = "https://s3.amazonaws.com/web-language-models/paracrawl/release4/paracrawl-release4.en-zh.tsv.gz"
    filename = os.path.join(output_dir, "paracrawl-release4.en-zh.tsv.gz")
    print("Downloading ParaCrawl data...")
    response = requests.get(url, stream=True)
    with open(filename, "wb") as file:
        shutil.copyfileobj(response.raw, file)

    # 解压缩数据文件
    print("Extracting data...")
    with gzip.open(filename, 'rb') as f_in:
        with open(filename[:-3], 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)

    # 删除压缩文件
    os.remove(filename)

    print("Data downloaded and extracted successfully.")

# 定义保存文件的目录
output_dir = "paracrawl_data"

# 下载和处理数据
download_paracrawl_data(output_dir)

# 读取数据并保存到txt文件
input_file = os.path.join(output_dir, "paracrawl-release4.en-zh.tsv")
output_file = "paracrawl_data.txt"

print("Processing data...")
with open(input_file, "r", encoding="utf-8") as f_in, open(output_file, "w", encoding="utf-8") as f_out:
    for line in f_in:
        en_sentence, zh_sentence, _ = line.strip().split("\t")
        f_out.write(f"{zh_sentence}\t{en_sentence}\n")

print("Data processing complete. Saved to paracrawl_data.txt.")

