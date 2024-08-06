import csv
import os  # Ensure the os module is imported
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time

def main():
    # Setup Chrome options
    options = Options()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    # Setup the Chrome service
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    # Open the target webpage
    newsgroup_url = "https://groups.google.com/g/net.news" #insert the link to the groupgroup here
    driver.get(newsgroup_url)

    # Extract newsgroup name and format it for filename
    newsgroup = newsgroup_url.split("/g/")[1].replace('.', '')
    csv_filename = f"{newsgroup}_threads.csv"

    # Ensure the output directory exists
    output_directory = '[INSERT FILE DIRECTORY PATH HERE]'
    os.makedirs(output_directory, exist_ok=True)

    # Determine the full output file path
    output_filepath = os.path.join(output_directory, csv_filename)

    # Initialize list to store all thread data
    all_threads = []
    total_threads = 0  # To store the total number of threads

    try:
        # Extract the total number of threads from the page
        time.sleep(5)  # Ensure the page loads
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        total_threads_element = soup.find("div", class_="aEb7Ed")
        if total_threads_element:
            total_threads_text = total_threads_element.text.split()[-1]
            total_threads = int(total_threads_text.replace(",", ""))  # Remove commas and convert to int
            print(f"Total threads: {total_threads}")

        # Set starting counter for IDs
        thread_id_counter = total_threads

        while thread_id_counter > 0:
            # Extract the page's HTML and parse it
            soup = BeautifulSoup(driver.page_source, 'html.parser')

            # Find all thread entries on the page
            threads = soup.find_all("div", role="row")
            for thread in threads:
                try:
                    title_element = thread.find("span", class_="o1DPKc")
                    link_element = thread.find("a", class_="ZLl54")
                    date_element = thread.find("div", class_="tRlaM")
                    messages_element = thread.find("span", class_="F5JnCe")

                    if title_element and link_element and date_element:
                        title = title_element.text.strip()
                        link = 'https://groups.google.com' + link_element['href']
                        date = date_element.text.strip()

                        # Extract the number of messages from the text content if present
                        if messages_element:
                            messages = messages_element.text.strip()  # Directly use the text content
                        else:
                            messages = "1"  # Default to 1 if the F5JnCe class is not present

                        # Generate zero-padded unique ID for the thread, counting backwards
                        unique_id = f"TH{str(thread_id_counter).zfill(5)}"
                        thread_id_counter -= 1

                        # Append data including unique ID
                        all_threads.append((unique_id, title, link, date, messages))

                        # Stop if all threads are collected
                        if thread_id_counter <= 0:
                            break
                    else:
                        print("Missing element in thread. Title, Link, or Date not found.")
                except Exception as e:
                    print(f"Error processing thread details: {e}")
            else:
                # Find and click the 'Next page' button
                try:
                    # Wait for the next button to be clickable and then click it
                    next_button = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, 'div[role="button"][aria-label="Next page"]'))
                    )
                    next_button.click()
                    time.sleep(5)  # Ensure the next page loads
                except Exception as e:
                    print(f"Error clicking the next page button: {e}")
                    break
                continue
            break  # Exit the loop after collecting all threads

    except Exception as e:
        print(f"An error occurred while navigating pages or processing data: {e}")
    finally:
        # Save all collected thread data to a CSV file
        with open(output_filepath, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['ThreadID', 'Thread Title', 'URL', 'Date', 'Number of Messages'])  # Write CSV header
            writer.writerows(all_threads)

        print(f"Data successfully written to {output_filepath}")

        # Close the browser
        driver.quit()

if __name__ == "__main__":
    main()
