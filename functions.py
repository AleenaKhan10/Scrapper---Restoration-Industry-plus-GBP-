from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
import csv
import os
from xpaths import DETAIL_XPATHS, GBP_XPATHS, EXTRA_FIELDS_XPATH, STANDARD_FIELDS

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
        element = WebDriverWait(driver, 2).until(
            EC.presence_of_element_located((By.XPATH, xpath))
        )
        return element.get_attribute('href')
    except:
        return ""

def get_element_src(driver, xpath):
    """Safely get src attribute from an element"""
    try:
        element = WebDriverWait(driver, 2).until(
            EC.presence_of_element_located((By.XPATH, xpath))
        )
        return element.get_attribute('src')
    except:
        return ""

def get_extra_fields(driver):
    """Extract extra fields from the listing page"""
    extra_fields = {}
    try:
        # Find all field elements
        field_elements = driver.find_elements(By.XPATH, EXTRA_FIELDS_XPATH)
        
        for element in field_elements:
            try:
                # Get the field name (key)
                key_element = element.find_element(By.XPATH, "./div")
                key = key_element.text.strip()
                
                # Skip if it's a standard field
                if key in STANDARD_FIELDS:
                    continue
                
                # Get the field value
                value_element = element.find_element(By.XPATH, "./div[2]")
                value = value_element.text.strip()
                
                if key and value:  # Only add if both key and value exist
                    extra_fields[key] = value
            except:
                continue
                
        return extra_fields
    except:
        return {}

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
        
        # Get extra fields
        extra_fields = get_extra_fields(driver)
        data['extra_fields'] = extra_fields
        
        return data
    except Exception as e:
        print(f"Error extracting details from {url}: {str(e)}")
        return None

def extract_cid_from_href(href):
    """Extract CID from Google Business Profile href"""
    try:
        # Extract the ludocid parameter from the href
        if 'ludocid=' in href:
            cid = href.split('ludocid=')[1].split('&')[0]
            return cid
        return ""
    except:
        return ""

def create_maps_url(cid):
    """Create Google Maps URL from CID"""
    if cid:
        return f"https://maps.google.com/?cid={cid}"
    return ""

def get_google_reviews(driver, title, address):
    """Get reviews and GBP details from Google Business Profile"""
    try:
        # Navigate to Google
        driver.get("https://www.google.com")
        time.sleep(2)
        
        # Search for the business
        search_query = f"{title} {address}"
        search_box = WebDriverWait(driver, 5).until(
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

        try:
            gbp_data['gbp_map_image'] = get_element_src(driver, GBP_XPATHS['gbp_map_image'])
        except:
            gbp_data['gbp_map_image'] = ""

        try:
            gbp_data['gbp_outside_image'] = get_element_src(driver, GBP_XPATHS['gbp_outside_image'])
        except:
            gbp_data['gbp_outside_image'] = ""

        # Extract CID and create Maps URL
        try:
            cid_href = get_element_href(driver, GBP_XPATHS['gbp_cid_link'])
            cid = extract_cid_from_href(cid_href)
            gbp_data['gbp_maps_url'] = create_maps_url(cid)
        except:
            gbp_data['gbp_maps_url'] = ""
        
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
                # Check for 'More' link and click if present
                try:
                    more_link = element.find_element(By.XPATH, ".//a[text()='More']")
                    driver.execute_script("arguments[0].click();", more_link)
                    time.sleep(1)
                except NoSuchElementException:
                    pass

                # Extract review text
                reviews.append(element.text.strip())
                
        except:
            print("No reviews found")

        # Get ratings
        ratings = []
        try:
            rating_elements = driver.find_elements(By.XPATH, ".//div[contains(@aria-label, 'Rated')]")
            for element in rating_elements[:5]:  # Get up to 5 ratings
                rating_text = element.get_attribute('aria-label')
                rating_value = rating_text.split(' ')[1]  # Extract the rating value
                ratings.append(rating_value)
        except:
            print("No ratings found")
        
        # Add reviews and ratings to gbp_data
        for i in range(5):
            gbp_data[f'review_{i+1}'] = reviews[i] if i < len(reviews) else ""
            gbp_data[f'review_rating_{i+1}'] = ratings[i] if i < len(ratings) else ""
        
        # Extract embedded images
        try:
            image_sources = extract_embedded_images(driver)
            gbp_data['gbp_embedded_url_1'] = image_sources[0] if len(image_sources) > 0 else ""
            gbp_data['gbp_embedded_url_2'] = image_sources[1] if len(image_sources) > 1 else ""
            gbp_data['gbp_embedded_url_3'] = image_sources[2] if len(image_sources) > 2 else ""
        except:
            gbp_data['gbp_embedded_url_1'] = ""
            gbp_data['gbp_embedded_url_2'] = ""
            gbp_data['gbp_embedded_url_3'] = ""
        
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
        'gbp_title', 'gbp_address', 'gbp_phone', 'gbp_website', 
        'gbp_image', 'gbp_map_image', 'gbp_outside_image',
        'gbp_maps_url', 'extra_fields',
        'review_1', 'review_2', 'review_3', 'review_4', 'review_5',
        'review_rating_1', 'review_rating_2', 'review_rating_3', 'review_rating_4', 'review_rating_5',
        'gbp_embedded_url_1', 'gbp_embedded_url_2', 'gbp_embedded_url_3'
    ]
    
    try:
        with open(filename, 'a', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            # Write header if file doesn't exist
            if not file_exists:
                writer.writeheader()
            
            # Convert extra_fields dictionary to string if it exists
            if 'extra_fields' in data and isinstance(data['extra_fields'], dict):
                data['extra_fields'] = str(data['extra_fields'])
            
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
        print(reviews)
        print(gbp_data)
        print("__________________________________________________________________")
        
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

def extract_embedded_images(driver):
    """Extract sources of the first embedded image normally and use a different XPath for the second and third images"""
    try:
        # Click on the initial image to open the modal
        gbp_image = driver.find_element(By.XPATH, GBP_XPATHS['gbp_image'])
        driver.execute_script("arguments[0].click();", gbp_image)
        
        # Wait for the modal to load
        time.sleep(6)

        # Find all embedded images
        embedded_images = driver.find_elements(By.XPATH, GBP_XPATHS['embedded_images'])

        # Initialize a list to store image sources
        image_sources = []

        # Get the first embedded image normally
        if embedded_images:
            driver.execute_script("arguments[0].click();", embedded_images[0])
            time.sleep(2)
            large_image = driver.find_element(By.XPATH, GBP_XPATHS['large_image'])
            image_sources.append(large_image.get_attribute('src'))

        # Use a different XPath for the second and third images
        additional_images = driver.find_elements(By.XPATH, "//img[@data-ils=3 and @jsaction='rcuQ6b:trigger.M8vzZb']")
        for img in additional_images[:2]:
            image_sources.append(img.get_attribute('src'))

        return image_sources
    except Exception as e:
        print(f"Error extracting embedded images: {str(e)}")
        return [] 