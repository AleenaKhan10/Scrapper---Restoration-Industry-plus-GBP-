# XPath selectors for the restoration industry website
LISTING_URLS = "//span[@class='field-content']/a"
NEXT_PAGE_BUTTON = "//a[@title='Go to next page']"

# Base URL for the website
BASE_URL = "https://pro.restorationindustry.org"

# Detailed information XPaths
DETAIL_XPATHS = {
    'title': "//h1[@class='page-header']",
    'phone': "//div[contains(@class,'field--name-field-ams-phone')]/div[2]",
    'email': "//div[contains(@class,'field--name-field-ams-email')]/div[2]",
    'organization': "//span[contains(@class,'organization')]",
    'address_line1': "//span[contains(@class,'address-line1')]",
    'address_line2': "//span[contains(@class,'address-line2')]",
    'locality': "//span[contains(@class,'locality')]",
    'administrative_area': "//span[contains(@class,'administrative-area')]",
    'postal_code': "//span[contains(@class,'postal-code')]",
    'country': "//span[contains(@class,'country')]",
    'about': "//div[contains(@class,'field--name-field-ams-ind-company-desc')]/div[2]",
    'contact': "//div[contains(@class,'field--name-field-ams-master-contact')]/div[2]",
    'description': "//div[contains(@class, 'field--name-field-ams-description-plain')]/div[2]",
    'website': "//div[contains(@class, 'field--name-field-ams-website-url')]/div/a"
}

# Google Business Profile XPaths
GBP_XPATHS = {
    'reviews_button': "//span[text()='Reviews']",
    'review_text': "//div[@class='OA1nbd']",
    'gbp_title': "//div[@id='rhs']//div[@data-attrid='title'] | //h2[@data-attrid='title']",
    'gbp_address': "//div[@id='rhs']//span[@class='LrzXr']",
    'gbp_phone': "//div[@id='rhs']//span[contains(@aria-label, 'Call phone number')]",
    'gbp_website': "//div[@id='rhs']//a[@class='n1obkb mI8Pwc']",
    'gbp_image': "//div[@class='nmrhhd luib-5']//div[./span[text()='See photos']]//img",
    'gbp_map_image': "//img[contains(@alt, 'Map of')]",
    'gbp_outside_image': "//div[@class='nmrhhd luib-5']//div[.//span[text()='See outside']]//img",
    'gbp_cid_link': "//div/span/a[contains(@href,'cid=')]",
    'embedded_images': "//div[@aria-label='Photo gallery']//img[not(contains(@src, 'https://streetviewpixels'))]",
    'large_image': "//img[contains(@jsaction,'load:trigger')]"
}

# XPath for extra fields
EXTRA_FIELDS_XPATH = "//div[contains(@class, 'field field--name-field')]"

# List of standard fields to ignore when processing extra fields
STANDARD_FIELDS = {
    'Contact', 'Address', 'Title', 'Website', 'Email', 
    'Phone', 'About', 'Organization', 'Description'
} 