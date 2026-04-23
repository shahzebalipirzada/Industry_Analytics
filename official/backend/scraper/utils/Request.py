import asyncio
from playwright.async_api import async_playwright
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
output_folder = BASE_DIR / "files" / "html_files"
output_folder.mkdir(parents=True, exist_ok=True)



class Request:
    
          
    async def auto_scroll(self,page):
            await page.evaluate(
                '''
                window.scrollTo(
                    {
                        top:document.body.scrollHeight,
                        behavior: 'smooth'
                    }
                )
                '''
            )

    async def search_to_html(self,search_keyword,no_pages):
          html_content = []
          async with async_playwright() as p:
                browser = await p.chromium.launch(headless=False)
                context = await browser.new_context()

                #going to linkedin page:
                page = await context.new_page()
                

                #add cookies to the page:

                await context.add_cookies([
                      {
                            "name":"li_at",
                            "value":"AQEDAWb3r48EVENyAAABnbS7st4AAAGd2Mg23k4AVlLf9djMl4-8dtxtrQ-fzzmJ95iHYySTNl6y0G7Go7v55_okeL0nd7U_nVuVKdV63f1Gl7CQ5n-jisQeFHTMro5l7s9j9DWTUpDtaw1jV8w_qbAj",
                            "domain":"www.linkedin.com",
                            "path":"/"
                      }
                ])

                await page.goto("https://linkedin.com")


               

                #wait till dom content is loaded:
                await page.wait_for_load_state("domcontentloaded")

                keyword = search_keyword
                
                #searching keyword:
                search_box = page.locator('[data-testid="typeahead-input"]')
                await search_box.click()
                await search_box.fill(keyword)

                await search_box.press("Enter")
                await page.wait_for_timeout(10000)
                #wait till searched page loaded:
                await page.wait_for_load_state("domcontentloaded")

                #click the people button:
                people_btn = page.get_by_role("button",name="People")
                await people_btn.click()

                #scroll page to down:
                await self.auto_scroll(page)


                #declare next page button:
                next_btn = page.locator('button[aria-label="Next"]')

                for i in range(no_pages):
                    
                    await page.wait_for_timeout(10000)
                    await self.auto_scroll(page)
                    content =  await page.content()
                    html_content.append(content)
                    file_path = output_folder / f"searched_page_{i+1}.html"

                    with open(file_path,'w',encoding='utf-8') as file:
                        file.write(content)
                    await next_btn.click()


                browser.close()
                return html_content

    async def link_to_html(self,page_link,page_no):
          
          async with async_playwright() as p:
                browser = await p.chromium.launch(headless=False)
                context = await browser.new_context()

                #going to linkedin page:
                page = await context.new_page()
                

                #add cookies to the page:

                await context.add_cookies([
                      {
                            "name":"li_at",
                            "value":"AQEDAWb3r48EVENyAAABnbS7st4AAAGd2Mg23k4AVlLf9djMl4-8dtxtrQ-fzzmJ95iHYySTNl6y0G7Go7v55_okeL0nd7U_nVuVKdV63f1Gl7CQ5n-jisQeFHTMro5l7s9j9DWTUpDtaw1jV8w_qbAj",
                            "domain":"www.linkedin.com",
                            "path":"/"
                      }
                ])
                
                # await page.goto(page_link)
                await page.goto(page_link, timeout=60000, wait_until="domcontentloaded")
                #reload page after cookies setup:

                # await page.reload()

                #wait till dom content is loaded:
                await page.wait_for_load_state("domcontentloaded")

                await page.wait_for_timeout(10000)

                #Scroll Page to Down:
                await self.auto_scroll(page)

                #get content from page:
                content =  await page.content()
                
                #set file Name:
                file_path = output_folder / f"link_page_{page_no}.html"

                #write file
                with open(file_path,'w',encoding='utf-8') as file:
                    file.write(content)
                    

                

                await browser.close()
                return content
                      






                
    