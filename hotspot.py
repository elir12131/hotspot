import random
import string
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Function to generate a random string of four lowercase letters
def generate_random_string(length=4):
    return ''.join(random.choice(string.ascii_lowercase) for _ in range(length))

# Initialize the WebDriver
driver = webdriver.Chrome()  # Ensure you have ChromeDriver installed

# Open the form URL
driver.get("https://www.t-mobile.com/brand/project-10-million-form/start")

# Allow time for the page to fully load
time.sleep(3)  # Adjust the time if necessary

# Define student information
first_name = "Eli"
last_name = "Roitblat " + generate_random_string()  # Added a space after "Roitblat"
email = "johndoe@example.com"
confirm_email = "johndoe@example.com"
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
            except:
                print(f"Retrying to fill field '{field_id}' (attempt {attempt + 1})...")

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

    # Optionally submit the form
    # WebDriverWait(driver, 10).until(
    #     EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']"))
    # ).click()

    # Pause to review the filled form
    time.sleep(5)

finally:
    # Close the driver after the operation
    driver.quit()
