from driver_setup import setup_driver
from xpaths import LISTING_URLS, NEXT_PAGE_BUTTON, BASE_URL
from functions import (
    get_listing_urls, click_next_page, extract_listing_details,
    save_to_csv, update_csv_with_reviews
)
import time

def main():
    # Initialize the driver
    driver = setup_driver()
    
    try:
        # Navigate to the initial URL
        initial_url = f"{BASE_URL}/directory-search?combine=&field_ams_geofield_proximity%5Bvalue%5D=100&field_ams_geofield_proximity%5Bsource_configuration%5D%5Borigin_address%5D=New%20York%20US%2C%20United%20States&page=0"
        driver.get(initial_url)
        
        # Wait for initial page load
        time.sleep(3)
        
        all_urls = []
        page_number = 1
        
        # First, collect all URLs
        while True:
            print(f"Scraping page {page_number}...")
            
            # Get URLs from current page
            page_urls = get_listing_urls(driver, LISTING_URLS)
            all_urls.extend(page_urls)
            
            print(f"Found {len(page_urls)} URLs on page {page_number}")
            
            # Try to click next page
            if not click_next_page(driver, NEXT_PAGE_BUTTON):
                print("Reached last page")
                break
                
            page_number += 1
        
        print(f"\nTotal URLs collected: {len(all_urls)}")
        
        # Now process each URL and extract details
        for index, url in enumerate(all_urls, 1):
            print(f"\nProcessing listing {index}/{len(all_urls)}: {url}")
            
            # Extract details from the listing
            listing_data = extract_listing_details(driver, url)
            
            if listing_data:
                # Save to CSV
                save_to_csv(listing_data)
                print(f"Successfully saved data for {url}")
            else:
                print(f"Failed to extract data for {url}")
            
            # Add a small delay between requests
            time.sleep(1)
        
        print("\nStarting Google Business Profile review collection...")
        # Update CSV with Google reviews
        update_csv_with_reviews(driver)
        print("\nReview collection completed!")
            
    except Exception as e:
        print(f"An error occurred: {str(e)}")
    
    finally:
        # Close the browser
        driver.quit()

if __name__ == "__main__":
    main() 