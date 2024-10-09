import random
import string
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Function to generate a random string of four lowercase letters
def generate_random_string(length=4):
    return ''.join(random.choice(string.ascii_lowercase) for _ in range(length))

# Function to generate a Mailinator email address
def generate_mailinator_email():
    # Generate a random username for the email
    random_username = f"testuser{generate_random_string()}"
    return f"{random_username}@mailinator.com"

# Function to check for new emails from Mailinator
def fetch_mailinator_emails(email):
    inbox_url = f"https://api.mailinator.com/v2/inbox?to={email.split('@')[0]}"
    response = requests.get(inbox_url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

# Initialize the WebDriver
driver = webdriver.Chrome()  # Ensure you have ChromeDriver installed

# Open the form URL
driver.get("https://www.t-mobile.com/brand/project-10-million-form/start")

# Allow time for the page to fully load
time.sleep(3)  # Adjust the time if necessary

# Define student information
first_name = "Eli"
last_name = "Roitblat " + generate_random_string()  # Added space after "Roitblat"
email = generate_mailinator_email()  # Generate a Mailinator email
confirm_email = email  # Use the same email for confirmation
store_id = "12345"  # If this is needed and applicable

try:
    # Function to fill a field with retries in case of stale elements
    def fill_field(field_id, value):
        retries = 5
        for attempt in range(retries):
            try:
                element = WebDriverWait(driver, 10).until(
                    EC.visibility_of_element_located((By.ID, field_id))
                )
                element.clear()  # Clear any existing text
                element.send_keys(value)
                break  # Exit the loop if successful
            except Exception as e:
                print(f"Retrying to fill field '{field_id}' (attempt {attempt + 1})... Error: {e}")

    # Input first name
    fill_field("firstName", first_name)

    # Input last name with random letters appended
    fill_field("lastName", last_name)

    # Input email
    fill_field("email", email)

    # Confirm email
    fill_field("confirmEmail", confirm_email)

    # Input store ID (use JavaScript if the element is not interactable)
    try:
        store_id_element = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "storeId"))
        )
        store_id_element.clear()
        store_id_element.send_keys(store_id)
    except:
        # Fallback to JavaScript for hidden or non-interactable elements
        driver.execute_script("document.getElementById('storeId').value = arguments[0];", store_id)

    # Click the continue button using a more accurate selector
    try:
        continue_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'cta-button') and contains(., 'Continue')]"))
        )
        continue_button.click()
    except Exception as e:
        print(f"Error clicking continue button: {e}")

    # Pause to allow the next page to load or handle any additional steps
    time.sleep(5)

    # Fetch emails sent to the generated Mailinator address
    emails = fetch_mailinator_emails(email)
    print(emails)  # Print the fetched emails for review

finally:
    # Close the driver after the operation
    driver.quit()
