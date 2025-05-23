import pandas as pd

# Load the CSV file
df = pd.read_csv('restoration_listings_with_reviews.csv')

# Separate the 'gbp_image' column
gbp_image_df = df[['gbp_image']]

# Separate the rest of the columns
other_columns_df = df.drop(columns=['gbp_image'])

# Save the 'gbp_image' column to a new CSV file
gbp_image_df.to_csv('gbp_image.csv', index=False)

# Save the other columns to another new CSV file
other_columns_df.to_csv('other_columns.csv', index=False)

print("Columns have been separated and saved to 'gbp_image.csv' and 'other_columns.csv'.") 