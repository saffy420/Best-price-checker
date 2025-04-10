from seleniumwire import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import random
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from fake_useragent import UserAgent

proxy_url = "http://pcDCKl5YiW-res-us:PC_1dYtl5BcqA7Zz4j7e@proxy-us.proxy-cheap.com:5959"

seleniumwire_options = {
    "proxy": {
        "http": proxy_url,
        "https": proxy_url  
    }
}

# Initialize the UserAgent object
ua = UserAgent()

# Get a random user agent
random_user_agent = ua.random

options = Options()
options.add_argument("--disable-gpu")
options.add_argument(f"user-agent={random_user_agent}")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-extensions")
options.add_argument("--disable-infobars")
options.add_argument("--window-size=1920x1080")


driver = webdriver.Chrome(
    seleniumwire_options=seleniumwire_options,
    options=options
)

def get_price(product_name):
    query = product_name.replace(" ", "+")
    driver.get(f"https://www.amazon.com/s?k={query}&field-keywords={query}")

    try:
        # Wait for the product grid to load
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.s-main-slot"))
        )
        results = driver.find_elements(By.CSS_SELECTOR, "div.s-main-slot div[data-component-type='s-search-result']")
        for result in results:
            # Skip if "Sponsored"
            try:
                badge = result.find_element(By.CSS_SELECTOR, "aok-inline-block s-ad-feedback-label puis-sponsored-label-text")
                print(f"Badge text: {badge.text}")  # Debugging line
                if "Sponsored" in badge.text:
                    continue  # Skip this result if it is sponsored
            except Exception as e:
                print(f"Exception: {e}")  # Debugging line
                pass
        try:
            price_element = driver.find_element(By.CSS_SELECTOR, "span.a-price > span.a-offscreen")
            price = price_element.get_attribute("outerHTML")
            print(f"Price: {get_int_from_outerhtml(price)}")
            return price
        except:
            print("Price not found")
            return None  # Skip if price not found

    except Exception as e:
        print(f"Error: {e}")
    finally:
        return None

def get_int_from_outerhtml(outerhtml):
    price = []
    for i in outerhtml:
        if i.isdigit() or i == ".":
            price.append(i)   
    return ''.join(price)

if __name__ == "__main__":
    get_price(product_name = input("Enter the product name: "))

