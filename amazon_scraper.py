from seleniumwire import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from price_parser import get_price_from_html
from scraper_config import get_proxy_config, get_chrome_options
from selenium.webdriver.support.wait import TimeoutException
import time

class AmazonScraper:
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
            self.driver.get(f"https://www.amazon.com/s?k={query}&field-keywords={query}")
            
            try:
                # Wait for search results container
                WebDriverWait(self.driver, self.timeout).until(
                    EC.presence_of_element_located((By.XPATH, "//*[contains(@cel_widget_id, 'MAIN-SEARCH_RESULTS-')]"))
                )
            except TimeoutException:
                # If timeout occurs, try to find element anyway
                pass
            
            # Try to find results without waiting
            results = self.driver.find_elements(By.XPATH, "//*[contains(@cel_widget_id, 'MAIN-SEARCH_RESULTS-')]")
            
            if results:
                result = results[0]  # Take the first result
                try:
                    # Try to get price directly without waiting
                    price_element = result.find_element(By.CSS_SELECTOR, "span.a-price > span.a-offscreen")
                    price = price_element.get_attribute("outerHTML")
                    parsed_price = get_price_from_html(price)
                    formatted_price = f"${parsed_price}" if not parsed_price.startswith('$') else parsed_price
                    print(f"Amazon Price: {formatted_price}")
                    return formatted_price
                except Exception as e:
                    print(f"Amazon Error finding price: {e}")
                    
                    # Fallback: try alternative price selectors
                    try:
                        price_element = result.find_element(By.CSS_SELECTOR, "span.a-price")
                        price = price_element.get_attribute("outerHTML")
                        parsed_price = get_price_from_html(price)
                        formatted_price = f"${parsed_price}" if not parsed_price.startswith('$') else parsed_price
                        print(f"Amazon Price (fallback): {formatted_price}")
                        return formatted_price
                    except:
                        return None
            else:
                print("No results found")
                return None
                
        except Exception as e:
            print(f"Amazon Error: {e}")
            return None
        finally:
            if self.driver:
                self.driver.quit()




