import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options


from amazon_utils import (
    expand_onboarding_section,
    edit_dob_and_licence_details,
    edit_photo,
    verify_and_update_associate_settings,
    verify_onboarding_progress,
    basic_info_onboarding,
    complete_task,
    logout,
)


def driver_amazon_onboarding(
    first_name, last_name, email, location, dob, license_expiry_date, driver_license
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
            # driver.get("https://mylocation.org")
            # driver.save_screenshot("ip_for_amazon.png")

            # Open Amazon DSP Account Management page
            driver.get("https://logistics.amazon.ca/dsp-account-management/")
            driver.maximize_window()
            print(driver.title)

            # Check if already logged in
            if "Sign In" in driver.title:
                # Locate email input
                email = driver.find_element(By.NAME, "email")
                email.clear()
                email.send_keys(os.getenv("AMAZON_EMAIL"))
                email.send_keys(Keys.RETURN)

                time.sleep(3)

                # Wait for password field
                wait.until(EC.presence_of_element_located((By.NAME, "password")))

                remember_me_checkbox = driver.find_element(
                    By.NAME, "rememberMe"
                )  # Or use aria-label if needed
                if not remember_me_checkbox.is_selected():
                    remember_me_checkbox.click()
                time.sleep(3)

                # Enter password
                password = driver.find_element(By.NAME, "password")
                password.clear()
                password.send_keys(os.getenv("AMAZON_PASSWORD"))
                time.sleep(1)
                password.send_keys(Keys.RETURN)
                time.sleep(3)

                # Wait until redirected to the DSP dashboard
                if "Sign In" in driver.title:
                    print("Sign in and make sure to be on homepage.")
                    input("Press Enter to proceed...")
                else:
                    print("Logged in successfully.")

            else:
                print("Already logged in!")

        except:
            print("Sign in and make sure to be on homepage.")
            input("Press Enter to proceed...")
            driver.maximize_window()

        driver.get("https://logistics.amazon.ca/dspconsole")

        if "Logistics" in driver.title:
            side_menu_button = wait.until(
                EC.presence_of_element_located((By.CLASS_NAME, "fp-nav-menu-icon"))
            )

            if side_menu_button.is_displayed():
                time.sleep(3)
                print("Side menu button is visible in mobile view.")
                side_menu_button.click()  # Click to open the side menu
                print("Clicked the side menu button.")
                time.sleep(3)  # Allow the menu to fully load

            nav_list = driver.find_elements(By.CLASS_NAME, "fp-nav-menu-list-item")

            time.sleep(2)

            setup_link = None
            for nav_item in nav_list:
                anchor = nav_item.find_element(By.TAG_NAME, "a")
                if "Set-up" in anchor.text:
                    setup_link = anchor
                    break

            time.sleep(2)

            if setup_link.is_displayed():
                print("The 'Set-up' link is visible.")
            else:
                print("The 'Set-up' link is not visible. Check for rendering issues.")
                return False

            time.sleep(2)

            size = setup_link.size
            setup_link_location = setup_link.location
            print(f"Element size: {size}, setup_link_location: {setup_link_location}")

            if size["width"] == 0 or size["height"] == 0:
                print(
                    "The element has zero dimensions. Ensure it is not hidden or offscreen."
                )
                return False

            else:
                print(
                    "Found 'Set-up' link with href:", setup_link.get_attribute("href")
                )

                # Perform hover action
                actions = ActionChains(driver)
                actions.move_to_element(setup_link).perform()
                print("Hovered over the 'Set-up' link.")
                setup_link.click()
                print("Clicked over the 'Set-up' link.")
                time.sleep(2)

                dropdown_menu = wait.until(
                    EC.presence_of_element_located(
                        (By.XPATH, '//*[@id="fp-nav-menu"]/ul/li[7]/ul')
                    )
                )
                print("Dropdown menu appeared.")
                time.sleep(3)

                # Locate the 'Associates' link
                associates_option = WebDriverWait(dropdown_menu, 10).until(
                    EC.presence_of_element_located((By.LINK_TEXT, "Associates"))
                )
                driver.execute_script(
                    "arguments[0].scrollIntoView();", associates_option
                )
                associates_option.click()
                print("Clicked on the 'Associates' option.")

            try:
                # Step 1: Click the "Add Delivery Associates" element
                add_delivery_associates_button = wait.until(
                    EC.presence_of_element_located(
                        (
                            By.XPATH,
                            '//*[@id="root"]/div/div/div[1]/div/div/div/div/div/div[3]/div/div[2]/div/a',
                        )
                    )
                )


                driver.execute_script(
                    "arguments[0].scrollIntoView();", add_delivery_associates_button
                )
                time.sleep(2)
                add_delivery_associates_button.click()
                print("Clicked on the Add Delivery Associates element.")

                time.sleep(5)

                # Step 2: Wait for the new window and switch to it
                wait.until(lambda d: len(driver.window_handles) > 1)
                new_window = [
                    window
                    for window in driver.window_handles
                    if window != driver.current_window_handle
                ][0]
                driver.switch_to.window(new_window)
                print("Switched to the new window.")
                time.sleep(3)

                # Step 3: Click the "Add a New Delivery Associate" element
                try:
                    add_a_new_delivery_associate_button = wait.until(
                        EC.presence_of_element_located(
                            (
                                By.XPATH,
                                '//*[@id="dsp-onboarding"]/div/main/div[2]/div[2]/button',
                            )
                        )
                    )
                    driver.execute_script(
                        "arguments[0].scrollIntoView();",
                        add_a_new_delivery_associate_button,
                    )
                    time.sleep(3)

                    add_a_new_delivery_associate_button.click()
                    print("Clicked on the Add a New Delivery Associate element.")

                except Exception as e:
                    print(f"Failed to click on 'Add a New Delivery Associate': {e}")
                    return False

                try:

                    # driver.get(
                    #     "https://logistics.amazon.ca/account-management/delivery-associates/detail/amzn1.flex.provider.v1.04d870a7-df08-4856-886c-69cd0e4e7358"
                    # )

                    # driver.get(
                    #     "https://logistics.amazon.ca/account-management/delivery-associates/detail/amzn1.flex.provider.v1.afd288b2-dbb0-4f9f-8b8f-6886d9fa4e12"
                    # # )
                    # driver.get(
                    #     "https://logistics.amazon.ca/account-management/delivery-associates/detail/amzn1.flex.provider.v1.7c7b366f-3b46-47e0-a1e8-a18db853f911"
                    # )
                    # driver.get(
                    #     "https://logistics.amazon.ca/account-management/delivery-associates/detail/amzn1.flex.provider.v1.d0d9f15d-eb26-4dcc-a0cb-578e9238514c"
                    # )
                    # driver.get(
                    #     "https://logistics.amazon.ca/account-management/delivery-associates/detail/amzn1.flex.provider.v1.8e8f9b42-71b0-438e-b5f7-9f0dece1d4a3"
                    # )
                    # time.sleep(5)

                    basic_info_onboarding_success = basic_info_onboarding(
                        driver, wait, location, first_name, last_name, email
                    )
                    if not basic_info_onboarding_success:
                        return False



                    wait.until(
                        EC.presence_of_element_located(
                            (
                                By.XPATH,
                                "//div[@class='af-column da__photo__empty align-center justify-center']",
                            )
                        )
                    )
                    print("Page has loaded after redirection.")

                    # Check the current URL to ensure you're on the correct page
                    current_url = driver.current_url
                    print(f"Current URL after redirection: {current_url}")

                    time.sleep(5)

                    edit_photo_success = edit_photo(driver, wait)
                    if not edit_photo_success:
                        return False
                    time.sleep(5)

                    edit_dob_and_licence_details_success = edit_dob_and_licence_details(
                        driver, wait, dob, license_expiry_date, driver_license
                    )
                    if not edit_dob_and_licence_details_success:
                        return False
                    time.sleep(3)

                    verify_and_update_associate_settings_success = (
                        verify_and_update_associate_settings(driver, wait, location)
                    )
                    if not verify_and_update_associate_settings_success:
                        return False
                    time.sleep(3)

                    expand_onboarding_section_success = expand_onboarding_section(
                        driver,
                        wait,
                        '//*[@id="dsp-onboarding"]/div/main/div/div[4]/div/div[1]/i',
                    )
                    if not expand_onboarding_section_success:
                        return False

                    time.sleep(3)

                    verify_onboarding_initial_progress_success = verify_onboarding_progress(
                        driver,
                        wait,
                        onboarding_progress_xpath="//span[contains(@class, 'af-accordion__right-label')]",
                        expected_progress="4 of 11 Completed",
                    )
                    if not verify_onboarding_initial_progress_success:
                        return False
                    time.sleep(3)

                    driver_record_verification_task_success = complete_task(
                        driver,
                        wait,
                        "Driver record verification",
                        '//*[@id="dsp-onboarding"]/div/main/div/div[4]/div/div[2]/div/div[1]/div[1]/div[1]/div/h3/a',
                        '//*[@id="manual-task-yes"]',
                        '//*[@id="dsp-onboarding"]/div/main/div/span[5]/div/div/div[2]/div[2]/button[1]',
                    )
                    if not driver_record_verification_task_success:
                        return False
                    time.sleep(3)

                    drug_test_task_success = complete_task(
                        driver,
                        wait,
                        "Drug test",
                        '//*[@id="dsp-onboarding"]/div/main/div/div[4]/div/div[2]/div/div[1]/div[6]/div[1]/div/h3/a',
                        '//*[@id="manual-task-yes"]',
                        '//*[@id="dsp-onboarding"]/div/main/div/span[5]/div/div/div[2]/div[2]/button[1]',
                    )
                    if not drug_test_task_success:
                        return False
                    time.sleep(2)

                    background_check_task_success = complete_task(
                        driver,
                        wait,
                        "Background check",
                        '//*[@id="dsp-onboarding"]/div/main/div/div[4]/div/div[2]/div/div[1]/div[7]/div[1]/div/h3/a',
                        '//*[@id="manual-task-yes"]',
                        '//*[@id="dsp-onboarding"]/div/main/div/span[5]/div/div/div[2]/div[2]/button[1]',
                    )
                    if not background_check_task_success:
                        return False
                    time.sleep(1)

                    training_task_success = complete_task(
                        driver,
                        wait,
                        "Training",
                        '//*[@id="dsp-onboarding"]/div/main/div/div[4]/div/div[2]/div/div[1]/div[8]/div[1]/div/h3/a',
                        '//*[@id="manual-task-yes"]',
                        '//*[@id="dsp-onboarding"]/div/main/div/span[5]/div/div/div[2]/div[2]/button[1]',
                    )
                    if not training_task_success:
                        return False
                    time.sleep(2)

                    verify_onboarding_final_progress_success = verify_onboarding_progress(
                        driver,
                        wait,
                        onboarding_progress_xpath="//span[contains(@class, 'af-accordion__right-label')]",
                        expected_progress="8 of 11 Completed",
                    )
                    if not verify_onboarding_final_progress_success:
                        return False
                    time.sleep(5)

                    # logout_success = logout(driver, wait)     #  in progress
                    # if not logout_success:
                    #     return False

                    return True
                except Exception as e:
                    print(f"Failed to onboard: {e}")
                    return False

            except Exception as e:
                print(
                    f"Failed to click on the 'Add Delivery Associates' element or switch windows: {e}"
                )
                return False

        else:
            print("Something went wrong. Logistics page can not be loaded")
            return False

    except Exception as e:
        print("Something went wrong. Error:", str(e))
        return False
    finally:
        driver.quit()
