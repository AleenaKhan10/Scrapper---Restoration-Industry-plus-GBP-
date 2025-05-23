import csv
import os
import requests
from urllib.parse import urlparse

def download_image(image_url, save_path):
    try:
        response = requests.get(image_url, stream=True)
        if response.status_code == 200:
            with open(save_path, 'wb') as out_file:
                for chunk in response.iter_content(1024):
                    out_file.write(chunk)
            return save_path
        else:
            print(f"Failed to download image: {image_url}")
            return None
    except Exception as e:
        print(f"Error downloading image: {e}")
        return None

def process_csv(input_csv, output_csv, image_folder):
    if not os.path.exists(image_folder):
        os.makedirs(image_folder)

    with open(input_csv, mode='r', newline='', encoding='utf-8') as infile,\
         open(output_csv, mode='w', newline='', encoding='utf-8') as outfile:
        
        reader = csv.DictReader(infile)
        fieldnames = reader.fieldnames + ['image_path']
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        
        writer.writeheader()
        
        for row in reader:
            try:
                image_url = row['image_url']
                name = row['name']
                image_name = f"{name}_image.jpg"
                image_path = os.path.join(image_folder, image_name)
                
                downloaded_image_path = download_image(image_url, image_path)
                if downloaded_image_path:
                    row['image_path'] = downloaded_image_path
                else:
                    row['image_path'] = ''
                
                # Write each row immediately after processing
                writer.writerow(row)
                
            except Exception as e:
                print(f"Error occurred while processing {row}")
                print(e)
                # Write the row even if there was an error
                writer.writerow(row)

# Example usage
input_csv = 'input.csv'
output_csv = 'output.csv'
image_folder = 'downloaded_images'
process_csv(input_csv, output_csv, image_folder)
