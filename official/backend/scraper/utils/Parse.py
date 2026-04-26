from scrapy import Selector
import pandas as pd

class Parse:

    __links_xpath = "//div[contains(@class,'search-marvel-srp')]//div[contains(@class,'display-flex align-items-center')]/a/@href"
    
    __education_xpath = "//div[@data-component-type = 'LazyColumn']//div[contains(@componentkey,'entity-collection-item')]"

    __education_xpath = {
        "block" : "//div[@data-component-type = 'LazyColumn']//div[contains(@componentkey,'entity-collection-item')]",

        "school" : ".//a[contains(@href, 'https://www.linkedin.com/school/')]/div/div/div/p[1]/text()",
        "degree" : ".//a[contains(@href, 'https://www.linkedin.com/school/')]/div/div/div/p[2]/text()",
        "date"   : ".//a[contains(@href, 'https://www.linkedin.com/school/')]/div/p/text()"

    }

    def search(self, html):
        sel = Selector(text = html)
        links = sel.xpath(self.__links_xpath).extract()
        links = pd.DataFrame({  "links" : links  })
        links = links["links"].str.extract(r'(h[^?]*)')
        return links
    
    def education(self, html):
        sel = Selector(text = html)
        blocks = sel.xpath(self.__education_xpath["block"])
        rows = []

        for block in blocks:
            school = block.xpath(self.__education_xpath["school"]).get()
            degree = block.xpath(self.__education_xpath["degree"]).get()
            date = block.xpath(self.__education_xpath["date"]).get()

            row = {
                "school" : school if school != None else None,
                "degree" : degree if degree != None else None,
                "date"   : date   if date   != None else None
            }
            rows.append(row)

        df = pd.DataFrame(rows, columns=["date", "school", "degree"])
        df = df.drop_duplicates()
        df = df.dropna(how="all") 
        return df
    
