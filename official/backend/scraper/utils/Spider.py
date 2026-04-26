import utils.Request as req
import utils.Parse   as par

class Spider:

    __addons = [
        "/details/education",
        "/details/experience",
        "/details/certifications"
    ]

    def __init__(self):
        self.parser  = par.Parse()
        self.request = None

    async def __aenter__(self):
        self.request = req.Request()
        await self.request.__aenter__()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.request.__aexit__(exc_type, exc_val, exc_tb)

    async def collect_links(self, keyword, pages):
        links = []
        search_pages = await self.request.search_to_html(keyword, pages)
        for page in search_pages:
            link = self.parser.get_links(page)
            links.extend(link)
            
        return links
            
    async def collect_education(self, links):
        for link in links:
            html = await self.request.link_to_html(link + self.__addons[0])
            if html:
                self.parser.get_education(html, link)
            else:
                print(f"[Skip] Failed to fetch: {link}")


