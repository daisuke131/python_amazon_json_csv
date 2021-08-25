import re

from common.beutifulsoup import Soup
from common.to_csv import write_csv
from common.to_json import write_json
from common.util import filename_creation

# import pandas as pd


class Scraping:
    def __init__(self, url: str) -> None:
        # self.df = pd.DataFrame()
        self.dic = dict()
        self.csv_title: str = url
        self.url: str = url

    def scraping(self) -> None:
        soup = Soup(self.url)
        # self.df = self.df.append(
        #     {
        #         "product_name": self.fetch_product_name(soup),
        #         "price": self.fetch_prise(soup),
        #         "asin": self.fetch_asin(soup),
        #         "about_this_product": self.fetch_about_this_product(soup),
        #         "point": self.fetch_point(soup),
        #         "variation": self.fetch_variation(soup),
        #         "brand_name": self.fetch_brand_name(soup),
        #         "regist_info": self.fetch_regist_info(soup),
        #         "detailed_info": self.fetch_detailed_info(soup),
        #         "image_url": self.fetch_image(soup),
        #     },
        #     ignore_index=True,
        # )
        self.dic["product_name"] = self.fetch_product_name(soup)
        self.dic["price"] = self.fetch_prise(soup)
        self.dic["asin"] = self.fetch_asin(soup)
        self.dic["about_this_product"] = self.fetch_about_this_product(soup)
        self.dic["point"] = self.fetch_point(soup)
        self.dic["variation"] = self.fetch_variation(soup)
        self.dic["brand_name"] = self.fetch_brand_name(soup)
        self.dic["regist_info"] = self.fetch_regist_info(soup)
        self.dic["detailed_info"] = self.fetch_detailed_info(soup)
        self.dic["image_url"] = self.fetch_image(soup)

    def fetch_product_name(self, soup) -> str:
        try:
            product_name = soup.select("#productTitle").text.strip()
            self.csv_title = product_name
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
            return price.strip()

    def fetch_asin(self, soup) -> str:
        try:
            asin = soup.select("#ASIN")["value"]
        except Exception:
            asin = "失敗"
        finally:
            return asin

    def fetch_about_this_product(self, soup) -> str:
        abouts = []
        try:
            elements = soup.selects("#feature-bullets > ul > li > span.a-list-item")
            for el in elements:
                abouts.append(el.get_text().strip())
            # 表示件数を増やす以降
            elements = soup.selects("#feature-bullets > div > div > ul > li")
            for i, el in enumerate(elements):
                abouts.append(el.get_text().strip())
        except Exception:
            abouts = "失敗"
        finally:
            return abouts

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
        variations: dict = {}
        try:
            sizes = self.fetch_size(soup)
            colors = self.fetch_color(soup)
            styles = self.fetch_style(soup)
            if sizes:
                variations["size"] = sizes
            if colors:
                variations["color"] = colors
            if styles:
                variations["style"] = styles
        except Exception:
            pass
        finally:
            return variations

    def fetch_size(self, soup):
        sizes = []
        try:
            elements = soup.selects(".dropdownAvailable")
            for el in elements:
                sizes.append(el.get_text().strip())
        except Exception:
            pass
        finally:
            return sizes

    def fetch_color(self, soup):
        colors = []
        try:
            elements = soup.selects("#variation_color_name > ul > li")
            for el in elements:
                colors.append(el["title"].replace("を選択するにはクリックしてください", ""))
                el["data-defaultasin"]
                el["data-dp-url"]
        except Exception:
            pass
        finally:
            return colors

    def fetch_style(self, soup):
        styles = []
        try:
            elements = soup.selects("#variation_style_name > ul > li")
            for el in elements:
                styles.append(el["title"].replace("を選択するにはクリックしてください", ""))
                el["data-defaultasin"]
                el["data-dp-url"]
        except Exception:
            pass
        finally:
            return styles

    def fetch_brand_name(self, soup) -> str:
        brand_name = ""
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
            pass
        finally:
            return brand_name

    def fetch_regist_info(self, soup) -> str:
        regist_infos = []
        try:
            elements = soup.selects("#detailBullets_feature_div > ul > li")
            for el in elements:
                regist_infos.append(
                    el.get_text()
                    .replace("\n\u200f\n", " ")
                    .replace("\n\u200e\n\n", " ")
                    .strip()
                )
            elements = soup.selects("#productDetails_detailBullets_sections1 > tr")
            for el in elements:
                regist_infos.append(
                    f'{el.select("th")[0].text.strip()}：'
                    + f'{el.select("td")[0].text.strip()}'
                )

        except Exception:
            pass
        finally:
            return regist_infos

    def fetch_detailed_info(self, soup) -> str:
        detailed_infos = []
        try:
            elements = soup.selects("#productDetails_techSpec_section_1 > tr")
            for el in elements:
                td = el.select("td")[0].text.replace("\u200e", "").strip()
                detailed_infos.append(f'{el.select("th")[0].text.strip()}：{td}')
        except Exception:
            pass
        finally:
            return detailed_infos

    def fetch_image(self, soup) -> str:
        try:
            img_url = soup.select("#landingImage").get("src")
        except Exception:
            img_url = "失敗"
        finally:
            return img_url

    def to_csv(self):
        write_csv(filename_creation("csv"), self.dic)

    def to_json(self):
        write_json(filename_creation("json"), self.dic)


def main():
    url = input("URL入力:")
    my_scraping = Scraping(url)
    my_scraping.scraping()
    # my_scraping.to_csv()
    my_scraping.to_json()


if __name__ == "__main__":
    main()
