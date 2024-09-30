#sab hogaya

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import re
import os
import json

# Path to your chromedriver executable
# chromedriver_path = r'./chromedriver.exe'

# Set up Chrome options (if needed)
chrome_options = Options()
# Set up the Service object
# service = Service(executable_path=chromedriver_path)

# Initialize the WebDriver with the Service object and options
driver = webdriver.Chrome(options=chrome_options)


# https://www.statista.com/statistics/265759/world-population-by-age-and-region/
# Open Statista URL

# topic_list = ['geography+chart','Demographics','Education+and+science','geography+and+nature','Aviation','Public+transportation+and+mobility+Services','Rail+Transport','Vehicles+and+Road+Traffic','Water+transport']

# for i in topic_list:
#     url = f'https://www.statista.com/search/?q={i}&p=1&tabGroup=statistic'  # Replace with your target URL
#     driver.get(url)

# WebDriverWait to handle dynamic content
wait = WebDriverWait(driver, 10)  # 10 seconds timeout

# Function to log in
def login(username, password,url1):
    try:
        # Handle "Allow Cookies" popup manually
        print("Please handle the 'Allow Cookies' popup manually, then press Enter to continue...")
        input("Press Enter after handling the cookies popup...") 

        # Click the login button
        login_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="main"]/header/div/div/div/div[1]/div[2]/div[1]/nav/ul/li[3]/form/input')))
        print('login button')
        login_button.click()

        # Input the username
        username_field = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="username"]')))
        print('username')
        username_field.send_keys(username)

        # Input the password
        password_field = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="password"]')))
        print('password')
        password_field.send_keys(password)

        # Submit the login form
        submit_button = wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/main/section/div/div/div/form/div[4]/button')))
        print('sbmit btns')
        submit_button.click()
        
        driver.execute_script("window.open('');") 
        driver.switch_to.window(driver.window_handles[1]) 
        driver.get(url1)

        # Wait for the page to load after login
        wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="resultRow"]')))
        print("Logged in successfully.")

    except Exception as e:
        print("Failed to log in:", e)
        driver.quit()

# Function to extract number of entries (rows) in the table and for number of pages
def no_of_entries(path):
    try:
        # Locate the div element and extract its text
        time.sleep(5)
        div_element = wait.until(EC.presence_of_element_located((By.XPATH,path))).text  # Replace with your actual XPath
        # div_element = driver.find_element(By.XPATH, '/html/body/div[4]/main/section[2]/div[2]/article[3]/div[2]/div[1]/div[1]/article/div/div/div[1]/div/div/div/div[2]/div')
        time.sleep(2)
        # div_text = div_element.text
        
        print(div_element)

        # Extract all numbers from the text using regular expressions
        numbers = [int(num) for num in re.findall(r'\d+', div_element)]
        print(numbers)

        # Find the greatest number (which represents the number of rows)
        greatest_number = max(numbers) if numbers else None

        if greatest_number is not None:
            print(f"The greatest number in the div text is: {greatest_number}")
            return greatest_number
        else:
            print("No numbers found in the div text.")
            return 0

    except Exception as e:
        print("An error occurred:", e)
        return 0

# Function to convert chart to data points
import time

