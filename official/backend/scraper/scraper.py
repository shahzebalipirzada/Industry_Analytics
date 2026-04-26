import utils.Request as req
import utils.Parse as parse
import asyncio


addons = ["details\education","details\experience","details\certifications"]
link = "https://www.linkedin.com/in/sher-muhammad-daudpota/"

res = req.Request()
pr =  parse.Parse()
education_html = asyncio.run(res.link_to_html(link + addons[2],1))
data  = pr.education(education_html)
print(data.to_string())

