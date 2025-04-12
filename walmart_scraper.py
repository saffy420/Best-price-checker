from seleniumwire import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from price_parser import get_price_from_html
from scraper_config import get_proxy_config, get_chrome_options
from selenium.webdriver.support.wait import TimeoutException
import time

class WalmartScraper:
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
            self.driver.get(f"https://www.walmart.com/search?q={query}")
            
            try:
                # Wait for search results container
                WebDriverWait(self.driver, self.timeout).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, ".sans-serif.mid-gray.relative.flex.flex-column.w-100.hide-child-opacity"))
                )
            except TimeoutException:
                # If timeout occurs, try to find element anyway
                pass
                
            # Get all product items without waiting
            results = self.driver.find_elements(By.CSS_SELECTOR, ".sans-serif.mid-gray.relative.flex.flex-column.w-100.hide-child-opacity")
            
            if not results:
                print("No results found")
                return None
                
            # Process each result until we find a matching product
            for result_index, result in enumerate(results):
                title_text = ""
                
                # Get product title/description text
                try:
                    title_elements = result.find_elements(By.CSS_SELECTOR, ".normal.dark-gray.mb0.mt1.lh-title.f6.f5-l.lh-copy")
                    if title_elements:
                        title_text = title_elements[0].text.lower()
                        
                        # Get meaningful words from product name (longer than 2 chars)
                        product_keywords = [keyword.lower() for keyword in product_name.split() if len(keyword) > 2]
                        
                        # Check if ALL product name keywords are in the title
                        all_keywords_found = all(keyword in title_text for keyword in product_keywords)
                        
                        if not all_keywords_found:
                            continue
                        
                        print(f"Found exact matching product: {title_text}")
                except Exception as e:
                    print(f"Error finding product title: {e}")
                    continue  # Try the next product
                
                # Try to find price elements with class name w_iUH7
                try:
                    # Look for all elements with class name w_iUH7 within this result
                    price_elements = result.find_elements(By.CLASS_NAME, "w_iUH7")
                    
                    # Find element containing "current"
                    for element in price_elements:
                        element_text = element.get_attribute("innerHTML").lower()
                        if "current" in element_text:
                            price = element.get_attribute("innerHTML")
                            parsed_price = get_price_from_html(price)
                            formatted_price = f"${parsed_price}" if not parsed_price.startswith('$') else parsed_price
                            print(f"Walmart Price: {formatted_price}")
                            return formatted_price
                    
                    # If no element with "current" found, use the first one
                    if price_elements:
                        price = price_elements[0].get_attribute("innerHTML")
                        parsed_price = get_price_from_html(price)
                        formatted_price = f"${parsed_price}" if not parsed_price.startswith('$') else parsed_price
                        print(f"Walmart Price (first available): {formatted_price}")
                        return formatted_price
                    else:
                        print("No price elements found with class w_iUH7 for this product, trying fallback")
                
                except Exception as e:
                    print(f"Walmart Error finding price with new method: {e}")
                
                # Fallback to original method
                try:
                    # Try to find price in this specific result
                    price_element = result.find_element(By.CLASS_NAME, "product-price")
                    price = price_element.get_attribute("innerHTML")
                    parsed_price = get_price_from_html(price)
                    formatted_price = f"${parsed_price}" if not parsed_price.startswith('$') else parsed_price
                    print(f"Walmart Price (fallback 1): {formatted_price}")
                    return formatted_price
                except Exception as e:
                    print(f"Walmart Error with fallback 1: {e}")
                    
                    # Second fallback
                    try:
                        price_element = result.find_element(By.CSS_SELECTOR, "[data-automation-id='product-price']")
                        price = price_element.get_attribute("innerHTML")
                        parsed_price = get_price_from_html(price)
                        formatted_price = f"${parsed_price}" if not parsed_price.startswith('$') else parsed_price
                        print(f"Walmart Price (fallback 2): {formatted_price}")
                        return formatted_price
                    except Exception as e:
                        print(f"Walmart Error with fallback 2: {e}, trying next product")
                        continue  # Try the next product
            
            # If we get here, we've gone through all products without finding a match
            print("No matching products found")
            return None
                
        except Exception as e:
            print(f"Walmart Error: {e}")
            return None
        finally:
            if self.driver:
                self.driver.quit()
