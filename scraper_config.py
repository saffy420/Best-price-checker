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
        },
        "verify_ssl": False,  # Improve performance by disabling SSL verification
        "suppress_connection_errors": True,  # Suppress connection noise
        "connection_timeout": None  # Disable connection timeout
    }
    return seleniumwire_options

def get_chrome_options():
    options = Options()
    user_agent = UserAgent().random
    options.add_argument(f'user-agent={user_agent}')
    
    # Optimized headless configuration
    options.add_argument('--headless=new')
    options.add_argument('--window-size=1280,720')  # Reduced window size for better performance
    
    # Critical performance optimizations
    options.page_load_strategy = 'none'  # Don't wait for full page load
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    
    # Memory and CPU optimizations
    options.add_argument('--disable-javascript')  # Disable JS for pure HTML scraping
    options.add_argument('--disk-cache-size=50000000')  # 50MB disk cache
    options.add_argument('--media-cache-size=50000000')  # 50MB media cache
    options.add_argument('--disable-features=TranslateUI,BlinkGenPropertyTrees,IsolateOrigins,site-per-process')
    options.add_argument('--disable-dev-tools')
    
    # Disable unnecessary features
    options.add_argument('--disable-extensions')
    options.add_argument('--disable-notifications')
    options.add_argument('--disable-popup-blocking')
    options.add_argument('--blink-settings=imagesEnabled=false')
    
    # Resource usage optimizations
    prefs = {
        'profile.managed_default_content_settings': {
            'images': 2,
            'javascript': 2,
            'cookies': 2,
            'plugins': 2,
            'popups': 2,
            'geolocation': 2,
            'notifications': 2,
            'auto_select_certificate': 2,
            'fullscreen': 2,
            'mouselock': 2,
            'mixed_script': 2,
            'media_stream': 2,
            'media_stream_mic': 2,
            'media_stream_camera': 2,
            'protocol_handlers': 2,
            'ppapi_broker': 2,
            'automatic_downloads': 2,
            'midi_sysex': 2,
            'push_messaging': 2,
            'ssl_cert_decisions': 2,
            'metro_switch_to_desktop': 2,
            'protected_media_identifier': 2,
            'app_banner': 2,
            'site_engagement': 2,
            'durable_storage': 2
        },
        'disk-cache-size': 50000000,
        'profile.default_content_setting_values': {
            'cookies': 2
        }
    }
    options.add_experimental_option('prefs', prefs)
    
    return options

