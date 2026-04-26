from datetime import datetime
import re
from scrapy import Selector
import pandas as pd
from pymongo import MongoClient

class Parse:

    __links_xpath     = "//div[contains(@class,'search-marvel-srp')]//div[contains(@class,'display-flex align-items-center')]/a/@href"
    
    __education_xpath = {
        "block" : "//div[@data-component-type = 'LazyColumn']//div[contains(@componentkey,'entity-collection-item')]",

        "school" : ".//a[contains(@href, 'https://www.linkedin.com/school/')]/div/div/div/p[1]/text()",
        "degree" : ".//a[contains(@href, 'https://www.linkedin.com/school/')]/div/div/div/p[2]/text()",
        "date"   : ".//a[contains(@href, 'https://www.linkedin.com/school/')]/div/p/text()"

    }

    def __init__(self):
        self.client = MongoClient("mongodb://localhost:27017/")
        self.collection = self.client["industry_analytics"]["people"]

    def __del__(self):
        if self.client:
            self.client.close()

    def get_links(self, html):
        sel   = Selector(text=html)
        links = sel.xpath(self.__links_xpath).extract()
        links = [m.group(1) for l in links if (m := re.search(r'(h[^?]*)', l))]
        return links
    
    def get_education(self, html, url):
        sel     = Selector(text = html)
        blocks  = sel.xpath(self.__education_xpath["block"])
        records = []

        for block in blocks:
            school = block.xpath(self.__education_xpath["school"]).get()
            degree = block.xpath(self.__education_xpath["degree"]).get()
            date   = block.xpath(self.__education_xpath["date"]).get()


            education_records = {
                "school" : school ,
                "degree" : degree ,
                "date"   : date   
            }
            records.append(education_records)

        education_records = pd.DataFrame(records, columns=["date", "school", "degree"])
        education_records = education_records.drop_duplicates()
        education_records = education_records.dropna(how="all") 
        education_records = education_records.to_dict(orient="records")

        self.__store_education(education_records, url)

        return None
    
    def __store_education(self, education_records, person_url):
        
        self.collection.update_one(
            {"url": person_url},                       
            {"$set": {"education": education_records}}, 
            upsert=True                               
        )