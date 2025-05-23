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
    
    # List of URLs to process
    urls = [
        "https://pro.restorationindustry.org/directory-search?combine=&field_ams_geofield_proximity%5Bvalue%5D=100&field_ams_geofield_proximity%5Bsource_configuration%5D%5Borigin_address%5D=Connecticut+US%2C+United+States",
        "https://pro.restorationindustry.org/directory-search?combine=&field_ams_geofield_proximity%5Bvalue%5D=100&field_ams_geofield_proximity%5Bsource_configuration%5D%5Borigin_address%5D=Maine+US%2C+United+States",
        "https://pro.restorationindustry.org/directory-search?combine=&field_ams_geofield_proximity%5Bvalue%5D=100&field_ams_geofield_proximity%5Bsource_configuration%5D%5Borigin_address%5D=New+hampshire+US%2C+United+States"
    ]
    
    try:
        all_listings = []  # Store all listings data
        
        # First phase: Collect all listings from all URLs
        for url in urls:
            print(f"\nProcessing URL: {url}")
            driver.get(url)
            time.sleep(3)
            
            all_urls = []
            page_number = 1
            
            # Collect URLs from current starting URL
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
            
            print(f"\nTotal URLs collected from this starting URL: {len(all_urls)}")
            
            # Process each URL and extract details
            for index, listing_url in enumerate(all_urls, 1):
                print(f"\nProcessing listing {index}/{len(all_urls)}: {listing_url}")
                
                # Extract details from the listing
                listing_data = extract_listing_details(driver, listing_url)
                
                if listing_data:
                    all_listings.append(listing_data)  # Store the data instead of saving immediately
                    print(f"Successfully collected data for {listing_url}")
                else:
                    print(f"Failed to extract data for {listing_url}")
                
                # Add a small delay between requests
                time.sleep(1)
        
        # After collecting all listings, save them to CSV
        print("\nSaving all collected listings to CSV...")
        for listing_data in all_listings:
            save_to_csv(listing_data)
        print(f"Successfully saved {len(all_listings)} listings to CSV")
        
        # Second phase: Collect Google Business Profile reviews
        print("\nStarting Google Business Profile review collection...")
        update_csv_with_reviews(driver)
        print("\nReview collection completed!")
                
    except Exception as e:
        print(f"An error occurred: {str(e)}")
    
    finally:
        # Close the browser
        driver.quit()

if __name__ == "__main__":
    main() 