import os
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.keys import Keys


def basic_info_onboarding(driver, wait, location, first_name, last_name, email):
    try:

        first_name_field = wait.until(
            EC.presence_of_element_located((By.ID, "root_FIRST_NAME"))
        )

        last_name_field = wait.until(
            EC.presence_of_element_located((By.ID, "root_LAST_NAME"))
        )
        email_field = wait.until(EC.presence_of_element_located((By.ID, "root_EMAIL")))

        first_name_field.send_keys(first_name)
        time.sleep(3)

        last_name_field.send_keys(last_name)
        time.sleep(4)

        email_field.send_keys(email)
        time.sleep(3)

        select_offering_type_success = select_offering_type(driver, wait, location)
        if not select_offering_type_success:
            return False
        time.sleep(3)

        checkbox_driver = driver.find_element(
            By.ID, "root_POSITION_0"
        )  # Driver checkbox
        checkbox_helper = driver.find_element(
            By.ID, "root_POSITION_1"
        )  # Helper checkbox

        if not checkbox_driver.is_selected():
            checkbox_driver.click()  # Check Driver checkbox
            print("Checked the Driver checkbox.")
            time.sleep(2)

        if not checkbox_helper.is_selected():
            checkbox_helper.click()  # Check Helper checkbox
            print("Checked the Helper checkbox.")
            time.sleep(4)

        try:
            send_button = wait.until(
                EC.element_to_be_clickable(
                    (
                        By.XPATH,
                        "//button[@type='submit' and @class='af-button primary ' and @form='addAssociateFormId']",
                    )
                )
            )
            send_button.click()  # Click the 'Send' button
            print("Clicked the 'Send' button.")
            time.sleep(2)

            try:
                wait.until(
                    EC.visibility_of_element_located(
                        (By.XPATH, "//div[@class='popup-container']")
                    )
                )
                time.sleep(3)

                ok_button = driver.find_element(
                    By.XPATH,
                    "//div[@class='popup-container']//button[@type='button']",
                )
                ok_button.click()
                print("Clicked on the OK button to close the pop-up.")

            except Exception as e:
                print(f"Error: {e}")
                print("No pop-up appeared or could not click the OK button.")
                return False


            return True

        except Exception as e:
            print(f"Failed to click the 'Send' button: {e}")
            return False

    except Exception as e:
        print(f"Failed to fill the basic info onboarding form: {e}")
        return False


def select_offering_type(driver, wait, location):

    try:

        # Open the dropdown by clicking on the container
        offering_type_container = driver.find_element(
            By.ID, "option_container_root_OFFERING_TYPE"
        )
        time.sleep(1)

        offering_type_container.click()

        offering_type = ""
        if location == "DOI6":
            offering_type = "AMZL"
        elif location == "HYZ1":
            offering_type = "AMXL"
        else:
            print("Location not recognized.")
            return

        wait.until(
            EC.presence_of_element_located((By.ID, "option_list_root_OFFERING_TYPE"))
        )
        options = driver.find_elements(
            By.XPATH,
            f"//ul[@id='option_list_root_OFFERING_TYPE']/li[text()='{offering_type}']",
        )
        if options:
            time.sleep(1)
            options[0].click()  # Click on the correct option
            print(f"Selected Offering Type: {offering_type}")
            time.sleep(3)
            return True

        else:
            print(f"Offering Type {offering_type} not found.")
            return False
    except:
        return False


def upload_image_file(file_input, file_name):
    """Uploads the specified file if it exists."""
    try:
        file_path = os.path.abspath(file_name)

        if not file_input:
            print("File input field not found.")
            return False

        if not os.path.exists(file_path):
            print(f"File does not exist at the provided path: {file_path}")
            return False

        time.sleep(2)
        file_input.send_keys(file_path)
        time.sleep(3)

        print("File uploaded successfully.")
        return True
    except:
        return False


