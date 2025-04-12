# Best-price-checker

A concurrent web scraper tool that compares product prices across multiple online retailers, helping you find the best deals.

## Description

Best-price-checker is a Python-based application that allows users to enter a product name and automatically retrieve the current price from multiple major retailers including Amazon, Best Buy, Walmart, and Newegg. The application utilizes multithreading to perform searches concurrently, providing results quickly and efficiently.

## Features

- Scrapes product prices from four major retailers:
  - Amazon
  - Best Buy  
  - Walmart
  - Newegg
- Concurrent execution using Python's ThreadPoolExecutor for faster results
- Robust error handling to deal with retailer website variations
- Consistent price formatting with dollar signs
- Proxy support for avoiding IP blocks

## Requirements

- Python 3.6+
- Chrome browser
- ChromeDriver (compatible with your Chrome version)

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/Best-price-checker.git
   cd Best-price-checker
   ```

2. Install required packages:
   ```
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the root directory with your proxy settings (if needed):
   ```
   PROXY_USERNAME=your_username
   PROXY_PASSWORD=your_password
   PROXY_HOST=your_proxy_host
   PROXY_PORT=your_proxy_port
   ```

## Usage

Run the main script and follow the prompts:

```
python main.py
```

When prompted, enter the product name you want to search for. The application will then:
1. Search all retailers concurrently
2. Display prices as they become available
3. Show a final comparison of all results with the total search time

Example output:

```
Enter the product name: jbl flip 6

Searching prices...
------------------------------

Price Comparison:
------------------------------
Amazon: $149.95
Best Buy: $129.99
Walmart: $119.99
Newegg: $139.95

Total search time: 12.34 seconds
```

## Architecture

The project consists of separate scraper modules for each retailer:

- `amazon_scraper.py`: Handles Amazon product searches
- `bestbuy_scraper.py`: Handles Best Buy product searches  
- `walmart_scraper.py`: Handles Walmart product searches
- `newegg_scraper.py`: Handles Newegg product searches
- `scraper_config.py`: Contains shared configuration for proxies and browser options
- `main.py`: Coordinates the concurrent execution of all scrapers

Each scraper uses Selenium with Selenium Wire for web automation and handles various edge cases specific to each retailer's website.

## Troubleshooting

- If you encounter captchas or blocks, try:
  - Using a different proxy
  - Adjusting the user agent in `scraper_config.py`
  - Increasing timeouts in the scraper classes
- If a specific retailer consistently fails, check if their website structure has changed

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the project
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

Made for AP CSP 24-25
