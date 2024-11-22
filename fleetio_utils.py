import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


def navigate_to_fleetio_dashboard(driver, wait):
    try:
        # driver.get("https://mylocation.org")
        # driver.save_screenshot("ip_for_fleetio.png")

        driver.get("https://secure.fleetio.com/users/sign_in")

        if "dashboard" not in driver.current_url:
            print("Navigating to dashboard")
            return True
        else:
            print("Unable to navigate to dashboard")
            return False
    except:
        print("Unable to navigate to dashboard")
        return False


def add_contact(driver, wait, first_name, last_name, location, username, password):

    time.sleep(1)

    contacts_option = wait.until(
        EC.presence_of_element_located(
            (By.XPATH, "/html/body/div[3]/nav/ul/li[8]/a/div/div[2]/span")
        )
    )
    contacts_option.click()
    time.sleep(2)
    add_contacts_button = wait.until(
        EC.presence_of_element_located(
            (
                By.XPATH,
                '//*[@id="page-content-header"]/div/div[1]/div/div/div/div/div[2]/div/div[2]/a/span/span[2]',
            )
        )
    )
    add_contacts_button.click()
    time.sleep(1)
    first_name_field = wait.until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="field_5"]'))
    )
    first_name_field.clear()
    first_name_field.click()
    first_name_field.send_keys(first_name)
    print("First Name Entered.")
    time.sleep(1)

    last_name_field = wait.until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="field_7"]'))
    )
    last_name_field.clear()
    last_name_field.click()
    last_name_field.send_keys(last_name)
    print("Last Name Entered.")
    time.sleep(2)

    location_to_group = {"DOI6": "DOI6", "Fedex": "Fedex", "HYZ1": "HYZ1"}
    group_value = location_to_group.get(location)
    if not group_value:
        raise ValueError(f"Location not recognized: {location}")

    # Wait for the dropdown to be clickable
    group_dropdown = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, ".select-async__control"))
    )
    group_dropdown.click()
    time.sleep(1)

    # Find the group option by text and click it
    group_option = wait.until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".select-async__option"))
    )

    for option in group_option:
        if group_value in option.text:
            option.click()
            break

    time.sleep(1)

    operator_checkbox = wait.until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="field_12"]'))
    )
    operator_checkbox.click() if not operator_checkbox.is_selected() else None
    print("Operator checkbox selected.")
    time.sleep(2)

    employee_checkbox = wait.until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="field_13"]'))
    )
    employee_checkbox.click() if not employee_checkbox.is_selected() else None
    print("Employee checkbox selected.")
    time.sleep(1)

    full_access_element = wait.until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="field_15"]'))
    )
    driver.execute_script(
        "arguments[0].scrollIntoView({ behavior: 'smooth', block: 'center' });",
        full_access_element,
    )
    time.sleep(1)
    full_access_element.click()
    print("Full Access Radio Button clicked.")

    username_and_password_element = wait.until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="field_20"]'))
    )
    driver.execute_script(
        "arguments[0].scrollIntoView({ behavior: 'smooth', block: 'center' });",
        username_and_password_element,
    )
    time.sleep(1)
    username_and_password_element.click()
    print("Username and Password Radio Button clicked.")
    time.sleep(1)

    username_field = wait.until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="field_65"]'))
    )
    driver.execute_script(
        "arguments[0].scrollIntoView({ behavior: 'smooth', block: 'center' });",
        username_field,
    )
    username_field.click()
    username_field.clear()
    username_field.send_keys(username)
    print("Username Entered.")
    time.sleep(2)

    password_field = wait.until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="field_66"]'))
    )
    driver.execute_script(
        "arguments[0].scrollIntoView({ behavior: 'smooth', block: 'center' });",
        password_field,
    )
    password_field.click()
    password_field.clear()
    password_field.send_keys(password)
    print("Password Entered.")
    time.sleep(2)

    role_dropdown = wait.until(
        EC.element_to_be_clickable(
            (
                By.CSS_SELECTOR,
                ".select-async__control[data-testid='account_membership_attributes.role_id-react-select-control']",
            )
        )
    )
    driver.execute_script(
        "arguments[0].scrollIntoView({ behavior: 'smooth', block: 'center' });",
        role_dropdown,
    )
    role_dropdown.click()
    time.sleep(1)

    # Wait for the input inside the dropdown to be clickable and type the "Operator"
    role_option = wait.until(
        EC.presence_of_element_located(
            (
                By.CSS_SELECTOR,
                ".select-async__input[data-testid='account_membership_attributes.role_id-react-select-input']",
            )
        )
    )
    role_option.send_keys("Operator")
    time.sleep(1)  # Allow time for suggestions to load

    # Explicitly find and click the "Operator" option from the dropdown
    operator_option_xpath = "//div[contains(text(), 'Operator')]"
    operator_option = wait.until(
        EC.element_to_be_clickable((By.XPATH, operator_option_xpath))
    )
    operator_option.click()
    print("Role Operator Selected.")

    time.sleep(2)

    # XPaths for the dropdowns to process
    xpaths = [
        "//div[@data-testid='account_membership_attributes.vehicles_record_set_id-react-select-control']",
        "//div[@data-testid='account_membership_attributes.equipments_record_set_id-react-select-control']",
        "//div[@data-testid='account_membership_attributes.contacts_record_set_id-react-select-control']",
        "//div[@data-testid='account_membership_attributes.parts_record_set_id-react-select-control']",
        "//div[@data-testid='account_membership_attributes.inspection_forms_record_set_id-react-select-control']",
    ]

    # Process each dropdown in the list
    for xpath in xpaths:
        try:
            # Wait for the dropdown to be clickable and click it
            dropdown = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
            driver.execute_script(
                "arguments[0].scrollIntoView({ behavior: 'smooth', block: 'center' });",
                dropdown,
            )
            dropdown.click()
            time.sleep(1)

            # Wait for the options to load
            options = wait.until(
                EC.presence_of_all_elements_located(
                    (By.CSS_SELECTOR, ".select-async__option")
                )
            )

            # Select the option containing 'Full Access'
            for option in options:
                if "Full Access" in option.text:
                    option.click()
                    break

            time.sleep(1)
            print(f"Marked dropdown at '{xpath}' as 'Full Access'.")
        except Exception as e:
            print(f"Error handling dropdown at '{xpath}': {e}")
            return False

    save_contact_button = wait.until(
        EC.presence_of_element_located(
            (
                By.XPATH,
                "/html/body/div[3]/div/div/div[3]/div/div/form/div/div[2]/div/div/div[2]/div/div[4]/button",
            )
        )
    )
    driver.execute_script(
        "arguments[0].scrollIntoView({ behavior: 'smooth', block: 'center' });",
        save_contact_button,
    )
    save_contact_button.click()

    try:
        details_heading = wait.until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    "/html/body/div[3]/div/div/div[3]/div[1]/div/div[1]/div[1]/div/div[1]/div/div[1]",
                )
            )
        )
        print("Contact Added Successfully")
        return True
    except:
        print("Failed to add contact")
        return False
