from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
import csv
import os
from xpaths import DETAIL_XPATHS, GBP_XPATHS

def get_listing_urls(driver, xpath):
    """Extract all listing URLs from the current page"""
    try:
        # Wait for elements to be present
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, xpath))
        )
        
        # Find all listing elements
        listing_elements = driver.find_elements(By.XPATH, xpath)
        
        # Extract URLs
        urls = []
        for element in listing_elements:
            href = element.get_attribute('href')
            if href:
                urls.append(href)
        
        return urls
    except TimeoutException:
        print("Timeout waiting for listing elements")
        return []
    except Exception as e:
        print(f"Error getting listing URLs: {str(e)}")
        return []

def click_next_page(driver, next_page_xpath):
    """Click the next page button using JavaScript"""
    try:
        # Wait for next page button to be present
        next_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, next_page_xpath))
        )
        
        # Click using JavaScript
        driver.execute_script("arguments[0].click();", next_button)
        
        # Wait for page to load
        time.sleep(2)
        return True
    except TimeoutException:
        print("No more pages available")
        return False
    except Exception as e:
        print(f"Error clicking next page: {str(e)}")
        return False

def get_element_text(driver, xpath):
    """Safely get text from an element"""
    try:
        element = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, xpath))
        )
        return element.text.strip()
    except:
        return ""

def get_element_href(driver, xpath):
    """Safely get href attribute from an element"""
    try:
        element = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, xpath))
        )
        return element.get_attribute('href')
    except:
        return ""

def get_element_src(driver, xpath):
    """Safely get src attribute from an element"""
    try:
        element = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, xpath))
        )
        return element.get_attribute('src')
    except:
        return ""

def extract_listing_details(driver, url):
    """Extract all details from a listing page"""
    try:
        # Navigate to the URL
        driver.get(url)
        time.sleep(2)  # Wait for page load
        
        # Initialize data dictionary
        data = {'url': url}
        
        # Extract all fields
        for field, xpath in DETAIL_XPATHS.items():
            if field == 'website':
                data[field] = get_element_href(driver, xpath)
            else:
                data[field] = get_element_text(driver, xpath)
        
        # Format full address
        address_parts = [
            data['address_line1'],
            data['address_line2'],
            data['locality'],
            data['administrative_area'],
            data['postal_code'],
            data['country']
        ]
        data['full_address'] = ' '.join(filter(None, address_parts))
        
        return data
    except Exception as e:
        print(f"Error extracting details from {url}: {str(e)}")
        return None

def get_google_reviews(driver, title, address):
    """Get reviews and GBP details from Google Business Profile"""
    try:
        # Navigate to Google
        driver.get("https://www.google.com")
        time.sleep(2)
        
        # Search for the business
        search_query = f"{title} {address}"
        search_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "q"))
        )
        search_box.send_keys(search_query)
        search_box.submit()
        time.sleep(3)
        
        # Initialize GBP data dictionary
        gbp_data = {}
        
        # Extract GBP details
        try:
            gbp_data['gbp_title'] = get_element_text(driver, GBP_XPATHS['gbp_title'])
        except:
            gbp_data['gbp_title'] = ""
            
        try:
            gbp_data['gbp_address'] = get_element_text(driver, GBP_XPATHS['gbp_address'])
        except:
            gbp_data['gbp_address'] = ""
            
        try:
            gbp_data['gbp_phone'] = get_element_text(driver, GBP_XPATHS['gbp_phone'])
        except:
            gbp_data['gbp_phone'] = ""
            
        try:
            gbp_data['gbp_website'] = get_element_href(driver, GBP_XPATHS['gbp_website'])
        except:
            gbp_data['gbp_website'] = ""
            
        try:
            gbp_data['gbp_image'] = get_element_src(driver, GBP_XPATHS['gbp_image'])
        except:
            gbp_data['gbp_image'] = ""
        
        # Click on Reviews button if present
        try:
            reviews_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, GBP_XPATHS['reviews_button']))
            )
            driver.execute_script("arguments[0].click();", reviews_button)
            time.sleep(2)
        except:
            print("No reviews button found")
            return [], gbp_data
        
        # Get reviews
        reviews = []
        try:
            review_elements = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.XPATH, GBP_XPATHS['review_text']))
            )
            
            for element in review_elements[:5]:  # Get up to 5 reviews
                reviews.append(element.text.strip())
                
        except:
            print("No reviews found")
        
        return reviews, gbp_data
    except Exception as e:
        print(f"Error getting Google reviews: {str(e)}")
        return [], {}

def read_csv_data(filename='restoration_listings.csv'):
    """Read data from CSV file"""
    data = []
    try:
        with open(filename, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                data.append(row)
    except Exception as e:
        print(f"Error reading CSV: {str(e)}")
    return data

def save_to_csv(data, filename='restoration_listings.csv'):
    """Save or append data to CSV file"""
    file_exists = os.path.isfile(filename)
    
    # Define fieldnames
    fieldnames = [
        'url', 'title', 'phone', 'email', 'organization',
        'address_line1', 'address_line2', 'locality',
        'administrative_area', 'postal_code', 'country',
        'full_address', 'about', 'contact', 'description', 'website',
        'gbp_title', 'gbp_address', 'gbp_phone', 'gbp_website', 'gbp_image',
        'review_1', 'review_2', 'review_3', 'review_4', 'review_5'
    ]
    
    try:
        with open(filename, 'a', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            # Write header if file doesn't exist
            if not file_exists:
                writer.writeheader()
            
            # Write data
            writer.writerow(data)
            
    except Exception as e:
        print(f"Error saving to CSV: {str(e)}")

def update_csv_with_reviews(driver, filename='restoration_listings.csv'):
    """Update CSV file with Google reviews"""
    # Read existing data
    data = read_csv_data(filename)
    
    # Create a new file for the updated data
    new_filename = 'restoration_listings_with_reviews.csv'
    
    # Process each row
    for row in data:
        print(f"\nProcessing reviews for: {row['title']}")
        
        # Get reviews and GBP data
        reviews, gbp_data = get_google_reviews(driver, row['title'], row['full_address'])
        
        # Add GBP data to the row
        row.update(gbp_data)
        
        # Add reviews to the row data
        for i, review in enumerate(reviews, 1):
            row[f'review_{i}'] = review
        
        # Fill empty review slots
        for i in range(len(reviews) + 1, 6):
            row[f'review_{i}'] = ""
        
        # Save to new CSV
        save_to_csv(row, new_filename)
        
        # Add delay between requests
        time.sleep(2) 