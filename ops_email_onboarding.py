import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options


def add_username_on_ops_email(username=None):
    chromedriver_path = "/home/marriam/Downloads/k/chromedrivernn"
    user_data_dir = "/home/marriam/Downloads/d/chrome-user-data-ms"

    # Set Chrome options
    chrome_options = Options()
    chrome_options.add_argument(f"user-data-dir={user_data_dir}")
    chrome_options.add_argument("--profile-directory=Default")

    # Initialize the webdriver
    service = Service(executable_path=chromedriver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)
    wait = WebDriverWait(driver, 10)

    # driver.get("https://mylocation.org")
    # driver.save_screenshot("ip_for_ops.png")

    driver.get("https://myaccount.microsoft.com/")
    time.sleep(3)
    driver.maximize_window()
    try:
        if "Sign" in driver.title:

            wait.until(EC.presence_of_element_located((By.NAME, "loginfmt")))

            # Enter email
            email = driver.find_element(By.NAME, "loginfmt")
            email.clear()
            email.send_keys(os.getenv("MS_OPS_EMAIL"))
            email.send_keys(Keys.RETURN)

            wait.until(EC.presence_of_element_located((By.NAME, "passwd")))

            # Enter password
            password = driver.find_element(By.NAME, "passwd")
            password.clear()
            password.send_keys(os.getenv("MS_OPS_PASSWORD"))
            password.send_keys(Keys.RETURN)

            time.sleep(3)
            print("Please complete the MFA process. Press Enter once done.")
            input()
            if "My" in driver.title:
                print("Logged in successfully!")
            else:
                print("Can't login")
                print("Please login if not logged in and press Enter once done.")
                input()
        elif "My" in driver.title:
            print("Already logged in successfully!")
        else:
            print("Can't login")
            print("Please login if not logged in and press Enter once done.")
            input()

        time.sleep(1)

        try:
            # Wait for the feedback modal to appear, with a timeout of 5 seconds
            feedback_modal = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located(
                    (By.CLASS_NAME, "ms-Modal-scrollableContent")
                )
            )
            print("Feedback modal detected.")

            # Locate and click the close button
            close_button = feedback_modal.find_element(
                By.XPATH, './/button[contains(@class, "ms-Dialog-button--close")]'
            )
            close_button.click()
            time.sleep(2)
            print("Feedback modal closed.")
        except TimeoutException:
            print("No feedback modal detected.")

        driver.get("https://admin.microsoft.com/Adminportal/Home#/homepage")

        wait.until(EC.presence_of_element_located((By.ID, "DashboardSwitcher")))

        users_dropdown_button = driver.find_element(By.NAME, "Users")
        users_dropdown_button.click()
        time.sleep(1)

        active_users_button = wait.until(
            EC.presence_of_element_located((By.NAME, "Active users"))
        )

        if active_users_button.is_displayed():
            time.sleep(2)
            active_users_button.click()
            print("Clicked the active user  button.")
            time.sleep(2)

            active_users = driver.find_elements(By.CLASS_NAME, "ms-List-cell")

            for active_user in active_users:
                try:
                    time.sleep(3)
                    ops_text = active_user.find_element(
                        By.XPATH, ".//span[text()='ops']"
                    )
                    if (
                        ops_text.get_attribute("role") == "button"
                        and ops_text.text == "ops"
                    ):
                        ops_text.click()

                        print("Clicked on Ops Active User")
                        time.sleep(4)
                        email_aliases_button = driver.find_element(
                            By.CSS_SELECTOR,
                            "button[humanfriendlyname='ManageEmail'][data-automation-id='UserDetailPanelRegion,ManageEmailLink']",
                        )

                        email_aliases_button.click()

                        time.sleep(3)
                        username_field = driver.find_element(
                            By.XPATH,
                            "/html/body/div[5]/div[2]/div/div/div/div[2]/div[2]/div/div[3]/div[3]/div[2]/div/div/div[1]/div/div/div/input",
                        )
                        username_field.send_keys(username)
                        username_field.send_keys(Keys.RETURN)
                        print("Username entered")

                        time.sleep(2)

                        try:
                            try:
                                exisiting_user_alert = driver.find_element(
                                    By.XPATH,
                                    '//*[@id="fluent-default-layer-host"]/div[2]/div/div/div/div[2]/div[2]/div/div[3]/div[3]/div[2]/div[2]',
                                )
                                print("User already exist")
                                return False
                            except:

                                add_button = driver.find_element(
                                    By.XPATH,
                                    '//*[@id="fluent-default-layer-host"]/div[2]/div/div/div/div[2]/div[2]/div/div[3]/div[3]/div[2]/div/div/button',
                                )
                                add_button.click()
                                print("Add button clicked")

                                time.sleep(2)

                                save_changes_button = driver.find_element(
                                    By.XPATH,
                                    '//*[@id="fluent-default-layer-host"]/div[2]/div/div/div/div[2]/div[2]/div/div[5]/div/div/button',
                                )
                                save_changes_button.click()
                                print("Saved button clicked")
                                time.sleep(2)
                                return True
                        except:
                            print("Something went wrong unable to add and save email")
                            return False

                except:
                    # print("Doesnot exist")
                    continue

            time.sleep(2)
            return False
    except Exception as e:
        print(f'Error: {e}')
        return False
    finally:
        driver.quit()
    return False
