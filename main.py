from amazon_scraper import AmazonScraper
from bestbuy_scraper import BestBuyScraper
from newegg_scraper import NeweggScraper
from walmart_scraper import WalmartScraper
from concurrent.futures import ThreadPoolExecutor
import time

def get_amazon_price(product_name):
    amazon_scraper = AmazonScraper()
    return ("Amazon", amazon_scraper.get_price(product_name))

def get_bestbuy_price(product_name):
    bestbuy_scraper = BestBuyScraper()
    return ("Best Buy", bestbuy_scraper.get_price(product_name))

def get_newegg_price(product_name):
    newegg_scraper = NeweggScraper()
    return ("Newegg", newegg_scraper.get_price(product_name))

def get_walmart_price(product_name):
    walmart_scraper = WalmartScraper()
    return ("Walmart", walmart_scraper.get_price(product_name))

def get_prices(product_name):
    start_time = time.time()
    
    # Create a list of tasks to run
    tasks = [
        get_amazon_price,
        get_bestbuy_price,
        get_newegg_price,
        get_walmart_price
    ]
    
    # Run all scrapers concurrently
    with ThreadPoolExecutor(max_workers=4) as executor:
        # Submit all tasks and get their futures
        futures = [executor.submit(task, product_name) for task in tasks]
        
        # Print header while waiting
        print("\nSearching prices...")
        print("-" * 30)
        
        # Collect results as they complete
        results = {}
        for future in futures:
            store, price = future.result()
            results[store] = price
    
    # Print results
    print("\nPrice Comparison:")
    print("-" * 30)
    for store, price in results.items():
        print(f"{store}: {price if price else 'Not found'}")
    
    end_time = time.time()
    print(f"\nTotal search time: {end_time - start_time:.2f} seconds")

if __name__ == "__main__":
    product_name = input("Enter the product name: ")
    get_prices(product_name)
    
