from dataclasses import dataclass
from functools import cached_property
from src import cache
import tabula

COUNTIES = [
    'Passaic',
    'Bergen',
    'Hudson',
    'Essex',
    'Union',
    'Middlesex',
    'Monmouth',
    'Sussex',
    'Morris',
    'Somerset',
    'Ocean',
    'Warren',
    'Hunterdon',
    'Mercer',
    'Burlington',
    'Camden',
    'Gloucester',
    'Salem',
    'Cumberland',
    'Cape May',
    'Alantic'
]

@dataclass
class Dialects:
    pdf_path: str = "../data/NJ_dialects_coye2009.pdf"

    @staticmethod
    def process(df):
        df = df.loc[df["COUNTY"].isin(COUNTIES)].reset_index(drop=True)
        df["COUNTY"] = df["COUNTY"].str.upper()
        for col in df.columns:
            if col != "COUNTY":
                df[col] = df[col].astype(int)
        df["COUNTY"] = df["COUNTY"].str.replace("ALANTIC","ATLANTIC")
        return df

    @cached_property
    @cache.localcache()
    def calm(self):
        df = tabula.read_pdf(self.pdf_path, pages='16', area=[138,81,444,402], columns=[174, 210, 243, 294, 336, 366])[0]
        df.columns = ["COUNTY", "calm-no-l", "calm-with-l", "calm-cant-tell", "almond-no-l", "almond-with-l", "almond-cant-tell"]
        df = self.process(df)
        df["calm-total"] = df[["calm-no-l", "calm-with-l"]].sum(axis=1)
        df["almond-total"] = df[["almond-no-l", "almond-with-l"]].sum(axis=1)
        df["calm-no-l"] = 100*(df["calm-no-l"] / df["calm-total"])
        df["almond-no-l"] = 100*(df["almond-no-l"] / df["almond-total"])
        return df[["COUNTY","calm-no-l","almond-no-l"]]

    @cached_property
    @cache.localcache()
    def draw(self):
        df = tabula.read_pdf(self.pdf_path, pages='17', area=[114,240,432,432], columns=[336,372,408])[0]
        df.columns=["COUNTY", "drawer", "draw", "both"]
        df = self.process(df)
        df["drawer"] = 100*(df["drawer"] / (df["drawer"] + df["draw"]))
        return df[["COUNTY", "drawer"]]

    @cached_property
    @cache.localcache()
    def forward(self):
        df = tabula.read_pdf(self.pdf_path, pages='18', area=[114,212,432,432], columns=[308,342,381])[0]
        df.columns=["COUNTY", "forward-no-r", "forward-with-r", "both"]
        df = self.process(df)
        df["forward-no-r"] = 100*(df["forward-no-r"] / (df["forward-no-r"] + df["forward-with-r"]))
        return df[["COUNTY", "forward-no-r"]]

    @cached_property
    @cache.localcache()
    def gone(self):
        df = tabula.read_pdf(self.pdf_path, pages='19', area=[162,254,450,420], columns=[349,390])[0]
        df.columns=["COUNTY", "gone-don", "gone-dawn"]
        df = self.process(df)
        df["gone-don"] = 100*(df["gone-don"] / (df["gone-don"] + df["gone-dawn"]))
        return df[["COUNTY", "gone-don"]]
