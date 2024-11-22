import time
from datetime import datetime

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select


def navigate_to_cards_and_add_driver(
    driver,
    wait,
    first_name,
    last_name,
    email,
    driver_license,
    license_expiry_date,
    phone_number,
):

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
    except:
        print("Unable to navigate to cards tab and add driver form")
        return False, None

    try:
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
        wait.until(EC.presence_of_element_located((By.ID, "phoneNumber"))).send_keys(
            phone_number
        )
        print("Phone Number entered.")
        time.sleep(2)

        wait.until(
            EC.presence_of_element_located((By.ID, "emailAddress"))
        ).clear()  # Clear and input
        wait.until(EC.presence_of_element_located((By.ID, "emailAddress"))).send_keys(
            email
        )
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
        wait.until(EC.presence_of_element_located((By.ID, "licenseNumber"))).send_keys(
            driver_license
        )
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

        wait.until(EC.presence_of_element_located((By.ID, "licenseExpDate"))).clear()

        wait.until(EC.presence_of_element_located((By.ID, "licenseExpDate"))).click()
        wait.until(EC.presence_of_element_located((By.ID, "licenseExpDate"))).send_keys(
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
            if (
                success_alert.text
                == "You have created a new driver with the following information."
            ):
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
