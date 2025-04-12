from seleniumwire import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from price_parser import get_price_from_html
from scraper_config import get_proxy_config, get_chrome_options
from selenium.webdriver.support.wait import TimeoutException
import time

class BestBuyScraper:
    def __init__(self):
        self.seleniumwire_options = get_proxy_config()
        self.options = get_chrome_options()
        self.driver = None
        self.timeout = 20  # Set consistent timeout

    def get_price(self, product_name):
        self.driver = webdriver.Chrome(
            seleniumwire_options=self.seleniumwire_options,
            options=self.options
        )
        
        try:
            query = product_name.replace(" ", "+")
            
            # Set timeouts
            self.driver.set_page_load_timeout(self.timeout)
            self.driver.set_script_timeout(self.timeout)
            
            # Load the page
            self.driver.get(f"https://www.bestbuy.com/site/searchpage.jsp?st={query}")
            
            try:
                # Wait for search results container
                WebDriverWait(self.driver, self.timeout).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "sku-item"))
                )
            except TimeoutException:
                # If timeout occurs, try to find element anyway
                pass
                
            # Get all product items without waiting
            results = self.driver.find_elements(By.CLASS_NAME, "sku-item")
            
            if results:
                result = results[0]  # Take the first result
                try:
                    # Wait for price element to be present and visible
                    price_element = WebDriverWait(self.driver, self.timeout).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, "div.priceView-customer-price span[aria-hidden='true']"))
                    )
                    # Additional wait for visibility
                    WebDriverWait(self.driver, self.timeout).until(
                        EC.visibility_of(price_element)
                    )
                    
                    price = price_element.get_attribute("innerHTML")
                    parsed_price = get_price_from_html(price)
                    formatted_price = f"${parsed_price}" if not parsed_price.startswith('$') else parsed_price
                    print(f"Best Buy Price: {formatted_price}")
                    return formatted_price
                except TimeoutException as e:
                    print(f"Best Buy Error: Price element not found within {self.timeout} seconds")
                    return None
                except Exception as e:
                    print(f"Best Buy Error finding price: {e}")
                    return None
            else:
                print("No results found")
                return None
                
        except Exception as e:
            print(f"Best Buy Error: {e}")
            return None
        finally:
            if self.driver:
                self.driver.quit()