def edit_dob_and_licence_details(
    driver, wait, dob, license_expiry_date, driver_license
):
    """Fill DOB, license expiration date, and license number, then confirm."""
    try:

        edit_button = wait.until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "//*[@id='dsp-onboarding']/div/main/div/div[1]/div/div[2]/div[2]/div[1]/div[5]/a",
                )
            )
        )
        time.sleep(1)

        edit_button.click()
        # time.sleep(3)

        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    "//*[@id='dsp-onboarding']/div/main/div/div[6]/span/div",
                )
            )
        )

        print("Modal detected.")

        modal_container = driver.find_element(
            By.CLASS_NAME, "af-modal-container"
        ).find_elements(By.TAG_NAME, "input")

        def set_date(modal_container, input_no_tag, value):
            how_many_possibilities_allowed = 5
            is_rerun = True
            possibilities = 0
            date_field = modal_container[input_no_tag]
            while is_rerun and possibilities < how_many_possibilities_allowed:
                possibilities = possibilities + 1
                time.sleep(2)
                date_field.click()
                time.sleep(1)

                date_field.send_keys(value)
                time.sleep(1)
                date_field.send_keys(Keys.RETURN)

                check_val_ = (
                    driver.find_element(By.CLASS_NAME, "af-modal-container")
                    .find_elements(By.TAG_NAME, "input")[input_no_tag]
                    .get_attribute("value")
                )
                if check_val_ == value:
                    is_rerun = False
                    return True
            return False

        set_dob_date_success = set_date(modal_container, 0, dob)
        if not set_dob_date_success:
            return False
        time.sleep(3)

        set_licence_expiry_date_success = set_date(
            modal_container, 1, license_expiry_date
        )
        if not set_licence_expiry_date_success:
            return False

        # Locate and fill the Driver's License Number field
        license_number_field = driver.find_element(By.ID, "dl-input")
        license_number_field.send_keys(Keys.CONTROL, "a")
        time.sleep(1)
        license_number_field.send_keys(Keys.BACKSPACE)
        time.sleep(2)
        license_number_field.send_keys(driver_license)
        time.sleep(2)

        print(f"Driver's License Number set to: {driver_license}")

        # Locate and click the Confirm button
        confirm_button = driver.find_element(
            By.XPATH,
            "//button[contains(@class, 'af-button primary') and text()='Confirm']",
        )
        time.sleep(2)
        confirm_button.click()
        print("Confirm button clicked.")
        time.sleep(3)

        try:
            alert_message = driver.find_element(
                By.XPATH,
                "//div[@role='alert' and contains(@class, 'css-15gmago')]",
            )
            error_text = alert_message.text.strip()
            print(f"Error detected: {error_text}")
            return False
        except Exception:
            print("No alert message detected. Proceeding.")

        return True

    except Exception as e:
        print(f"Error updating DOB and license details: {e}")
        return False


def edit_photo(driver, wait):
    try:
        edit_button = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//*[@id='dsp-onboarding']/div/main/div/div[1]/div/div[1]/a")
            )
        )
        time.sleep(1)
        edit_button.click()
        time.sleep(3)

        modal_container = wait.until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    "//div[@class='af-modal-container af-text edit-profile__modal center']",
                )
            )
        )

        # If the page is correct, proceed with file upload
        file_input = driver.find_element(By.XPATH, "//input[@type='file']")

        if file_input:
            time.sleep(1)
            file_name = "Photo.png"
            upload_image_file_success = upload_image_file(file_input, file_name)
            time.sleep(2)
            if not upload_image_file_success:
                return False

            try:
                confirm_button = driver.find_element(
                    By.XPATH, "//button[@type='button' and contains(@class, 'primary')]"
                )
                time.sleep(1)
                confirm_button.click()
                time.sleep(3)
                print("Confirm button clicked successfully.")
                return True
            except Exception as e:
                print(f"Error clicking the Confirm button: {e}")
                return False

        else:
            print("File input field not found.")
            return False
    except:
        print("Failed to edit photo.")
        return False


def verify_and_update_associate_settings(driver, wait, location):
    try:
        # Locate the Primary Delivery Station setting
        delivery_station_label_xpath = (
            '//*[@id="dsp-onboarding"]/div/main/div/div[3]/div[2]/div[4]/span'
        )
        # Fetch the current station text
        delivery_station_element = driver.find_element(
            By.XPATH, delivery_station_label_xpath
        )
        time.sleep(1)

        current_station = delivery_station_element.text.strip()
        time.sleep(2)

        print(f"Current Delivery Station: {current_station}")
        expected_station = None
        if location == "DOI6":
            # Define expected stations
            expected_station = "Mississauga (DOI6)- Amazon.com"
        elif location == "HYZ1":
            expected_station = "Oakville (HYZ1)- Amazon.com"

        # Check if the settings are correct
        if current_station == expected_station:
            print("Primary Delivery Station is correctly set to Mississauga (DOI6).")
        elif current_station == expected_station:
            print("Primary Delivery Station is correctly set to Oakville (HYZ1).")
        else:
            print("Incorrect Primary Delivery Station found.")

            # Locate and click the "Edit" button
            edit_button_xpath = (
                "//div[@class='af-row margin-bottom__x-small']/div/a[text()='Edit']"
            )
            edit_button = driver.find_element(By.XPATH, edit_button_xpath)
            time.sleep(2)

            edit_button.click()
            print("Edit button clicked. Proceeding to update settings.")
            time.sleep(2)
            # Wait for the modal to appear
            modal = wait.until(
                EC.presence_of_element_located((By.CLASS_NAME, "af-modal"))
            )

            # Select the 'Primary Delivery Station'
            station_dropdown = modal.find_element(
                By.XPATH,
                "//label[contains(text(),'Service areas')]/following-sibling::div",
            )
            time.sleep(2)

            station_dropdown.click()  # Open the dropdown
            time.sleep(2)

            # Select the correct station
            station_options = wait.until(
                EC.presence_of_all_elements_located(
                    (By.XPATH, "//ul[contains(@class,'af-options')]/li")
                )
            )

            for option in station_options:

                if option.text.replace(" ", "") == expected_station.replace(" ", ""):
                    time.sleep(1)
                    driver.execute_script("arguments[0].scrollIntoView(true);", option)
                    try:
                        time.sleep(2)
                        option.click()
                        time.sleep(1)

                        break
                    except Exception as e:
                        print(
                            f"Click intercepted for option '{option.text}', retrying..."
                        )
                        time.sleep(1)
                        try:
                            driver.execute_script("arguments[0].click();", option)
                            return True  # JavaScript click successful
                        except Exception as e2:
                            print(
                                f"Failed to click on option '{option.text}' even with JavaScript: {e2}"
                            )
                            return False  # JS click also failed

            else:
                print(
                    f"Station '{expected_station}' not found in the dropdown options."
                )
                return False

            # Confirm the changes
            confirm_button = modal.find_element(
                By.XPATH, "//button[contains(text(),'Confirm')]"
            )
            time.sleep(1)
            confirm_button.click()
            time.sleep(2)

            # Verify the changes are saved (optional, based on your page's behavior)
            wait.until(EC.invisibility_of_element(modal))
            print(f"Associate settings updated: Station='{expected_station}")

            time.sleep(2)
            
        return True
    except NoSuchElementException as e:
        print(f"Element not found: {e}")
        return False
    except TimeoutException as e:
        print(f"Timed out waiting for element: {e}")
        return False
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return False


