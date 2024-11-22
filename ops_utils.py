import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


def navigate_to_email_aliases_tab(driver, wait):
    try:
        driver.get("https://admin.microsoft.com/Adminportal/Home#/homepage")

        wait.until(EC.presence_of_element_located((By.ID, "DashboardSwitcher")))

        users_dropdown_button = driver.find_element(By.NAME, "Users")
        users_dropdown_button.click()
        time.sleep(4)

        active_users_button = wait.until(
            EC.presence_of_element_located((By.NAME, "Active users"))
        )

        if active_users_button.is_displayed():
            time.sleep(2)
            active_users_button.click()
            print("Clicked the active user button.")
            time.sleep(2)
            if "users" in driver.current_url:
                print("Active user tab opened")
                active_users = driver.find_elements(By.CLASS_NAME, "ms-List-cell")

                for active_user in active_users:
                    try:
                        time.sleep(4)
                        ops_text = active_user.find_element(
                            By.XPATH, ".//span[text()='ops']"
                        )
                        if (
                            ops_text.get_attribute("role") == "button"
                            and ops_text.text == "ops"
                        ):
                            ops_text.click()
                            print("Clicked on Ops Active User")
                            time.sleep(5)
                            try:
                                email_aliases_button = driver.find_element(
                                    By.CSS_SELECTOR,
                                    "button[humanfriendlyname='ManageEmail'][data-automation-id='UserDetailPanelRegion,ManageEmailLink']",
                                )

                                email_aliases_button.click()
                                time.sleep(3)
                                return True
                            except:
                                print("Unable to locate add email aliases option")
                                return False

                    except:
                        continue
                print("Unable to find Ops User")
                return False
            else:
                print("Unable to locate to active drivers")
                return False

        else:
            print("Unable to locate to active users tab")
            return False
    except:
        print("Unable to locate to active drivers")
        return False


def add_email_alias(driver, wait, username):

    try:
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
        print("Something went wrong unable to add and save email")
        return False
