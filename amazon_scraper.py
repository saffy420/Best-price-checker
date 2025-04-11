from seleniumwire import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from price_parser import get_price_from_html
from scraper_config import get_proxy_config, get_chrome_options

class AmazonScraper:
    def __init__(self):
        self.seleniumwire_options = get_proxy_config()
        self.options = get_chrome_options()
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
                
                
                return get_price_from_html(price)
            except Exception as e:
                print(f"Error finding price or title: {e}")
                return None  # Skip if price or title not found
        except Exception as e:
            print(f"Error: {e}")
            return None
        finally:
            if self.driver:
                self.driver.quit() 

