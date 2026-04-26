
import random
from playwright.async_api import async_playwright, Error as PlaywrightError

class Request:

    __cookies = {
        "name":"li_at",
        "value":"AQEDAWeaWV4EmfAgAAABncsFCOIAAAGd7xGM4k4AF5iSApATbKwdl2duCLdoT0ErLMthbx9M3ztmXTOSVec6mHNU-bIcFLwsMqFjzyee6OJclmnq69JWBtOwcKIHmPE68q4M-Vr3BxHrJcRIwe4i8rBR",
        "domain":"www.linkedin.com",
        "path":"/"
    }

    def __init__(self):
        self.playwright = None
        self.browser    = None
        self.context    = None
        self.page       = None
        
    async def __aenter__(self):
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch(headless=False)
        self.context = await self.browser.new_context()
        await self.context.add_cookies([self.__cookies])
        self.page  = self.context.pages[0] if self.context.pages else await self.context.new_page()   
        print("Browser launched")
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.context:
            await self.context.close()
        if self.playwright:
            await self.playwright.stop()
        print("Browser closed")
    

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
        await page.wait_for_timeout(random.randint(2000,3000))

    async def search_to_html(self,keyword,no_pages):

        html_content = []
    
        try:
            #Goto Linkedin Page
            await self.page.goto("https://linkedin.com", timeout=60000, wait_until="domcontentloaded")
            
            #Wait 1 to 2 Seconds to Load
            await self.page.wait_for_timeout(random.randint(2000,3000))
    
            #Search Keyword:
            search_box = self.page.locator('[data-testid="typeahead-input"]')
            await search_box.click()
            await search_box.fill(keyword)
            await search_box.press("Enter")
            await self.page.wait_for_timeout(random.randint(10000,15000))
            
            #Wait Until Page Loads:
            await self.page.wait_for_load_state("domcontentloaded")

            #Click on People Button:
            people_btn = self.page.get_by_role("button", name="People")
            await people_btn.wait_for(state="visible", timeout=120000)  # wait until visible
            await people_btn.scroll_into_view_if_needed()               # scroll to it
            await people_btn.click()

            #Declare Next Button:
            next_btn = self.page.locator('button[aria-label="Next"]')

            for i in range(no_pages):
                await self.page.wait_for_timeout(random.randint(10000,15000))
                await self.auto_scroll(self.page)

                content =  await self.page.content()
                html_content.append(content)
                
                if i < no_pages - 1 and await next_btn.is_visible():
                    await next_btn.click()
                    await self.page.wait_for_load_state("domcontentloaded")
                else:
                    break

        except PlaywrightError as e:
            if "ERR_TOO_MANY_REDIRECTS" in e.message:
                print("ERROR :    Too many redirects,")
                print("PROBABIIY: Invalid cookie or session issue.")

            elif "ERR_CONNECTION_RESET" in e.message:
                print("ERROR :    Connection reset by peer,")
                print("PROBABIIY: Network issue or server-side problem.")

            elif "ERR_TIMED_OUT" in e.message:
                print("ERROR :    Request timed out,") 
                print("PROBABIIY: Slow network connection or server overload.")

            else:
                print(f"An unexpected Playwright error occurred: {e.message}")          
        
        return html_content

    async def link_to_html(self,page_link):
        content = None
        try:
            await self.page.goto(page_link, timeout=60000, wait_until="domcontentloaded")
            
            #reload page after cookies setup:
            await self.page.wait_for_timeout(random.randint(10000,15000))

            #Scroll Page to Down:
            await self.auto_scroll(self.page)

            #get content from page:
            content =  await self.page.content()
            
        except PlaywrightError as e:
            if "ERR_TOO_MANY_REDIRECTS" in e.message:
                print("ERROR :    Too many redirects,")
                print("PROBABIIY: Invalid cookie or session issue.")

            elif "ERR_CONNECTION_RESET" in e.message:
                print("ERROR :    Connection reset by peer,")
                print("PROBABIIY: Network issue or server-side problem.")

            elif "ERR_TIMED_OUT" in e.message:
                print("ERROR :    Request timed out,") 
                print("PROBABIIY: Slow network connection or server overload.")

            else:
                print(f"An unexpected Playwright error occurred: {e.message}")                       
            
        return content   