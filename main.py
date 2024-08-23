from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import re
import os

# Path to your chromedriver executable
chromedriver_path = 'chromedriver.exe'

# Set up Chrome options (if needed)
chrome_options = Options()
# Set up the Service object
service = Service(executable_path=chromedriver_path)

# Initialize the WebDriver with the Service object and options
driver = webdriver.Chrome(service=service, options=chrome_options)

# Open Statista URL
url = 'https://www.statista.com/statistics/265759/world-population-by-age-and-region/'  # Replace with your target URL
driver.get(url)

# WebDriverWait to handle dynamic content
wait = WebDriverWait(driver, 10)  # 10 seconds timeout

# Function to log in
def login(username, password):
    try:
        # Handle "Allow Cookies" popup manually
        print("Please handle the 'Allow Cookies' popup manually, then press Enter to continue...")
        input("Press Enter after handling the cookies popup...")

        # Click the login button
        login_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="main"]/header/div/div/div/div[1]/div[2]/div[1]/nav/ul/li[3]/form/input')))
        login_button.click()

        # Input the username
        username_field = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="loginStat_username"]')))
        username_field.send_keys(username)

        # Input the password
        password_field = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="loginStat_password"]')))
        password_field.send_keys(password)

        # Submit the login form
        submit_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="loginStat_submitLogin"]')))
        submit_button.click()

        # Wait for the page to load after login
        wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="statisticContainer"]')))
        print("Logged in successfully.")

    except Exception as e:
        print("Failed to log in:", e)
        driver.quit()

# Function to extract number of entries (rows) in the table
def no_of_entries():
    try:
        # Locate the div element and extract its text
        div_element = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="tableContainer"]/div/div/div/div[2]/div')))  # Replace with your actual XPath
        div_text = div_element.text

        # Extract all numbers from the text using regular expressions
        numbers = [int(num) for num in re.findall(r'\d+', div_text)]

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

# def convert_chart_to_datapoints(number_of_rows):
#     try:
#         # Step 1: Click the settings button on the chart
#         settings_button_xpath = '//*[@id="statisticContainer"]/div[2]/div/div[1]/div[3]/button'
#         settings_button = wait.until(EC.element_to_be_clickable((By.XPATH, settings_button_xpath)))
#         settings_button.click()
#         WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.XPATH, '//*[@id="statisticContainer"]/div[2]/div/div[2]/div/div/fieldset[1]/div[1]/button[3]')))

#         # Step 2: Select the option to view data points
#         data_points_option_xpath = '//*[@id="statisticContainer"]/div[2]/div/div[2]/div/div/fieldset[1]/div[1]/button[3]'
#         data_points_option = wait.until(EC.element_to_be_clickable((By.XPATH, data_points_option_xpath)))
#         data_points_option.click()
        
#         # Optional: Wait a bit longer if the data takes time to load
#         time.sleep(5)  # Adjust the sleep duration if needed

#         # Step 3: Close the settings or data points view if necessary
#         close_button_xpath = '//*[@id="statisticContainer"]/div[2]/div/div[2]/div/button'
#         close_button = wait.until(EC.element_to_be_clickable((By.XPATH, close_button_xpath)))
#         close_button.click()

#         # Step 4: Scrape the data points from the table
#         data = []

#         for i in range(1, number_of_rows + 1):  # Loop through each row
#             row_xpath = f'//*[@id="data-table-1724315321850"]/tbody/tr[i]/td[i]'
            
#             # //*[@id="data-table-1724381536584"]/tbody/tr[1]/td[1]
#             # //*[@id="data-table-1724381536584"]/tbody/tr[1]/td[1]/span
            
            
#             try:
#                 row = wait.until(EC.presence_of_element_located((By.XPATH, row_xpath)))
#                 span_elements = row.find_elements(By.XPATH, '/span')
#                 row_data = [span.text for span in span_elements]

