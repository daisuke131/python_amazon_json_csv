# import os
# from concurrent.futures import ThreadPoolExecutor
# from time import sleep

import re

import pandas as pd

from common.beutifulsoup import Soup

# from common.driver import Driver
# from common.spread_sheet import SpreadSheetNew
# from common.util import filename_creation

# from dotenv import load_dotenv


# THREAD_COUNT = None  # スレッド数Noneで自動
# PG2_QUERY = "/ref=zg_bs_pg_2?ie=UTF8&pg=2"
# load_dotenv()
# LOGIN_ID = os.getenv("LOGIN_ID")
# PASSWORD = os.getenv("PASSWORD")


class Scraping:
    def __init__(self, url: str) -> None:
        self.df = pd.DataFrame()
        self.url: str = url

    def scraping(self) -> None:
        soup = Soup(self.url)
        self.df = self.df.append(
            {
                "product_name": self.fetch_product_name(soup).strip(),
                "price": self.fetch_prise(soup).strip(),
                "asin": self.fetch_asin(soup),
                "about_this_product": self.fetch_about_this_product(soup).strip(),
                "point": self.fetch_point(soup),
                "variation": self.fetch_variation(soup),
                "brand_name": self.fetch_brand_name(soup),
                "regist_info": self.fetch_regist_info(soup),
                "detailed_info": self.fetch_detailed_info(soup),
                "image_url": self.fetch_image(soup),
            }
        )

    def fetch_product_name(self, soup) -> str:
        try:
            product_name = soup.select("#productTitle").text
        except Exception:
            product_name = "失敗"
        return product_name

    def fetch_prise(self, soup) -> str:
        price = "-"
        try:
            if soup.selects("#priceblock_ourprice"):
                price = soup.select("#priceblock_ourprice").text
            elif soup.selects("#priceblock_dealprice"):
                price = soup.select("#priceblock_dealprice").text
            elif soup.selects("#priceblock_saleprice"):
                price = soup.select("#priceblock_saleprice").text
            elif soup.selects("#availability > span.a-size-medium.a-color-price"):
                price = soup.select(
                    "#availability > span.a-size-medium.a-color-price"
                ).text
            elif soup.selects(".a-size-base.a-color-price"):
                price = soup.select(".a-size-base.a-color-price").text
            else:
                price = "失敗"
        except Exception:
            price = "失敗"
        finally:
            return price

    def fetch_asin(self, soup) -> str:
        try:
            asin = soup.select("#ASIN")["value"]
        except Exception:
            asin = "失敗"
        finally:
            return asin

    def fetch_about_this_product(self, soup) -> str:
        try:
            about = ""
            elements = soup.selects("#feature-bullets > ul > li")
            for i, a in enumerate(elements):
                if i != 0:
                    about += f"・{a.get_text().strip()}\n"
            elements = soup.selects("#feature-bullets > div > div > ul > li")
            for i, a in enumerate(elements):
                about += f"・{a.get_text().strip()}\n"
        except Exception:
            about = "失敗"
        finally:
            return about

    def fetch_point(self, soup) -> str:
        try:
            point = soup.select(
                ".a-span12.a-color-secondary.a-size-base > span"
            ).get_text()
            point = re.search(r"\d+", point).group()
        except Exception:
            point = ""
        finally:
            return point

    def fetch_variation(self, soup) -> str:
        try:
            variation = ""
            # サイズ
            elements = soup.selects(".dropdownAvailable")
            for v in elements:
                variation += f"・{v.get_text().strip()}\n"
            # 色
            elements = soup.selects("#variation_color_name > ul > li")
            for v in elements:
                variation += f'・{v["title"].replace("を選択するにはクリックしてください","")}\n'
                v["data-defaultasin"]
                v["data-dp-url"]
            # スタイル
            elements = soup.selects("#variation_style_name > ul > li")
            for v in elements:
                variation += f'・{v["title"].replace("を選択するにはクリックしてください","")}\n'
                v["data-defaultasin"]
                v["data-dp-url"]
        except Exception:
            variation = ""
        finally:
            return variation

    def fetch_brand_name(self, soup) -> str:
        try:
            elements = soup.selects(
                "#productOverview_feature_div > div > table > tr > td > span"
            )
            get_flg = 0
            for el in elements:
                if el.get_text() == "ブランド":
                    get_flg = 1
                if get_flg:
                    brand_name = el.get_text()
                    break
        except Exception:
            brand_name = ""
        finally:
            return brand_name

    def fetch_regist_info(self, soup) -> str:
        try:
            elements = soup.selects("#detailBullets_feature_div > ul > li")
        except Exception:
            regist_info = ""
        finally:
            return regist_info

    def fetch_image(self, soup) -> str:
        try:
            img_url = soup.select("#landingImage").get("src")
        except Exception:
            img_url = "失敗"
        finally:
            return img_url


def main():
    url = input("URL入力:")
    my_scraping = Scraping(url)
    my_scraping.scraping()


if __name__ == "__main__":
    main()
