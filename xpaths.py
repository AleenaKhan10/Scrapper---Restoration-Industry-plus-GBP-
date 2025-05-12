# XPath selectors for the restoration industry website
LISTING_URLS = "//span[@class='field-content']/a"
NEXT_PAGE_BUTTON = "//a[@title='Go to next page']"

# Base URL for the website
BASE_URL = "https://pro.restorationindustry.org"

# Detailed information XPaths
DETAIL_XPATHS = {
    'title': "//h1[@class='page-header']",
    'phone': "//div[contains(@class,'field--name-field-ams-phone')]",
    'email': "//div[contains(@class,'field--name-field-ams-email')]",
    'organization': "//span[contains(@class,'organization')]",
    'address_line1': "//span[contains(@class,'address-line1')]",
    'address_line2': "//span[contains(@class,'address-line2')]",
    'locality': "//span[contains(@class,'locality')]",
    'administrative_area': "//span[contains(@class,'administrative-area')]",
    'postal_code': "//span[contains(@class,'postal-code')]",
    'country': "//span[contains(@class,'country')]",
    'about': "//div[contains(@class,'field--name-field-ams-ind-company-desc')]",
    'contact': "//div[contains(@class,'field--name-field-ams-master-contact')]",
    'description': "//div[contains(@class, 'field--name-field-ams-description-plain')]",
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
    'gbp_image': "//div[@id='rhs']//g-img[@class='ZGomKf']/img"
} 