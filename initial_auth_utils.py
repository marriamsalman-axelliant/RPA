import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException


def initial_setup_amazon_and_shell():
    try:
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
        wait = WebDriverWait(driver, 10)
        return True, driver, wait
    except:
        print("Failed to initialize chrome")
        return False, None, None


def initial_setup_msops_fleetio_and_amazon_last_step():
    try:
        chromedriver_path = "/home/marriam/Downloads/k/chromedrivernn"
        user_data_dir = "/home/marriam/Downloads/d/chrome-user-data-ms"

        # Set Chrome options
        chrome_options = Options()
        chrome_options.add_argument(f"user-data-dir={user_data_dir}")
        chrome_options.add_argument("--profile-directory=Default")
        chrome_options.add_argument("--start-maximized")

        # Start ChromeDriver
        service = Service(chromedriver_path)
        driver = webdriver.Chrome(service=service, options=chrome_options)
        wait = WebDriverWait(driver, 10)
        return True, driver, wait
    except:
        print("Failed to initialize chrome")
        return False, None, None


def amazon_auth(driver, wait):
    try:
        # driver.get("https://mylocation.org")
        # driver.save_screenshot("ip_for_amazon.png")
        # Open Amazon DSP Account Management page
        driver.get("https://logistics.amazon.ca/dsp-account-management/")
        print("Tab title: ", driver.title)

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
                user_input = input(
                    "Press Enter if successfully logged in or Q to quit: "
                )
                if user_input.upper() == "Q":
                    print("Quitting...")
            else:
                print("Logged in successfully.")

        else:
            print("Already logged in!")
    except:
        print("Sign in and make sure to be on homepage.")
        user_input = input("Press Enter if successfully logged in or Q to quit: ")
        if user_input.upper() == "Q":
            print("Quitting...")
            return False

    return True


def ms_ops_auth(driver, wait):

    try:
        # driver.get("https://mylocation.org")
        # driver.save_screenshot("ip_for_ops.png")

        driver.get("https://myaccount.microsoft.com/")
        time.sleep(3)

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
            user_input = input(
                "Please complete the MFA process. Press Enter once done or Q to quit: "
            )
            if user_input.upper() == "Q":
                print("Quitting...")
                return False

            if "My" in driver.title:
                print("Logged in successfully!")
            else:
                print("Please Sign in.")
                user_input = input(
                    "Press Enter if successfully logged in or Q to quit: "
                )
                if user_input.upper() == "Q":
                    print("Quitting...")
                    return False

        elif "My" in driver.title:
            print("Already logged in successfully!")
        else:
            print("Please Sign in.")
            user_input = input("Press Enter if successfully logged in or Q to quit: ")
            if user_input.upper() == "Q":
                print("Quitting...")
                return False

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

        return True
    except Exception as e:
        print(f"Failed to login to ms ops: {e}")
        return False


def shell_auth(driver, wait):
    try:
        #     driver.get("https://mylocation.org")
        #     driver.save_screenshot("ip_for_shell.png")

        driver.get("https://shellaccountmanager.ca/home")
        print("Tab title: ", driver.title)
        time.sleep(7)

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
                user_input = input(
                    "Approve the push request and press Enter or Q to quit: "
                )
                if user_input.upper() == "Q":
                    print("Quitting...")
                    return False

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
        print("Logged in")
        return True

    except:
        user_input = input(
            "ailed to Login. Login and press Enter if successfully logged in or Q to quit: "
        )
        if user_input.upper() == "Q":
            print("Quitting...")
            return False


def fleetio_auth(driver, wait):
    try:

        # driver.get("https://mylocation.org")
        # driver.save_screenshot("ip_for_fleetio.png")
        driver.get("https://secure.fleetio.com/users/sign_in")
        time.sleep(3)

        if "dashboard" not in driver.current_url:
            fleetio_username_field = wait.until(
                EC.presence_of_element_located((By.ID, "user_login"))
            )
            fleetio_username_field.clear()
            fleetio_username_field.click()
            fleetio_username_field.send_keys(os.getenv("FLEETIO_USERNAME"))
            print("Username Entered.")
            time.sleep(2)

            fleetio_password_field = wait.until(
                EC.presence_of_element_located((By.ID, "user_password"))
            )
            fleetio_password_field.clear()
            fleetio_password_field.click()
            fleetio_password_field.send_keys(os.getenv("FLEETIO_PASSWORD"))
            print("Password Entered.")
            time.sleep(1)

            remember_me_button = wait.until(
                EC.presence_of_element_located((By.ID, "user_remember_me"))
            )
            remember_me_button.click() if not remember_me_button.is_selected() else None
            print("Remember me button toggled.")
            time.sleep(1)

            login_button = wait.until(
                EC.presence_of_element_located(
                    (By.XPATH, '//*[@id="new_user"]/div[6]/input')
                )
            )
            login_button.submit()
            time.sleep(3)
            if "dashboard" not in driver.current_url:
                print("Logged in")
            else:

                print("Please login and make sure to be on dashboard.")
                user_input = input(
                    "Press Enter if successfully logged in or Q to quit: "
                )
                if user_input.upper() == "Q":
                    print("Quitting...")
                    return False

        else:
            print("Logged in")
            return True
    except:
        print("Unable to load fleetio site")
        return False


def ping_me_initial_process_and_auth(driver):
    try:
        print("Lets pick a number from ping me")
        driver.execute_script("window.open('');")
        time.sleep(2)
        driver.switch_to.window(driver.window_handles[-1])
        print("Opening ping me site...")
        driver.get("https://messages.pingme.tel/")
        time.sleep(5)

        try:
            welcome_heading = driver.find_element(
                By.XPATH, '//*[@id="login"]/div/div[1]'
            )
            if "Welcome" in welcome_heading.text:
                print("Ping Me Not signed in")
                user_input = input(
                    "Sign in Ping Me manually and then press enter. Make sure to be on Messaged Tab or Q to quit:"
                )

                if user_input.upper() == "Q":
                    print("Quitting...")
                    return False

        except:
            print("Ping Me Signed in already")
        return True

    except:
        print("Failed to sign in Ping Me")
        user_input = input(
            "Sign in Ping Me manually and then press enter. Make sure to be on Messaged Tab or Q to quit:"
        )

        if user_input.upper() == "Q":
            print("Quitting...")
            return False
        return True
