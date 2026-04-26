import aiofiles
from logging import exception
import random
from playwright.async_api import async_playwright, Error as PlaywrightError
from pathlib import Path
class Request:

    __BASE_DIR = Path(__file__).resolve().parent.parent
    __output_folder = __BASE_DIR / "files" / "html_files"
    __cookies = {
        "name":"li_at",
        "value":"AQEDAWb3r48EIH2oAAABnckmHRUAAAGd7TKhFU4AMWyGfWsEy88RgCuhj-FLTA7-OIyxGBOmFIiCR8UY7J9rQssufWERbvrYltwqx40LseWSiK2Qb6FvzT22NZDLzu81_t8nnmDnRovQVCmsWGkZMm0j",
        "domain":"www.linkedin.com",
        "path":"/"
    }
    

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

    async def search_to_html(self,keyword,no_pages):
        #check if output folder exist or not, if not then create it:
        self.__output_folder.mkdir(parents=True, exist_ok=True)

        html_content = []
        browser = None  
        async with async_playwright() as p:
            try:
                #Launch Chrome Browser
                browser = await p.chromium.launch(headless=False)
                context = await browser.new_context()

                #Add Cookie
                await context.add_cookies([self.__cookies])
                
                #Open Tab
                page = await context.new_page()

                #Goto Linkedin Page
                await page.goto("https://linkedin.com", timeout=60000, wait_until="domcontentloaded")
                
                #Wait 1 to 2 Seconds to Load
                await page.wait_for_timeout(random.randint(2000,3000))
        
                #Search Keyword:
                search_box = page.locator('[data-testid="typeahead-input"]')
                await search_box.click()
                await search_box.fill(keyword)
                await search_box.press("Enter")
                await page.wait_for_timeout(random.randint(10000,15000))
                
                #Wait Until Page Loads:
                await page.wait_for_load_state("domcontentloaded")

                #Click on People Button:
                people_btn = page.get_by_role("button",name="People")
                await people_btn.click()

                #Declare Next Button:
                next_btn = page.locator('button[aria-label="Next"]')

                for i in range(no_pages):
                    await page.wait_for_timeout(random.randint(10000,15000))
                    await self.auto_scroll(page)

                    content =  await page.content()
                    html_content.append(content)
                    file_path = self.__output_folder / f"searched_page_{i+1}.html"

                    async with aiofiles.open(file_path,'w',encoding='utf-8') as file:
                        await file.write(content)
                    
                    if i < no_pages - 1:
                        await next_btn.click()
                        await page.wait_for_load_state("domcontentloaded")

            except PlaywrightError as e:
                print(f"An unexpected Playwright error occurred: {e.message}")        

            finally:
                await browser.close()
            
            return html_content

    async def link_to_html(self,page_link,page_no):
        #check if output folder exist or not, if not then create it:
        self.__output_folder.mkdir(parents=True, exist_ok=True)

        #   default value incase of crash or failure:
        content = None
        
        async with async_playwright() as p:
            try:
                browser = await p.chromium.launch(headless=False)
                context = await browser.new_context()

                #add cookies to the page:
                await context.add_cookies([self.__cookies])
                
                #going to linkedin page:
                page = await context.new_page()

                # await page.goto(page_link)
                await page.goto(page_link, timeout=60000, wait_until="domcontentloaded")
                
                #reload page after cookies setup:
                await page.wait_for_timeout(random.randint(10000,15000))

                #Scroll Page to Down:
                await self.auto_scroll(page)

                #get content from page:
                content =  await page.content()
                
                #set file Name:
                file_path = self.__output_folder / f"link_page_{page_no}.html"

                #write file
                async with aiofiles.open(file_path,'w',encoding='utf-8') as file:
                    await file.write(content)

            except PlaywrightError as e:
                if "ERR_TOO_MANY_REDIRECTS" in str(e):
                    print("ERROR :    Too many redirects,")
                    print("PROBABIIY: Invalid cookie or session issue.")

                elif "ERR_CONNECTION_RESET" in str(e):
                    print("ERROR :    Connection reset by peer,")
                    print("PROBABIIY: Network issue or server-side problem.")

                elif "ERR_TIMED_OUT" in str(e):
                    print("ERROR :    Request timed out,") 
                    print("PROBABIIY: Slow network connection or server overload.")

                else:
                    print(f"An unexpected Playwright error occurred: {e.message}")                       
                
            finally:    
                await browser.close()

            return content    