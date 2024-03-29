# %%
import censusdata
from functools import cached_property
from src import cache
import geopandas as gpd
import requests
import yaml
import time
import tqdm
import json
import pandas as pd
from dataclasses import dataclass
from pathlib import Path
import glob

@dataclass
class CensusCentroids:

    # Load the census tract data for New Jersey
    @cached_property
    def longlats(self):
        df = gpd.read_file("../data/tl_2018_34_tract/tl_2018_34_tract.shp")
        return [
            f"{y},{x}"
            for x,y in 
            zip(df.geometry.centroid.x,df.geometry.centroid.y)
        ]

@dataclass
class Foursquare(CensusCentroids):
    company:str = "wawa"

    @property
    def company_id(self):
        return {
            "wawa":"2cb519f8-883c-4263-860a-cd83325fbb97",
            "dunkin":"2cb519f8-883c-4263-860a-cd83325fbb97"
        }
    
    @cached_property
    def auth(self):
        with open("../secrets.yaml", "r") as file:
            return yaml.load(file, Loader=yaml.FullLoader)["FOURSQUARE"]
        
    @property
    def headers(self):
        return {
            'Authorization': self.auth,
            'accept': "application/json"
        }

    def querystring(self, longlat):
        return {
            "chains":self.company_id[self.company],
            "ll":longlat,
            'radius':100_000,
            "limit":50,
            "sort":"DISTANCE"
        }

    def query(self, longlat):
        url = "https://api.foursquare.com/v3/places/search"
        response = requests.request(
            "GET", url, 
            headers=self.headers, 
            params=self.querystring(longlat)
        )
        return response.json()

    def save(self):
        for i,x in tqdm.tqdm(enumerate(self.longlats)):
            result = self.query(
                longlat=x
            )
            out = f"../data/{self.company}/{i}.json"
            if Path(out).exists():
                continue
            else:
                with open(out, "w") as f:
                    json.dump(result, f)
                time.sleep(0.25)

    def get_df(self):
        files = glob.glob(f"../data/{self.company}/*.json")
        df_files = []
        for file in files:
            with open(file, "r") as f:
                df_files.append(json.load(f))

        df = pd.DataFrame([
            (
                res["fsq_id"],
                res["location"]["census_block"][2:5],
                res["location"]["census_block"][5:11]
            )
            for f in df_files
            for res in f["results"]
        ], columns=[
            f"{self.company}_id",
            f"{self.company}_county",
            f"{self.company}_tract",
        ])
        return df.drop_duplicates(subset=f"{self.company}_id")

    @cached_property
    @cache.localcache(dtype={"dunkin_tract":str,"dunkin_county":str})
    def df_dunkins(self):
        return self.get_df()

    @cached_property
    @cache.localcache(dtype={"wawa_tract":str,"wawa_county":str})
    def df_wawas(self):
        return self.get_df()

    @cached_property
    def df_dunkins_tract(self):
        return(
            self.df_dunkins
            .groupby(["dunkin_county","dunkin_tract"])
            .agg({
                "dunkin_id":"count"
            })
            .reset_index()
        )

    @cached_property
    def df_wawa_tract(self):
        return(
            self.df_wawas
            .groupby(["wawa_county","wawa_tract"])
            .agg({
                "wawa_id":"count"
            })
            .reset_index()
        )

    @cached_property
    def df_dunkins_county(self):
        return(
            self.df_dunkins
            .groupby("dunkin_county")
            .agg({
                "dunkin_id":"count"
            })
            .reset_index()
        )

    @cached_property
    def df_wawa_county(self):
        return(
            self.df_wawas
            .groupby("wawa_county")
            .agg({
                "wawa_id":"count"
            })
            .reset_index()
        )
