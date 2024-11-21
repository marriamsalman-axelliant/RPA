import os
import time
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager


def driver_shell_onboarding(
    first_name, last_name, email, driver_license, license_expiry_date, phone_number
):
    chromedriver_path = "/home/marriam/Downloads/k/chromedrivernn"
    user_data_dir = "/home/marriam/Downloads/d/chrome-user-data"

    # Chrome options
    chrome_options = Options()
    chrome_options.add_argument(f"--user-data-dir={user_data_dir}")
    chrome_options.add_argument("--profile-directory=Default")
    chrome_options.add_argument("--start-maximized")

    # Start ChromeDriver
    service = Service(chromedriver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        # WebDriverWait instance
        wait = WebDriverWait(driver, 10)

        try:
            driver.get("https://mylocation.org")
            driver.save_screenshot("ip_for_shell.png")

            driver.get("https://shellaccountmanager.ca/home")
            driver.maximize_window()
            print(driver.title)
            time.sleep(10)
            # some issue here need to check it
            if "https://www.shellaccountmanager.ca/login" in driver.current_url:

                print("Logging in...")
                username_field = wait.until(
                    EC.presence_of_element_located((By.ID, "okta-signin-username"))
                )
                username_field.send_keys(os.getenv("SHELL_USERNAME"))
                time.sleep(3)
                password_field = wait.until(
                    EC.presence_of_element_located((By.ID, "okta-signin-password"))
                )
                password_field.send_keys(os.getenv("SHELL_PASSWORD"))
                time.sleep(2)
                login_button = wait.until(
                    EC.element_to_be_clickable((By.ID, "okta-signin-submit"))
                )
                login_button.click()
                time.sleep(5)

                try:
                    # Wait for multi-factor authentication (MFA) approval
                    print("Waiting for MFA approval...")
                    push_button = wait.until(
                        EC.element_to_be_clickable(
                            (
                                By.CSS_SELECTOR,
                                "input.button.button-primary[type='submit']",
                            )
                        )
                    )
                    push_button.click()
                    time.sleep(2)
                    input("Approve the push request and press Enter")
                    time.sleep(1)
                    wait.until(EC.url_contains("shellaccountmanager.ca/home"))
                    print("MFA approved and redirected to home page.")
                except Exception as e:
                    print(f"No MFA or failed to handle MFA: {e}")

                try:
                    # Handle pop-up if it appears
                    print("Closing pop-up...")
                    pop_up_close_button = wait.until(
                        EC.element_to_be_clickable(
                            (
                                By.CSS_SELECTOR,
                                "button.mat-ripple.appearance-icon.size-compact.state-enabled",
                            )
                        )
                    )
                    driver.execute_script("arguments[0].click();", pop_up_close_button)
                    print("Pop-up closed.")
                except Exception as e:
                    print(f"No pop-up or failed to close pop-up: {e}")

            else:
                print("Logged in")

            # Wait for the DOM to stabilize
            time.sleep(2)

        except:
            print("Failed to Login")
            return False, None
        print("Logged in")

        try:

            print("Navigating to 'Cards'...")
            cards_button = wait.until(
                EC.presence_of_element_located(
                    (
                        By.CSS_SELECTOR,
                        "span[data-qa='nav__cards_tab'] .main-nav-item-text",
                    )
                )
            )
            driver.execute_script("arguments[0].click();", cards_button)
            print("'Cards' section opened.")

            print("Navigating to 'Add driver'...")
            add_driver_button = wait.until(
                EC.presence_of_element_located(
                    (
                        By.CSS_SELECTOR,
                        "span[data-qa='nav__addDriver'] .main-nav-item-text",
                    )
                )
            )
            driver.execute_script("arguments[0].click();", add_driver_button)
            print("'Add driver' section opened.")

            # Wait for the form to load
            print("Waiting for the form to load...")
            time.sleep(5)  # Allow time for the form to fully render

            # Take a screenshot to debug the form state
            driver.save_screenshot("form_loaded.png")
            print("Screenshot of the form taken for debugging.")
            time.sleep(3)

            print("Filling out the form...")
            iframe = driver.find_element(By.TAG_NAME, "iframe")
            driver.switch_to.frame(iframe)

            # Fill out the form
            print("Filling out the form...")
            wait.until(EC.presence_of_element_located((By.ID, "lastName"))).clear()
            wait.until(EC.presence_of_element_located((By.ID, "lastName"))).send_keys(
                last_name
            )
            print("Last Name entered.")
            time.sleep(2)

            wait.until(
                EC.presence_of_element_located((By.ID, "firstName"))
            ).clear()  # Clear and input
            wait.until(EC.presence_of_element_located((By.ID, "firstName"))).send_keys(
                first_name
            )
            print("First Name entered.")
            time.sleep(1)

            wait.until(
                EC.presence_of_element_located((By.ID, "phoneNumber"))
            ).clear()  # Clear and input
            wait.until(
                EC.presence_of_element_located((By.ID, "phoneNumber"))
            ).send_keys(phone_number)
            print("Phone Number entered.")
            time.sleep(2)

            wait.until(
                EC.presence_of_element_located((By.ID, "emailAddress"))
            ).clear()  # Clear and input
            wait.until(
                EC.presence_of_element_located((By.ID, "emailAddress"))
            ).send_keys(email)
            print("Email Address entered.")
            time.sleep(2)

            # Clear and ensure middle name is empty
            middle_name_field = wait.until(
                EC.presence_of_element_located((By.ID, "middleName"))
            )
            middle_name_field.clear()
            print("Middle Name cleared.")
            time.sleep(1)

            # Fill license number and employee number
            wait.until(EC.presence_of_element_located((By.ID, "licenseNumber"))).clear()
            wait.until(
                EC.presence_of_element_located((By.ID, "licenseNumber"))
            ).send_keys(driver_license)
            print("License Number entered.")
            time.sleep(2)

            # wait.until(
            #     EC.presence_of_element_located((By.ID, "employeeNumber"))
            # ).clear()
            # wait.until(
            #     EC.presence_of_element_located((By.ID, "employeeNumber"))
            # ).send_keys()
            # print("Employee Number entered.")
            # time.sleep(1)

            # Fill job title and license expiration date
            wait.until(EC.presence_of_element_located((By.ID, "jobTitle"))).clear()
            wait.until(EC.presence_of_element_located((By.ID, "jobTitle"))).send_keys(
                "Driver"
            )
            print("Job Title entered.")
            time.sleep(2)

            wait.until(
                EC.presence_of_element_located((By.ID, "licenseExpDate"))
            ).clear()

            wait.until(
                EC.presence_of_element_located((By.ID, "licenseExpDate"))
            ).click()
            wait.until(
                EC.presence_of_element_located((By.ID, "licenseExpDate"))
            ).send_keys(
                datetime.strptime(license_expiry_date, "%m/%d/%Y").strftime("%Y-%m-%d")
            )
            print("License Expiration Date entered.")
            time.sleep(3)

            # Select dropdowns
            print("Selecting dropdowns...")
            Select(
                wait.until(EC.presence_of_element_located((By.NAME, "licenseState")))
            ).select_by_visible_text("Ontario")
            print("License State/Province selected.")
            time.sleep(2)

            Select(
                wait.until(EC.presence_of_element_located((By.ID, "departmentRowID")))
            ).select_by_visible_text("OPS")
            print("Driver Department selected.")
            time.sleep(2)

            Select(
                wait.until(EC.presence_of_element_located((By.ID, "licenseCountry")))
            ).select_by_visible_text("Canada")
            print("License Country selected.")
            time.sleep(1)

            # Take a screenshot to debug the filled form state
            driver.save_screenshot("form_filled.png")
            print("Screenshot of the filled form taken for debugging.")
            time.sleep(3)

            # Submit the form by clicking the Add button
            print("Submitting the form...")
            add_button = wait.until(
                EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, "button[name='_eventId_apply'][type='submit']")
                )
            )
            driver.execute_script("arguments[0].click();", add_button)
            time.sleep(3)
            try:
                success_alert = driver.find_element(By.XPATH, '//*[@id="errorContent"]')
                if success_alert.text == 'You have created a new driver with the following information.':
                    print("Form submitted successfully by clicking 'Add'.")
                else:
                    return False, None
            except:
                print("Something went wrong. Form not submitted.")
                return False, None

            time.sleep(2)

            try:
                driver_prompt_id_element = driver.find_element(
                    By.XPATH,
                    '//*[@id="driverView"]/div[2]/main/div[2]/div/div[3]/div[1]/div[7]/div',
                )
                driver_prompt_id = driver_prompt_id_element.text.strip()[-4:]
            except:
                driver_prompt_id = None
            return True, driver_prompt_id

        except Exception as e:
            print(f"An error occurred: {e}")

            # Take a screenshot to debug the error
            driver.save_screenshot("error_screenshot.png")
            print("Screenshot of the error state taken for debugging.")
            time.sleep(1)
            return False, None

    finally:
        # Close the driver when done
        driver.quit()
