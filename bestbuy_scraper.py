from seleniumwire import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from price_parser import get_price_from_html
from scraper_config import get_proxy_config, get_chrome_options

class BestBuyScraper:
    def __init__(self):
        self.seleniumwire_options = get_proxy_config()
        self.options = get_chrome_options()
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
            result = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "sku-item"))
            )

            try:
                # Get the product price
                price_element = result.find_element(By.CSS_SELECTOR, "div.priceView-customer-price span[aria-hidden='true']")
                price = price_element.get_attribute("innerHTML")
                
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

scraper = BestBuyScraper()
price = scraper.get_price("jbl flip 6")
print(f"Final Price: {price}")