def expand_onboarding_section(driver, wait, expand_button_xpath):
    """
    Expands the onboarding section and waits for the 'Complete your tasks' text.
    """
    try:
        expand_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, expand_button_xpath))
        )
        time.sleep(2)
        expand_button.click()
        time.sleep(2)

        while True:
            task_text = wait.until(
                EC.presence_of_element_located(
                    (
                        By.XPATH,
                        '//*[@id="dsp-onboarding"]/div/main/div/div[4]/div/div[2]/div/div[1]/h3[1]',
                    )
                )
            )
            if task_text.is_displayed():
                break
            else:
                expand_button = wait.until(
                    EC.element_to_be_clickable((By.XPATH, expand_button_xpath))
                )
                time.sleep(4)
                expand_button.click()

        return True
    except:
        print("Something went wrong while expanding onboarding section")
        return False


def verify_onboarding_progress(
    driver, wait, onboarding_progress_xpath, expected_progress
):
    """
    Verifies the initial progress.
    """
    try:
        driver.refresh()
        time.sleep(2)
        # Verify progress
        onboarding_progress = wait.until(
            EC.presence_of_element_located((By.XPATH, onboarding_progress_xpath))
        )
        time.sleep(1)

        if expected_progress not in onboarding_progress.text:
            time.sleep(2)
            print(
                f"Error: Expected progress '{expected_progress}' not found. Found: {onboarding_progress.text}"
            )
            return False

        print(f"Initial progress verified: {onboarding_progress.text}")
        return True

    except TimeoutException as e:
        print(f"Error: Timeout while waiting for onboarding progress element: {e}")
    except Exception as e:
        print(f"Error: {e}")

    return False


def complete_task(
    driver,
    wait,
    task_name,
    edit_button_xpath,
    yes_radio_button_xpath,
    confirm_button_xpath,
):
    """
    Completes a specific onboarding task by clicking Edit and confirming YES.
    """
    try:
        expand_onboarding_section_success = expand_onboarding_section(
            driver, wait, '//*[@id="dsp-onboarding"]/div/main/div/div[4]/div/div[1]/i'
        )
        if not expand_onboarding_section_success:
            return False

        edit_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, edit_button_xpath))
        )
        time.sleep(2)

        edit_button.click()
        time.sleep(1)

        yes_radio_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, yes_radio_button_xpath))
        )
        time.sleep(1)
        yes_radio_button.click()
        time.sleep(2)

        print(f"Selected 'Yes' for task '{task_name}'.")

        # confirm_button_xpath = "//button[text()='YES']"
        confirm_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, confirm_button_xpath))
        )
        time.sleep(1)
        confirm_button.click()
        time.sleep(2)

        print(f"Task '{task_name}' completed successfully.")
        return True
    except:
        print(f"Task '{task_name}' failed to complete.")
        return False


def logout(driver, wait):
    #  in progress
    try:
        # Wait for the profile menu icon to be visible and click it
        time.sleep(2)
        profile_menu_icon = wait.until(
            EC.element_to_be_clickable((By.ID, "mobile-profile-menu-icon"))
        )
        time.sleep(1)
        profile_menu_icon.click()

        # Wait for the logout link to be visible in the dropdown
        logout_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, '//a[contains(text(), "Sign Out")]'))
        )
        time.sleep(1)
        logout_button.click()
        time.sleep(2)

        print("Successfully logged out.")
        return True

    except Exception as e:
        print(f"Error during logout: {e}")
        return False