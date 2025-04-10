from seleniumwire import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from fake_useragent import UserAgent
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from price_parser import get_price_from_html

class AmazonScraper:
    def __init__(self):
        self.proxy_url = "http://pcDCKl5YiW-res-us:PC_1dYtl5BcqA7Zz4j7e@proxy-us.proxy-cheap.com:5959"
        self.seleniumwire_options = {
            "proxy": {
                "http": self.proxy_url,
                "https": self.proxy_url  
            }
        }
        
        self.options = Options()
        self.options.add_argument("--disable-gpu")
        self.options.add_argument(f"user-agent={UserAgent().random}")
        self.options.add_argument("--no-sandbox")
        self.options.add_argument("--headless")
        self.options.add_argument("--disable-dev-shm-usage")
        self.options.add_argument("--disable-extensions")
        self.options.add_argument("--disable-infobars")
        self.options.add_argument("--window-size=1920x1080")
        
        self.driver = None

    def _get_int_from_outerhtml(self, outerhtml):
        price = []
        for i in outerhtml:
            if i.isdigit() or i == ".":
                price.append(i)   
        return ''.join(price)

    def get_price(self, product_name):
        self.driver = webdriver.Chrome(
            seleniumwire_options=self.seleniumwire_options,
            options=self.options
        )
        
        try:
            query = product_name.replace(" ", "+")
            self.driver.get(f"https://www.amazon.com/s?k={query}&field-keywords={query}")
            
            # Wait for the main search result to load
            WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.XPATH, "//*[@cel_widget_id='MAIN-SEARCH_RESULTS-5']"))
            )
            # Find the main search result
            result = self.driver.find_element(By.XPATH, "//*[@cel_widget_id='MAIN-SEARCH_RESULTS-5']")

            try:
                # Get the product price
                price_element = result.find_element(By.CSS_SELECTOR, "span.a-price > span.a-offscreen")
                price = price_element.get_attribute("outerHTML")
                
                print(f"Price: {get_price_from_html(price)}")
                return price
            except Exception as e:
                print(f"Error finding price or title: {e}")
                return None  # Skip if price or title not found
        except Exception as e:
            print(f"Error: {e}")
            return None
        finally:
            if self.driver:
                self.driver.quit() 