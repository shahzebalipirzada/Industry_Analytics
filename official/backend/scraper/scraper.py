import utils.Request as req
import utils.Parse as parse

import asyncio

res = req.Request()
pr =  parse.Parse()

addons = ["\details\education","\details\experience","\details\certifications"]
# html_contents = asyncio.run(res.search_to_html("Sukkur IBA University",1))


# for i in html_contents:
#     data = pr.search(i)
#     print(data.to_string())
link = "https://www.linkedin.com/in/mrshaikhmuhammad"

education_html = asyncio.run(res.link_to_html(link + addons[0],1))
data  = pr.education(education_html)
print(data.to_string())

