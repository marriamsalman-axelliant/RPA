import os
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options


def amazon_onboarding_password_set(
    first_name, last_name, email, password, phone_number
):

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
    # driver.save_screenshot("ip_for_amazon_last_step.png")

    driver.get("https://myaccount.microsoft.com/")
    time.sleep(3)
    driver.maximize_window()

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
        feedback_modal = wait.until(
            EC.presence_of_element_located(
                (By.CLASS_NAME, "ms-Modal-scrollableContent")
            )
        )
        print("Feedback modal detected.")

        # Locate and click the close button
        close_button = feedback_modal.find_element(
            By.XPATH, './/button[contains(@class, "ms-Dialog-button--close")]'
        )
        time.sleep(2)
        close_button.click()
        print("Feedback modal closed.")
    except TimeoutException:
        print("No feedback modal detected.")

    driver.get("https://outlook.office.com/mail/ops@flitetransport.com/")

    time.sleep(10)

    onboarding_element = driver.find_element(
        By.XPATH, "//div[@data-folder-name='onboarding']"
    )
    onboarding_element.click()
    print("Clicked on Onboarding Folder.")
    time.sleep(2)

    try:
        search_input = driver.find_element(By.ID, "topSearchInput")
        search_input.clear()
        search_input.send_keys(
            f"To accept this invitation, open the link below and use your email address ({email}) to create a new account."
        )
        time.sleep(2)

        search_input.send_keys(Keys.RETURN)
        print("Entered search parameter.")

        time.sleep(1)

        top_result = driver.find_element(
            By.XPATH,
            "/html/body/div[1]/div/div[2]/div/div[2]/div[2]/div/div/div/div[3]/div/div[2]/div[1]/div[1]/div/div/div/div/div/div/div/div[2]/div/div[2]/div/div/div/div/div[2]",
        )
        time.sleep(1)

        top_result.click()

        print("Clicked on top result.")

        time.sleep(2)

        link = driver.find_element(By.XPATH, "//a[text()='Click here']")
        time.sleep(1)
        link.click()
        print("Clicked on link.")
        time.sleep(3)

        # Switch to the new window (the last opened window will be the new one)
        driver.switch_to.window(driver.window_handles[-1])
        time.sleep(2)

        # Click the "Create Account" button in the new window

        create_account_button = driver.find_element(
            By.XPATH, '//*[@id="app"]/div/main/div/div/div/div/div/button'
        )
        time.sleep(2)

        create_account_button.click()
        print("Clicked on 'Create Account'.")
        time.sleep(5)

        driver.switch_to.window(driver.window_handles[-1])
        time.sleep(2)

        full_name_field = driver.find_element(By.XPATH, '//*[@id="ap_customer_name"]')
        full_name_field.send_keys(Keys.CONTROL, "a")
        full_name_field.send_keys(Keys.BACKSPACE)
        time.sleep(1)

        full_name_field.send_keys(first_name + " " + last_name)
        time.sleep(2)

        email_field = driver.find_element(By.XPATH, '//*[@id="ap_email"]')
        email_field.send_keys(Keys.CONTROL, "a")
        time.sleep(1)
        email_field.send_keys(Keys.BACKSPACE)
        time.sleep(2)

        email_field.send_keys(email)
        time.sleep(3)

        password_field = driver.find_element(By.XPATH, '//*[@id="ap_password"]')
        password_field.send_keys(Keys.CONTROL, "a")
        password_field.send_keys(Keys.BACKSPACE)
        time.sleep(1)

        password_field.send_keys(password)
        time.sleep(3)

        check_password_field = driver.find_element(
            By.XPATH, '//*[@id="ap_password_check"]'
        )
        check_password_field.send_keys(Keys.CONTROL, "a")
        check_password_field.send_keys(Keys.BACKSPACE)
        time.sleep(3)

        check_password_field.send_keys(password)
        time.sleep(3)

        create_your_amazon_account_button = driver.find_element(By.ID, "continue")
        create_your_amazon_account_button.submit()
        time.sleep(5)

        try:
            # Wait for the captcha iframe or the specific header text to appear
            verify_email_address_heading = driver.find_element(
                By.XPATH, '//*[@id="verification-code-form"]/div[1]/div[1]/h1'
            )

            if not verify_email_address_heading:
                print("Captcha detected. Please solve it.")
                input("Solve the captcha and press Enter to continue...")
                # Wait a few seconds to ensure the captcha is resolved
                time.sleep(3)
            else:
                print("No captcha detected.")

        except Exception as e:
            print("Captcha detected. Please solve it.")
            input("Solve the captcha and press Enter to continue...")
            time.sleep(3)

        driver.switch_to.window(driver.window_handles[0])
        driver.refresh()

        time.sleep(2)

        sign_in_element = driver.find_element(
            By.XPATH, "//div[@data-folder-name='sign-in notifications']"
        )
        sign_in_element.click()
        print("Clicked on Sign-In Notifications Folder.")
        time.sleep(5)

        search_input = driver.find_element(By.ID, "topSearchInput")
        search_input.send_keys(Keys.CONTROL, "a")
        time.sleep(2)
        search_input.send_keys(Keys.BACKSPACE)
        time.sleep(1)

        search_input.send_keys(
            f"To verify your email address, please use the following One Time Password (OTP)"
        )
        time.sleep(2)

        # Optionally, simulate pressing Enter
        search_input.send_keys(Keys.RETURN)
        print("Entered search parameter.")

        time.sleep(5)
        try:
            top_result = driver.find_element(
                By.XPATH,
                "/html/body/div[1]/div/div[2]/div/div[2]/div[2]/div/div/div/div[3]/div/div[2]/div[1]/div[1]/div/div/div/div/div/div/div/div[5]/div/div[2]/div/div/div/div",
            )
            time.sleep(1)

            top_result.click()
            print("Clicked on top result.")
            otp = driver.find_element(By.XPATH, '//*[@id="x_verificationMsg"]/p[2]')
            otp = otp.text
            print("Picked the otp.")
            time.sleep(3)
            otp_succes = verify_otp_for_amazon_account(driver, otp)
            if not otp_succes:
                input("Get the otp and fill it yourself...")

        except:
            try:

                def get_date_time_and_otp(xpath):
                    try:
                        top_result = driver.find_element(By.XPATH, xpath)
                    except:
                        print("Email does not exist")
                        return False, None, None
                    try:
                        time.sleep(1)
                        top_result.click()
                        print("Clicked on email.")
                        time.sleep(1)
                        date_time_element = driver.find_element(
                            By.XPATH,
                            "/html/body/div[1]/div/div[2]/div/div[2]/div[2]/div/div/div/div[3]/div/div[2]/div[3]/div/div/div/div[1]/div/div[2]/div/div/div[1]/div/div/div/div/div/div[1]/div[2]/div[2]/div[1]",
                        )
                        date_time_string = date_time_element.text

                        otp = driver.find_element(
                            By.XPATH, '//*[@id="x_verificationMsg"]/p[2]'
                        )
                        otp = otp.text
                        print("Picked the otp.")
                        time.sleep(3)
                        return True, date_time_string, otp
                    except:
                        print("Email otp or time does not exist")
                        return False, None, None

                date_time_and_otp = []
                for n in range(2, 5, 1):
                    success, date_time, otp = get_date_time_and_otp(
                        f"/html/body/div[1]/div/div[2]/div/div[2]/div[2]/div/div/div/div[3]/div/div[2]/div[1]/div[1]/div/div/div/div/div/div/div/div[{n}]"
                    )
                    if success:
                        date_time_and_otp.append([date_time, otp])
                    else:
                        continue

                if date_time_and_otp:
                    datetime_objects = [
                        (datetime.strptime(dt, "%a %m/%d/%Y %I:%M %p"), otp)
                        for dt, otp in date_time_and_otp
                    ]

                    # Find the most recent datetime and corresponding OTP
                    most_recent, otp = max(datetime_objects, key=lambda x: x[0])

                    print(
                        f"The most recent datetime is: {most_recent.strftime('%a %m/%d/%Y %I:%M %p')}"
                    )
                    print(f"The associated OTP is: {otp}")
                    otp_succes = verify_otp_for_amazon_account(driver, otp)
                    if not otp_succes:
                        input("Get the otp and fill it yourself...")

                else:
                    print("No valid datetime and OTP found.")
                    time.sleep(5)
            except:
                input("Get the otp and fill it yourself...")

        try:
            phone_number_field = driver.find_element(
                By.XPATH, '//*[@id="cvfPhoneNumber"]'
            )
            phone_number_field.send_keys(Keys.CONTROL, "a")
            phone_number_field.send_keys(Keys.BACKSPACE)
            time.sleep(2)

            print(len(driver.window_handles))
            driver.execute_script("window.open('');")
            time.sleep(2)
            driver.switch_to.window(driver.window_handles[-1])
            driver.get("https://messages.pingme.tel/")
            time.sleep(5)

            print(len(driver.window_handles))

            try:
                welcome_heading = driver.find_element(
                    By.XPATH, '//*[@id="login"]/div/div[1]'
                )
                if "Welcome" in welcome_heading.text:
                    print("Ping Me Not signed in")
                    input(
                        "Sign in Ping Me manually and then press enter. Make sure to be on Messaged Tab"
                    )

            except:
                print("Ping Me Signed in already")

            try:
                verification_tab = driver.find_element(
                    By.XPATH, '//*[@id="tabs"]/div[1]/div/div[2]/div/div[4]'
                )
                verification_tab.click()
                time.sleep(3)

                get_verification_code_button = driver.find_element(
                    By.XPATH,
                    '//*[@id="app"]/div[1]/main/div/div[1]/section[4]/div/aside/div[2]/button',
                )
                get_verification_code_button.click()
                time.sleep(3)

                website_dropdown = driver.find_element(
                    By.XPATH,
                    "/html/body/div/div[1]/main/div/div[1]/section[4]/div/div/div/section/div[1]/div[2]/div[2]/div[2]/div/div/div[1]/div[1]/input[1]",
                )
                website_dropdown.click()
                website_option = driver.find_element(
                    By.XPATH,
                    "//div[@role='option']//div[@class='v-list-item__content']//div[@class='v-list-item__title' and text()='Amazon']",
                )
                website_option.click()
                time.sleep(2)

                country_dropdown = driver.find_element(
                    By.XPATH,
                    '//*[@id="new-code"]/div[1]/div[2]/div[3]/div[2]/div/div/div[1]',
                )
                country_dropdown.click()
                country_option = driver.find_element(
                    By.XPATH,
                    "//div[contains(text(), 'United States') and contains(text(), '(+1)')]",
                )
                country_option.click()
                time.sleep(2)

                next_button = driver.find_element(
                    By.XPATH, '//*[@id="new-code"]/div[1]/div[4]/button'
                )
                next_button.click()
                time.sleep(4)

                phone_number = driver.find_element(
                    By.XPATH,
                    '//*[@id="new-code"]/div[1]/div[3]/div[2]/div[1]/div[2]/div[2]/div[1]/div[1]',
                )
                phone_number = (phone_number.text).split(" ")[1]
                print("Phone number copied from ping me")
            except:
                print("Unable to get a number")
                return False

            driver.switch_to.window(driver.window_handles[1])
            phone_number_field.send_keys(phone_number)
            print("Typed the phone number.")
            time.sleep(3)
            add_cell_number_button = driver.find_element(
                By.XPATH, '//*[@id="a-autoid-0"]/span/input'
            )
            time.sleep(1)
            add_cell_number_button.click()
            print("Clicked add cell number button.")
            time.sleep(5)

            if (
                driver.find_element(
                    By.XPATH, '//*[@id="cvf-page-content"]/div/div/form/div[1]/div[3]'
                ).text
                == "We've sent a One Time Password (OTP) to your phone number. Please enter it below."
            ):
                driver.switch_to.window(driver.window_handles[-2])

                try:
                    otp_text = driver.find_element(
                        By.XPATH,
                        '//*[@id="new-code"]/div[1]/div[3]/div[2]/div[1]/div[4]/div/div[1]',
                    ).text
                    otp = otp_text.split(" ")[0]
                    driver.switch_to.window(driver.window_handles[-2])

                    otp_code_field = driver.find_element(
                        By.XPATH, '//*[@id="cvf-input-code"]'
                    )
                    otp_code_field.send_keys(Keys.CONTROL, "a")
                    time.sleep(1)
                    otp_code_field.send_keys(Keys.BACKSPACE)
                    time.sleep(2)
                    otp_code_field.send_keys(otp)
                    print("Typed the otp code.")
                    time.sleep(3)

                    create_your_amazon_account_button = driver.find_element(
                        By.XPATH, '//*[@id="a-autoid-0"]/span/input'
                    )
                    time.sleep(1)
                    create_your_amazon_account_button.click()
                    print("Clicked on create your amazon account button.")
                    time.sleep(5)

                    try:
                        WebDriverWait(driver, 10).until(
                            EC.visibility_of_element_located(
                                (
                                    By.XPATH,
                                    "//div[@id='inline-otp-messages']//div[@id='cvf-widget-alert']",
                                )
                            )
                        )
                        print("Phone number validation failed")
                        input("Solve it and make sure to be on Welcome Screen")
                    except:
                        accept_invitation_button = driver.find_element(
                            By.XPATH,
                            '//*[@id="app"]/div/main/div/div/div/div/div/span/button',
                        )
                        accept_invitation_button.click()
                        time.sleep(5)
                        profile_button = wait.until(
                            EC.element_to_be_clickable(
                                (By.XPATH, '//*[@id="mobile-profile-menu-icon"]')
                            )
                        )
                        profile_button.click()
                        print("Profile Button clicked successfully.")
                        time.sleep(1)

                        sign_out_button = wait.until(
                            EC.element_to_be_clickable(
                                (By.XPATH, '//*[@id="fp-profile-menu"]/ul/li[3]/a')
                            )
                        )
                        sign_out_button.click()
                        print("Sign Out Button clicked successfully.")
                        time.sleep(2)
                        return True

                except:
                    print("Phone number validation failed")
                    input("Solve it and make sure to be on Welcome Screen")

        except:
            print("Worked without phone number verification.")
            accept_invitation_button = driver.find_element(
                By.XPATH, '//*[@id="app"]/div/main/div/div/div/div/div/span/button'
            )
            accept_invitation_button.click()
            time.sleep(5)
            profile_button = wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, '//*[@id="mobile-profile-menu-icon"]')
                )
            )
            profile_button.click()
            print("Profile Button clicked successfully.")
            time.sleep(1)

            sign_out_button = wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, '//*[@id="fp-profile-menu"]/ul/li[3]/a')
                )
            )
            sign_out_button.click()
            print("Sign Out Button clicked successfully.")
            time.sleep(2)
            return True

        time.sleep(3)
        input("Complete next steps and press Enter")

    except:
        return False
    finally:
        driver.quit()


def verify_otp_for_amazon_account(driver, otp):
    try:
        driver.switch_to.window(driver.window_handles[-1])
        time.sleep(5)

        otp_field = driver.find_element(By.XPATH, '//*[@id="cvf-input-code"]')
        otp_field.send_keys(Keys.CONTROL, "a")
        time.sleep(1)

        otp_field.send_keys(Keys.BACKSPACE)
        time.sleep(2)

        otp_field.send_keys(otp)
        print("Typed the otp.")
        time.sleep(2)

        verify_button = driver.find_element(
            By.XPATH, '//*[@id="cvf-submit-otp-button"]/span/input'
        )
        time.sleep(1)

        verify_button.click()
        print("Clicked on verify button.")
        time.sleep(3)

        try:
            WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located(
                    (
                        By.XPATH,
                        "//div[@id='inline-otp-messages']//div[contains(@class, 'a-alert-inline-error') and not(contains(@class, 'cvf-hidden'))]",
                    )
                )
            )
            return False
        except:
            return True

    except:
        return False
