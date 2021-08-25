import os

# import subprocess
from pathlib import Path

dir = Path("./csv")
dir.mkdir(parents=True, exist_ok=True)
CSV_FILE_PATH = os.path.join(os.getcwd(), "csv/{file_name}.csv")
CSV_FOLDER_PATH = os.path.join(os.getcwd(), "csv")


# CSV書き込み
def write_csv(file_name: str, df):
    # csvファイル名に検索ワードを加える。
    csv_path = CSV_FILE_PATH.format(file_name=file_name)
    # 行番号なしで出力
    df.to_csv(csv_path, index=False, encoding="utf-8-sig")
    # 保存フォルダ開く
    # subprocess.Popen(["explorer", CSV_FOLDER_PATH], shell=True)
    # subprocess.Popen(["start", csv_path], shell=True)