def convert_chart_to_datapoints():
    try:
        
        # # Step 1: Extract the title of the table
        # title_xpath = '/html/body/div[4]/main/section[2]/div[2]/article[2]/h2/span'
        # title_element = driver.find_element(By.XPATH, title_xpath)
        # table_title = title_element.text
        # print(f"Table Title: {table_title}")
                
        # Step : Click the settings button on the chart
        settings_button_xpath = '//*[@id="statisticContainer"]/div[2]/div/div[1]/div[3]/button'
        #//*[@id="statisticContainer"]/div[2]/div/div[1]/div[3]/button
        settings_button = wait.until(EC.element_to_be_clickable((By.XPATH, settings_button_xpath)))
        settings_button.click()
        WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.XPATH, '//*[@id="statisticContainer"]/div[2]/div/div[2]/div/div/fieldset[1]/div[1]/button[3]')))
        print('settings button hit')
        time.sleep(3)

        # Step 2: Select the option to view data points
        print('i am here, trying to directly hit the data point')
        data_points_option_xpath = '//*[@id="statisticContainer"]/div[2]/div/div[2]/div/div/fieldset[1]/div[1]/button[3]'
        data_points_options_xpath_trial = '/html/body/div[4]/main/section[2]/div[2]/article[3]/div[2]/div[1]/div[2]/div/div[2]/div/div/fieldset[1]/div[1]/button[3]'
        #//*[@id="statisticContainer"]/div[2]/div/div[2]/div/div/fieldset[1]/div[1]/button[3]
        data_points_option = driver.find_element(By.XPATH, data_points_options_xpath_trial)
        print(data_points_option)
        print(type(data_points_option))
        print('options')
        time.sleep(2)
        data_points_option.click()
        print('data option hit')
        
        # Optional: Wait a bit longer if the data takes time to load
        time.sleep(5)  # Adjust the sleep duration if needed
        
        #  Step 3: Close the settings or data points view if necessary
        close_button_xpath = '//*[@id="statisticContainer"]/div[2]/div/div[2]/div/button'
        close_button = wait.until(EC.element_to_be_clickable((By.XPATH, close_button_xpath)))
        close_button.click()
        print('close button hit')
        
        dropdown_element = driver.find_element(By.XPATH, '/html/body/div[4]/main/section[2]/div[2]/article[3]/div[2]/div[1]/div[1]/article/div/div/div[1]/div/div/div/div[1]/label/select')  # Replace the XPath if necessary

# Create a Select object based on the located dropdown element
        dropdown = Select(dropdown_element)

# Select the last option
        dropdown.select_by_index(len(dropdown.options) - 1)
        
        # time.sleep(30)
        # Get the number of rows (entries)
        number_of_rows = no_of_entries("/html/body/div[4]/main/section[2]/div[2]/article[3]/div[2]/div[1]/div[1]/article/div/div/div[1]/div/div/div/div[2]/div") #changed
        time.sleep(5)
        print(number_of_rows)
        
        # Step: Extract the column names dynamically
        column_names = []
        header_xpath = '/html/body/div[4]/main/section[2]/div[2]/article[3]/div[2]/div[1]/div[1]/article/div/div/div[1]/div/div/div/table/thead/tr/th'
        header_elements = driver.find_elements(By.XPATH, header_xpath)
        for header in header_elements:
            column_names.append(header.text)

        print(f"Column Names: {column_names}")
        
        # Step 3: Scrape the data points from the table
        data = []

        for i in range(1, number_of_rows+1):  # Loop through each row
            #//*[@id="data-table-1724445746147"]/tbody/tr[1]
            #/html/body/div[4]/main/section[2]/div[2]/article[3]/div[2]/div[1]/div[1]/article/div/div/div[1]/div/div/div/table/tbody/tr[1]
            row_xpath = f'/html/body/div[4]/main/section[2]/div[2]/article[3]/div[2]/div[1]/div[1]/article/div/div/div[1]/div/div/div/table/tbody/tr[{i}]'  # Adjust the XPath to match the correct table ID
            print(row_xpath)
            
            try:
                print('enter try loop')
                row = driver.find_element(By.XPATH, row_xpath)
                # print(row, 'found')
                # Find all span elements within the row
                span_elements = row.find_elements(By.XPATH, './/td/span')
                # print(span_elements, 'found')
                row_data = [span.text for span in span_elements]

                if row_data:
                    data.append(row_data)
                else:
                    print(f"Row {i} is empty or does not contain span elements.")
            except Exception as row_e:
                print(f"Failed to locate row {i}: {row_e}")

        # Convert the extracted data to a DataFrame
        if data:
            df = pd.DataFrame(data , columns=column_names)
            return df
        else:
            print("No data found.")
            return None

    except Exception as e:
        print("Failed to convert chart to data points:", e)
        return None


# Function to extract description
def extract_description():
    try:
        description = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="readingAidText"]'))).text
        return description
    except Exception as e:
        print("Failed to extract description:", e)
        return None
    
    
    
    # /html/body/div[4]/main/section[2]/section/div[1]/section[2]/div/div/div/div[1]/div/div[1]/a
    # /html/body/div[4]/main/section[2]/section/div[1]/section[2]/div/div/div/div[2]/div[1]/div[1]/a
    

