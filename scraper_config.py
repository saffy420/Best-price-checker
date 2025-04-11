import os
from dotenv import load_dotenv
from selenium.webdriver.chrome.options import Options
from fake_useragent import UserAgent

# Load environment variables from .env file
load_dotenv()

def get_proxy_config():
    username = os.getenv("PROXY_USERNAME")
    password = os.getenv("PROXY_PASSWORD")
    host = os.getenv("PROXY_HOST")
    port = os.getenv("PROXY_PORT")
    
    proxy_url = f"http://{username}:{password}@{host}:{port}"
    
    seleniumwire_options = {
        "proxy": {
            "http": proxy_url,
            "https": proxy_url  
        }
    }
    return seleniumwire_options

def get_chrome_options():
    options = Options()
    options.add_argument("--disable-gpu")
    options.add_argument(f"user-agent={UserAgent().random}")
    options.add_argument("--no-sandbox")
    #options.add_argument("--headless")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-infobars")
    options.add_argument("--window-size=1920x1080")
    options.add_argument("--enable-unsafe-swiftshader")
    options.add_argument("--disable-headless")
    
    
    return options

