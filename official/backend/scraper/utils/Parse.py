from scrapy import Selector
import pandas as pd

class Parse:
    __links_locator = "//div[contains(@class,'search-marvel-srp')]//div[contains(@class,'display-flex align-items-center')]/a/@href"
    
    __education_date = "//div[@data-component-type = 'LazyColumn']//a[contains(@href, '/school/')]/div/p/text()"
    __education_school = "//div[@data-component-type = 'LazyColumn']//a[contains(@href, '/school/')]/div/div/div/p[0]/text()"
    __education_degree = "//div[@data-component-type = 'LazyColumn']//a[contains(@href, '/school/')]/div/div/div/p[1]/text()"


    def search(self, html):
        sel = Selector(text = html)
        links = sel.xpath(self.__links_locator).extract()
        links = pd.DataFrame(
            {
                "links" : links
            }
        )
        links = links["links"].str.extract(r'(h[^?]*)')
        return links
    
    def education(self, html):
        sel = Selector(text = html)
        date = sel.xpath(self.__education_date).extract()
        school = sel.xpath(self.__education_school).extract()
        degree = sel.xpath(self.__education_degree).extract()
        print(date)
        print(school)
        print(degree)
        return None
    



# with open("file.html", "r", encoding="utf-8") as file:
#     html = file.read()


# print(html)

# pr = Parse()
# links = pr.search(html)
# print(links)