from scrapy import Selector
import pandas as pd

class Parse:
    __links_locator = "//div[@class='faZGYvqMtLqiMGnJErRsQeHoDBLViDlg']/div[@class='display-flex align-items-center']/a[@class='WKVSfLCavKyjywFEXwZDFLAfdDosdiAqrY  scale-down ']/@href"
    
    __data_locator = None

    def search(self, html):
        sel = Selector(text = html)
        links = sel.xpath(self.__links_locator).extract()
        links = pd.DataFrame(links)
        return links
    
    def profile(self, html):
        sel = Selector(text = html)
        data = sel.xpath(self.__data_locator).extract()
        data = pd.DataFrame(data)
        return data
    


with open("/home/muhammad/Downloads/index_1.html", 'r') as file:
    html = file.read()
parse = Parse()
df = pd.DataFrame(parse.search(html))
print(df)

