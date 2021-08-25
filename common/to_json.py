import json
import os
import pprint
from pathlib import Path

dir = Path("./json")
dir.mkdir(parents=True, exist_ok=True)
JSON_FILE_PATH = os.path.join(os.getcwd(), "json/{file_name}.json")
JSON_FOLDER_PATH = os.path.join(os.getcwd(), "json")


def write_json(file_name: str, dic: dict):
    json_path = JSON_FILE_PATH.format(file_name=file_name)
    pprint.pprint(json.dumps(dic, indent=4, ensure_ascii=False))
    with open(json_path, "w") as f:
        json.dump(dic, f, indent=4, ensure_ascii=False)
