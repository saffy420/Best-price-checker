from seleniumwire import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from scraper_config import get_proxy_config, get_chrome_options
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import time

class NeweggScraper:
    def __init__(self):
        self.seleniumwire_options = get_proxy_config()
        self.options = get_chrome_options()
        self.driver = None
        self.max_retries = 3
        self.retry_delay = 1
        self.timeout = 20  # Set consistent timeout

    def get_price(self, product_name):
        attempts = 0
        
        while attempts < self.max_retries:
            try:
                # Initialize a new WebDriver for each attempt
                if self.driver:
                    self.driver.quit()
                    
                self.driver = webdriver.Chrome(
                    seleniumwire_options=self.seleniumwire_options,
                    options=self.options
                )
                
                # Set timeouts
                self.driver.set_page_load_timeout(self.timeout)
                self.driver.set_script_timeout(self.timeout)
                
                query = product_name.replace(" ", "+")
                start_time = time.time()
                
                # Load the page
                self.driver.get(f"https://www.newegg.com/p/pl?d={query}")
                print(f"Time taken to load Newegg: {time.time() - start_time:.2f} seconds")
                
                # Quick check for 404 page
                try:
                    if self.driver.find_elements(By.CLASS_NAME, "page-404-text"):
                        print(f"404 page detected, retrying (attempt {attempts+1}/{self.max_retries})...")
                        attempts += 1
                        time.sleep(self.retry_delay)
                        continue
                except:
                    pass
                
                try:
                    # Use consistent timeout for initial load
                    WebDriverWait(self.driver, self.timeout).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, ".item-container"))
                    )
                except TimeoutException:
                    # If timeout occurs, try to find element anyway
                    pass
                
                # Try to find results without waiting
                results = self.driver.find_elements(By.CSS_SELECTOR, ".item-container")
                
                if results:
                    result = results[0]  # Take the first result
                    try:
                        # Try to get price directly without waiting
                        price_element = result.find_element(By.CSS_SELECTOR, "li.price-current")
                        dollars = price_element.find_element(By.TAG_NAME, "strong").text
                        cents = price_element.find_element(By.TAG_NAME, "sup").text
                        price = f"${dollars}{cents}"
                        print(f"Newegg Price: {price}")
                        return price
                    except Exception as e:
                        print(f"Newegg Error finding price: {e}")
                        return None
                else:
                    print("No results found")
                    attempts += 1
                    time.sleep(self.retry_delay)
                    continue
                    
            except Exception as e:
                print(f"Newegg Error: {e}")
                attempts += 1
                time.sleep(self.retry_delay)
                
                if self.driver:
                    self.driver.quit()
                    self.driver = None
            
        print(f"Maximum attempts ({self.max_retries}) reached, unable to get price")
        return None
                
        if self.driver:
            self.driver.quit()
            self.driver = None




