def get_price_from_html(html_string):
    """
    Extracts a price value from HTML string by keeping only digits and decimal points.
    
    Args:
        html_string (str): HTML string containing a price
        
    Returns:
        str: Extracted price as a string containing only digits and decimal point
    """
    price = []
    for char in html_string:
        if char.isdigit() or char == ".":
            price.append(char)   
    return ''.join(price) 