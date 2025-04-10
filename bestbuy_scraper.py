from seleniumwire import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from fake_useragent import UserAgent
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from price_parser import get_price_from_html

class BestBuyScraper:
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

    def get_price(self, product_name):
        self.driver = webdriver.Chrome(
            seleniumwire_options=self.seleniumwire_options,
            options=self.options
        )
        
        try:
            query = product_name.replace(" ", "+")
            self.driver.get(f"https://www.bestbuy.com/site/searchpage.jsp?st={query}")
            
            # Wait for the search results to load
            WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "li.sku-item"))
            )
            
            # Find the product by matching the name in image alt text
            product = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, f"//img[contains(@alt, '{product_name}')]"))
            )
            
            # Get the parent li.sku-item element that contains the price
            result = product.find_element(By.XPATH, "ancestor::li[contains(@class, 'sku-item')]")

            try:
                # Get the product price
                price_element = result.find_element(By.CSS_SELECTOR, "div.priceView-customer-price span[aria-hidden='true']")
                price = price_element.get_attribute("innerHTML")
                
                # Get the exact product name for verification
                product_title = product.get_attribute("alt")
                print(f"\nFound product: {product_title}")
                print(f"Price: {get_price_from_html(price)}")
                return price
            except Exception as e:
                print(f"Error finding price: {e}")
                return None
        except Exception as e:
            print(f"Error: {e}")
            return None
        finally:
            if self.driver:
                self.driver.quit() 