import pandas as pd
import requests
from bs4 import BeautifulSoup
import os

# Function to extract comments from a given URL
def extract_comments(url, thread_id):
    comments_data = []
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    comments = soup.find_all('section', class_='BkrUxb')  # Find all comment sections

    for i, comment in enumerate(comments):
        comment_id = f"CM{i + 1:05}"
        unique_comment_id = f"{thread_id}_{comment_id}"

        # Extracting author name
        author_tag = comment.find('h3', class_='s1f8Zd')
        author_name = author_tag.get_text() if author_tag else "Unknown"

        # Extracting date and time
        date_tag = comment.find('span', class_='zX2W9c')
        date_time = date_tag.get_text() if date_tag else "Unknown"

        # Extracting full text
        text_tag = comment.find('div', class_='ptW7te')
        full_text = text_tag.get_text(separator='\n').strip() if text_tag else "No text"

        # Extracting data-doc-id (url-string)
        data_doc_id = comment.get('data-doc-id', 'Unknown')

        # Storing the extracted data
        comment_data = {
            'Thread ID': thread_id,
            'Comment ID': comment_id,
            'Unique Comment ID': unique_comment_id,
            'Author': author_name,
            'Date and Time': date_time,
            'Full Text': full_text,
            'URL String': data_doc_id
        }
        comments_data.append(comment_data)

    return comments_data

# Main function to process the CSV file
def process_csv(input_csv_path):
    # Load the CSV file
    data = pd.read_csv(input_csv_path)

    # Check if the required columns exist
    required_columns = ['ThreadID', 'URL']
    for col in required_columns:
        if col not in data.columns:
            print(f"Error: Column '{col}' not found in the CSV file. Available columns: {data.columns}")
            return

    # Determine the output CSV file name
    base_name = os.path.basename(input_csv_path)
    output_base_name = base_name.replace('_threads', '_comments')
    output_directory = '[INPUT YOUR FILE DIRECTORY HERE]'
    output_csv_path = os.path.join(output_directory, output_base_name)

    # Iterate over each URL and collect comments
    all_comments = []
    for idx, row in data.iterrows():
        thread_id = row['ThreadID']  # Assuming the CSV has a 'ThreadID' column
        url = row['URL']
        comments = extract_comments(url, thread_id)
        all_comments.extend(comments)

        # Print progress every 50 links
        if (idx + 1) % 50 == 0:
            print(f"Processed {idx + 1} URLs...")

    # Convert the list of comments to a DataFrame and save to CSV
    comments_df = pd.DataFrame(all_comments)
    comments_df.to_csv(output_csv_path, index=False)
    print(f"Comments successfully saved to {output_csv_path}")

# Example usage with the provided file path
input_csv_path = '[INPUT CSV FILE PATH HERE]'  # Replace with your actual path
process_csv(input_csv_path)