def extract_links():
    
    last_page_no = '//*[@id="searchPaginator"]/div/div/ul/li[4]'
    total_page_no = no_of_entries(last_page_no) 
    print(f'total page number is {total_page_no}')
        
    links = []
    
    try:
        div_path = '/html/body/div[4]/main/section[2]/section/div[1]/section[2]/div/div/div'
        div = driver.find_element(By.XPATH, div_path)
        for i in range(0,total_page_no):
            for i in range(1, 25):
            
                 try:
                     div_links = div.find_elements(By.XPATH, f'.//div[{i}]/div[1]/div[1]/a')
                     for l in div_links:
                         links.append(l.get_attribute('href')) 
                 except Exception as e:
                     print(f"Failed to extract link from div[{i}]:", e)
            try:
                next_button_xpath = '//*[@id="searchPaginator"]/div/div/ul/li[5]/button'
                button = wait.until(EC.element_to_be_clickable((By.XPATH, next_button_xpath)))
                button.click()
                
            except Exception as e: 
                print("Failed to click button:",e)
                
            

    except Exception as e:
        print("Failed to locate the main div:", e)
    
    print(links)
    return links if links else None
 
# Initialize a list to hold all chart data
all_chart_data = []

def iterate_links(links):
    # Initialize a flag to control writing headers in the first iteration only
    is_first_iteration = True

    # Initialize a list to hold all chart data
    all_chart_data = []
    
    for url in links:
        try:
            driver.execute_script("window.open('');") 
            driver.switch_to.window(driver.window_handles[1]) 
            driver.get(url) 

            elements = driver.find_elements(By.XPATH, '/html/body/div[4]/main/section[2]/div[1]/div/div[1]/div[1]/a')
            if not elements:
                print("Not a premium content, proceeding to scrape data...")

                df = convert_chart_to_datapoints()
                if df is not None:
                   # Extract table title for the topic name 
                    topic_name = extract_title()
                    
                    # Dynamically store the column names and their corresponding data
                    columns_data = {}
                    for col in df.columns:
                        columns_data[col] = df[col].astype(str).tolist()
                    
                    description = extract_description()
                    

                    # Create a structured dictionary for this chart
                    data_to_save = {
                        "Chart": {
                            "Topic": topic_name,
                            "Columns": columns_data,
                            "Description": description
                        }
                    }

                    # Append this chart's data to the list
                    all_chart_data.append(data_to_save)

            driver.close() 
            driver.switch_to.window(driver.window_handles[0])

        except Exception as e:
            print("Failed to open link:", e)
            continue

    # Save all chart data to a single JSON file
    save_to_json(all_chart_data, filename='statista_data.json')
    
def save_to_json(data, filename='statista_data_with_descriptions.json'):
    with open(filename, 'w') as json_file:
        json.dump(data, json_file, indent=4)
    print(f"Data saved to {filename} successfully.")    
  
def extract_title():
    try:
        # Extract the title of the table (topic name)
        title_xpath = '/html/body/div[4]/main/section[2]/div[2]/article[2]/h2/span'
        title_element = driver.find_element(By.XPATH, title_xpath)
        table_title = title_element.text
        return table_title
    except Exception as e:
        print("Failed to extract title:", e)
        return "Unknown Topic" 
    
    

# Credentials
username = 'siddhanth.moraje288@svkmmumbai.onmicrosoft.com'  # Replace with your actual username
password = 'siddhanth@21'  # Replace with your actual password
counter = 0
topic_list = ['geography+chart'] #Demographics
#'geography+chart','Education+and+science','geography+and+nature','Aviation','Public+transportation+and+mobility+Services','Rail+Transport','Vehicles+and+Road+Traffic','Water+transport'


for i in topic_list:
    url = f'https://www.statista.com/search/?q={i}&p=1&tabGroup=statistic'  # Replace with your target URL
    driver.get(url)
    

    if counter==0:
        login(username, password,url)
        time.sleep(3)
        counter = 1
    try:
       links = extract_links()
       print(links)
    except Exception as e:
        print("Failed to extract links:", e)
    time.sleep(3)

    iterate_links(links)

# Save all data to JSON
    save_to_json(all_chart_data)

# Print current working directory
print("Current Working Directory:", os.getcwd())

# Close the WebDriver
driver.quit()