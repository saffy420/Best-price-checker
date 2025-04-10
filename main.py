from amazon_scraper import AmazonScraper
from bestbuy_scraper import BestBuyScraper

def get_prices(product_name):
    # Get Amazon price
    amazon_scraper = AmazonScraper()
    amazon_price = amazon_scraper.get_price(product_name)
    
    # Get Best Buy price
    bestbuy_scraper = BestBuyScraper()
    bestbuy_price = bestbuy_scraper.get_price(product_name)
    
    # Print comparison
    print("\nPrice Comparison:")
    print("-" * 30)
    print(f"Amazon: {amazon_price if amazon_price else 'Not found'}")
    print(f"Best Buy: {bestbuy_price if bestbuy_price else 'Not found'}")

if __name__ == "__main__":
    product_name = input("Enter the product name: ")
    get_prices(product_name)
    

