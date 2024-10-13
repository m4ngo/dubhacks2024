
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Path to the Chrome WebDriver, provide the path if necessary
# Example: driver = webdriver.Chrome('path_to_chromedriver/chromedriver.exe')
driver = webdriver.Chrome()

# Define the URL to scrape
url_page = "https://www.traderjoes.com/home/products/category/snacks-sweets-167"


# Navigate to the URL
driver.get(url_page)

#Find Prices and Items and Append in parallel Arrays
Prices = []
Items = []
i = 1
divisor = 1

determiner = True
"""
while determiner == True:
    
    if i == 2:
        divisor = len(Items)

    # Define the URL to scrape
    url = url_page+"?filters=%7B%22page%22%3A"+str(i)+"%7D"
    # Navigate to the URL
    driver.get(url)
    
    # Find Qty
    try:
        WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'span.ProductPrice_productPrice__price__3-50j'))
    )
    except Exception as e:
        print(f"Error occurred: {e}")
        driver.quit()
    
    # Find all price elements
    price_elements = driver.find_elements(By.CSS_SELECTOR, 'span.ProductPrice_productPrice__price__3-50j')

    for j in range(0, len(price_elements)):
        Prices.append((price_elements[j].text))
    
    # Find all product titles
    try:
        WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'h2.ProductCard_card__title__text__uiWLe'))
    )
    except Exception as e:
        print(f"Error occurred: {e}")
        driver.quit()
    
    Item_names = driver.find_elements(By.CSS_SELECTOR, 'h2.ProductCard_card__title__text__uiWLe a')
    
    i = i+1
    
    for title in Item_names:
        Items.append(title.text)
    
    if len(Item_names)%divisor != 0:
        determiner = False 
    else:
        determiner = True
    
    try:
        WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'span.ProductPrice_productPrice__unit__2jvkA'))
    )
    except Exception as e:
        print(f"Error occurred: {e}")
        driver.quit()
    
    # Find all price elements
    qty_elements = driver.find_elements(By.CSS_SELECTOR, 'span.ProductPrice_productPrice__unit__2jvkA')

    for k in range(0, len(qty_elements)):
        temp = qty.elements[k].text 
        value = Items[k] + temp
        Items[k] = value
"""
# Close the browser
driver.quit()
