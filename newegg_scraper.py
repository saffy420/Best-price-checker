from seleniumwire import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from scraper_config import get_proxy_config, get_chrome_options
from selenium.common.exceptions import NoSuchElementException
import time

class NeweggScraper:
    def __init__(self):
        self.seleniumwire_options = get_proxy_config()
        self.options = get_chrome_options()
        self.driver = None

    def get_price(self, product_name):
        max_attempts = 3
        attempts = 0
        
        try:
            while attempts < max_attempts:
                try:
                    # Initialize a new WebDriver for each attempt
                    if self.driver:
                        self.driver.quit()
                        
                    self.driver = webdriver.Chrome(
                        seleniumwire_options=self.seleniumwire_options,
                        options=self.options
                    )
                    
                    query = product_name.replace(" ", "+")
                    self.driver.get(f"https://www.newegg.com/p/pl?d={query}")
                    
                    # Check if 404 page exists
                    try:
                        self.driver.find_element(By.CLASS_NAME, "page-404-text")
                        print(f"404 page detected, restarting session (attempt {attempts+1}/{max_attempts})...")
                        attempts += 1
                        continue  # Skip to next iteration, which will restart the session
                    except NoSuchElementException:
                        # No 404 page found, proceed with scraping
                        pass
                    
                    # Wait for the search results to load
                    WebDriverWait(self.driver, 30).until(
                        EC.presence_of_element_located((By.CLASS_NAME, "item-open-box-italic"))
                    )
                    
                    # Find the product by matching the class name
                    result = WebDriverWait(self.driver, 10).until(
                        EC.presence_of_element_located((By.CLASS_NAME, "item-open-box-italic"))
                    )
                    
                    print(result.get_attribute("outerHTML"))

                    # Get the product price
                    price_element = result.find_element(By.CSS_SELECTOR, "li.price-current")
                    dollars = price_element.find_element(By.TAG_NAME, "strong").text
                    cents = price_element.find_element(By.TAG_NAME, "sup").text
                    price = f"${dollars}.{cents}"
                    
                    print(f"Price: {price}")
                    return price
                    
                except Exception as e:
                    print(f"Error: {e}")
                    attempts += 1
                    
                    # Close the current driver before retrying
                    if self.driver:
                        self.driver.quit()
                        self.driver = None
                        
                    # Wait a bit before retrying
                    time.sleep(2)
                    
            print(f"Maximum attempts ({max_attempts}) reached, unable to get price")
            return None
                
        finally:
            if self.driver:
                self.driver.quit()
                self.driver = None


scraper = NeweggScraper()
price = scraper.get_price("jbl flip 6")
print(f"Final Price: {price}")