#                 if row_data:
#                     data.append(row_data)
#                 else:
#                     print(f"Row {i} is empty.")
#             except Exception as row_e:
#                 print(f"Failed to locate row {i}: {row_e}")

#         # Convert the extracted data to a DataFrame
#         if data:
#             df = pd.DataFrame(data)
#             return df
#         else:
#             print("No data found.")
#             return None

#     except Exception as e:
#         print("Failed to convert chart to data points:", e)
#         return None



def convert_chart_to_datapoints(number_of_rows):
    try:
        # Step 1: Click the settings button on the chart
        settings_button_xpath = '//*[@id="statisticContainer"]/div[2]/div/div[1]/div[3]/button'
        settings_button = wait.until(EC.element_to_be_clickable((By.XPATH, settings_button_xpath)))
        settings_button.click()
        WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.XPATH, '//*[@id="statisticContainer"]/div[2]/div/div[2]/div/div/fieldset[1]/div[1]/button[3]')))

        # Step 2: Select the option to view data points
        data_points_option_xpath = '//*[@id="statisticContainer"]/div[2]/div/div[2]/div/div/fieldset[1]/div[1]/button[3]'
        data_points_option = wait.until(EC.element_to_be_clickable((By.XPATH, data_points_option_xpath)))
        data_points_option.click()
        
        # Optional: Wait a bit longer if the data takes time to load
        time.sleep(5)  # Adjust the sleep duration if needed
        
        #  Step 3: Close the settings or data points view if necessary
        close_button_xpath = '//*[@id="statisticContainer"]/div[2]/div/div[2]/div/button'
        close_button = wait.until(EC.element_to_be_clickable((By.XPATH, close_button_xpath)))
        close_button.click()
        
        time.sleep(30)

        # Step 3: Scrape the data points from the table
        data = []

        for i in range(1, number_of_rows + 1):  # Loop through each row
            row_xpath = f'//*[@id="data-table-1724381536584"]/tbody/tr[{i}]'  # Adjust the XPath to match the correct table ID
            print(row_xpath)
            
            try:
                row = wait.until(EC.presence_of_element_located((By.XPATH, row_xpath)))
                # Find all span elements within the row
                span_elements = row.find_elements(By.XPATH, './/td/span')
                row_data = [span.text for span in span_elements]

                if row_data:
                    data.append(row_data)
                else:
                    print(f"Row {i} is empty or does not contain span elements.")
            except Exception as row_e:
                print(f"Failed to locate row {i}: {row_e}")

        # Convert the extracted data to a DataFrame
        if data:
            df = pd.DataFrame(data)
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

# Credentials
username = 'siddhanth.moraje288@svkmmumbai.onmicrosoft.com'  # Replace with your actual username
password = 'siddhanth@21'  # Replace with your actual password

# Log in
login(username, password)

# Get the number of rows (entries)
number_of_rows = 7 #changed
print(number_of_rows)

# Example of scraping multiple charts
dataframes = []
descriptions = []

 # Example: loop over multiple charts
try:
    print(f"Processing chart...")
        
        # Convert chart to data points using the number of rows
    df = convert_chart_to_datapoints(number_of_rows)
    if df is not None:
        dataframes.append(df)
        print(f"Chart data points extracted successfully.")
    else:
        print(f"Chart  data points extraction failed.")

        # Extract description
    desc = extract_description()
    if desc:
        descriptions.append(desc)
        print(f"Chart  description extracted successfully.")
    else:
        print(f"Chart  description extraction failed.")
    
except Exception as e:
    print(f"Failed to scrape chart : {e}")

# Combine DataFrames or process data further as needed
if dataframes:
    final_df = pd.concat(dataframes, ignore_index=True)
    final_df.to_csv('statista_data.csv', index=False)
    print("CSV file has been created successfully.")
else:
    print("No data to save to CSV.")

# Print descriptions
for i, desc in enumerate(descriptions):
    print(f"Description {i+1}: {desc}")

# Print current working directory
print("Current Working Directory:", os.getcwd())

# Close the WebDriver
driver.quit()
