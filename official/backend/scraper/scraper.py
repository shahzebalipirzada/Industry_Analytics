import utils.Request as req
import asyncio

res = req.Request()
asyncio.run(res.link_to_html("https://www.linkedin.com/in/amir-khan-1021273aa/",1))


