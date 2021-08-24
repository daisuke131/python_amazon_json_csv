import os

import gspread
import gspread_formatting as gf
from gspread.models import Spreadsheet, Worksheet
from gspread_dataframe import set_with_dataframe
from oauth2client.service_account import ServiceAccountCredentials
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

JSON_PATH = os.path.join(os.getcwd(), "python-amazon-asin-8e6042541047.json")
FOLDER_KEY = "13DcAIECh93BoqvMTWQK1jRQ6b8zhALpm"


class SpreadSheetNew:
    def __init__(self, file_name: str) -> None:
        self.wb: Spreadsheet
        self.ws: Worksheet
        self.set_spread_sheet(file_name)

    def set_spread_sheet(self, file_name: str):
        scope = [
            "https://spreadsheets.google.com/feeds",
            "https://www.googleapis.com/auth/drive",
        ]

        scope = [
            "https://spreadsheets.google.com/feeds",
            "https://www.googleapis.com/auth/drive",
        ]
        credentials = ServiceAccountCredentials.from_json_keyfile_name(JSON_PATH, scope)

        gauth = GoogleAuth()
        gauth.credentials = credentials
        drive = GoogleDrive(gauth)

        f = drive.CreateFile(
            {
                "title": file_name,
                "mimeType": "application/vnd.google-apps.spreadsheet",
                "parents": [{"id": FOLDER_KEY}],
            }
        )
        f.Upload()

        gc = gspread.authorize(credentials)
        self.wb = gc.open_by_key(f["id"])
        self.ws = self.wb.sheet1

    def update_cell(self, row, col, val):
        self.ws.update_cell(row, col, val)

    def df_write(self, df):
        set_with_dataframe(self.ws, df)
        # 左寄せ、高さ真ん中
        fmt = gf.cellFormat(
            horizontalAlignment="LEFT",
            verticalAlignment="MIDDLE",
        )
        gf.format_cell_range(self.ws, "A2:H101", fmt)
        # 行高さ
        gf.set_row_height(self.ws, "2:101", 100)
