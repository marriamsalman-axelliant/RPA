import time

from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC


def accept_invitation(driver, wait):
    try:
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
        return True
    except:
        print("Failed to accept invitation")
        return False


def pick_number_and_fill_otp_from_ping_me(driver, wait, phone_number_field):
    try:
        print("Lets move to verification tab")
        verification_tab = wait.until(
            EC.presence_of_element_located(
                (By.XPATH, '//*[@id="tabs"]/div[1]/div/div[2]/div/div[4]')
            )
        )
        verification_tab.click()
        time.sleep(3)

        get_verification_code_button = wait.until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    '//*[@id="app"]/div[1]/main/div/div[1]/section[4]/div/aside/div[2]/button',
                )
            )
        )
        print("Clicking 'Get Verification Code' Button")
        get_verification_code_button.click()
        time.sleep(3)

        website_dropdown = wait.until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    "/html/body/div/div[1]/main/div/div[1]/section[4]/div/div/div/section/div[1]/div[2]/div[2]/div[2]/div/div/div[1]/div[1]/input[1]",
                )
            )
        )
        print("Selecting or reselecting Amazon from website dropdown...")
        website_dropdown.click()
        website_option = driver.find_element(
            By.XPATH,
            "//div[@role='option']//div[@class='v-list-item__content']//div[@class='v-list-item__title' and text()='Amazon']",
        )
        website_option.click()
        time.sleep(2)

        country_dropdown = wait.until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    '//*[@id="new-code"]/div[1]/div[2]/div[3]/div[2]/div/div/div[1]',
                )
            )
        )
        print("Selecting the country....")
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
        print("Clicking the next button...")
        next_button.click()
        time.sleep(4)

        phone_number = driver.find_element(
            By.XPATH,
            '//*[@id="new-code"]/div[1]/div[3]/div[2]/div[1]/div[2]/div[2]/div[1]/div[1]',
        )
        phone_number = (phone_number.text).split(" ")[1]
        print("Phone number copied from ping me")

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
            driver.switch_to.window(driver.window_handles[2])
            otp_text = driver.find_element(
                By.XPATH,
                '//*[@id="new-code"]/div[1]/div[3]/div[2]/div[1]/div[4]/div/div[1]',
            ).text
            otp = otp_text.split(" ")[0]
            driver.switch_to.window(driver.window_handles[1])

            otp_code_field = driver.find_element(By.XPATH, '//*[@id="cvf-input-code"]')
            otp_code_field.send_keys(Keys.CONTROL, "a")
            time.sleep(1)
            otp_code_field.send_keys(Keys.BACKSPACE)
            time.sleep(2)
            otp_code_field.send_keys(otp)
            print("Typed the otp code.")
            time.sleep(1)

            create_your_amazon_account_button = driver.find_element(
                By.XPATH, '//*[@id="a-autoid-0"]/span/input'
            )
            time.sleep(1)
            create_your_amazon_account_button.click()
            print("Clicked on create your amazon account button.")
            time.sleep(5)
        else:
            print("Unable to send the otp")
            user_input = input(
                "Send the otp yourself, complete the process till account invitation screen and press Enter or press Q for quitting."
            )
            if user_input.upper() == "Q":
                print("Quitting...")
                return False
        driver.switch_to.window(driver.window_handles[1])

        return True

    except:
        print("Unable to get a number")
        user_input = input(
            "Get the number yourself, complete the process till account invitation screen and press Enter or press Q for quitting."
        )
        if user_input.upper() == "Q":
            print("Quitting...")
            return False
        driver.switch_to.window(driver.window_handles[1])
        return True


def pick_email_otp(driver):
    try:
        otp = driver.find_element(By.XPATH, '//*[@id="x_verificationMsg"]/p[2]')
        otp = otp.text
        print("Picked the otp.")
        time.sleep(3)
        return True, otp
    except:
        print("Unable to pick up the otp")
        return False, None


def check_phone_number_requirement(wait):
    try:
        phone_number_field = wait.until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="cvfPhoneNumber"]'))
        )
        print("Selecting phone number field...")
        phone_number_field.send_keys(Keys.CONTROL, "a")
        phone_number_field.send_keys(Keys.BACKSPACE)
        time.sleep(2)
        return True, phone_number_field
    except:
        return False, None


def sign_out_from_amazon_driver(wait):
    try:
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
        return False


def pick_otp_and_submit_otp(driver, wait):
    try:
        success_pick_and_open_top_search_result = pick_and_open_top_search_result(
            driver,
            "/html/body/div[1]/div/div[2]/div/div[2]/div[2]/div/div/div/div[3]/div/div[2]/div[1]/div[1]/div/div/div/div/div/div/div/div[5]/div/div[2]/div/div/div/div",
        )
        if not success_pick_and_open_top_search_result:
            return False

        success_pick_email_otp, otp = pick_email_otp(driver)
        if not success_pick_email_otp:
            return False

        success_verify_otp_for_amazon_account = verify_otp_for_amazon_account(
            driver, wait, otp
        )
        if not success_verify_otp_for_amazon_account:
            user_input = input(
                "Get the otp and fill it yourself. Press Enter to continue and Q for quitting..."
            )
            if user_input.upper() == "Q":
                print("Quitting...")
                return False
        else:
            print("Successful OTP Attempt")
    except:
        try:
            date_time_and_otp = []
            for n in range(2, 5, 1):
                success, date_time, otp = get_date_time_and_otp(
                    driver,
                    f"/html/body/div[1]/div/div[2]/div/div[2]/div[2]/div/div/div/div[3]/div/div[2]/div[1]/div[1]/div/div/div/div/div/div/div/div[{n}]",
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
                success_verify_otp_for_amazon_account = verify_otp_for_amazon_account(
                    driver, wait, otp
                )
                if not success_verify_otp_for_amazon_account:
                    user_input = input(
                        "Get the otp and fill it yourself. Press Enter to continue and Q for quitting..."
                    )
                    if user_input.upper() == "Q":
                        print("Quitting...")
                        return False
                else:
                    print("Successful OTP Attempt")
            else:
                print("No valid datetime and OTP found.")
                time.sleep(5)
        except:
            user_input = input(
                "Get the otp and fill it yourself. Press Enter to continue and Q for quitting..."
            )
            if user_input.upper() == "Q":
                print("Quitting...")
                return False
    return True


def open_create_account_link_and_submit_form(
    driver, wait, first_name, last_name, password
):
    try:
        link = driver.find_element(By.XPATH, "//a[text()='Click here']")
        time.sleep(1)
        link.click()
        print("Clicked on link.")
        time.sleep(5)
    except:
        print("Unable to click on click here link")
        return False

    try:
        driver.switch_to.window(driver.window_handles[1])
        time.sleep(2)
        # Click the "Create Account" button in the new window
        create_account_button = wait.until(
            EC.presence_of_element_located(
                (By.XPATH, '//*[@id="app"]/div/main/div/div/div/div/div/button')
            )
        )
        time.sleep(2)
        create_account_button.click()
        print("Clicked on 'Create Account'.")
        time.sleep(5)

        full_name_field = wait.until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="ap_customer_name"]'))
        )
        full_name_field.send_keys(Keys.CONTROL, "a")
        full_name_field.send_keys(Keys.BACKSPACE)
        time.sleep(1)
        full_name_field.send_keys(first_name + " " + last_name)
        time.sleep(2)

        # email_field = driver.find_element(By.XPATH, '//*[@id="ap_email"]')
        # email_field.send_keys(Keys.CONTROL, "a")
        # time.sleep(1)
        # email_field.send_keys(Keys.BACKSPACE)
        # time.sleep(1)

        # email_field.send_keys(email)
        # time.sleep(1)

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
    except:
        print("Something went wrong in filling and submitting the form.")
        return False

    try:
        # Wait for the captcha iframe or the specific header text to appear
        verify_email_address_heading = wait.until(
            EC.presence_of_element_located(
                (By.XPATH, '//*[@id="verification-code-form"]/div[1]/div[1]/h1')
            )
        )
        if not verify_email_address_heading:
            print("Captcha detected. Please solve it.")
            user_input = input("Press Enter to continue and press Q for quitting...")
            if user_input.upper() == "Q":
                print("Quitting...")
                return False
            time.sleep(3)
        else:
            print("No captcha detected.")
        return True

    except Exception as e:
        print("Captcha detected. Please solve it.")
        user_input = input("Press Enter to continue and press Q for quitting...")
        if user_input.upper() == "Q":
            print("Quitting...")
            return False
        time.sleep(3)
        return True


def pick_and_open_top_search_result(driver, xpath):
    try:
        top_result = driver.find_element(By.XPATH, xpath)
        time.sleep(1)

        top_result.click()

        print("Clicked on top result.")

        time.sleep(2)
        return True
    except:
        return False


def email_search(driver, search_string):
    try:
        search_input = driver.find_element(By.ID, "topSearchInput")
        search_input.send_keys(Keys.CONTROL, "a")
        time.sleep(2)
        search_input.send_keys(Keys.BACKSPACE)
        time.sleep(1)
        search_input.send_keys(search_string)
        time.sleep(2)
        search_input.send_keys(Keys.RETURN)
        print("Entered search parameter.")
        time.sleep(1)
        return True
    except:
        print("Email Search Failed")
        return False


def open_folder(driver, wait, folder_name):
    try:

        driver.switch_to.window(driver.window_handles[0])
        driver.get("https://outlook.office.com/mail/ops@flitetransport.com/")
        time.sleep(5)

        folder_element = wait.until(
            EC.presence_of_element_located(
                (By.XPATH, f"//div[@data-folder-name='{folder_name}']")
            )
        )

        folder_element.click()
        print(f"Clicked on {folder_name} Folder.")
        time.sleep(2)
        return True
    except:
        print(f"Failed to open {folder_name}.")
        return False


def verify_otp_for_amazon_account(driver, wait, otp):
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
            wait.until(
                EC.visibility_of_element_located(
                    (
                        By.XPATH,
                        "//div[@id='inline-otp-messages']//div[contains(@class, 'a-alert-inline-error') and not(contains(@class, 'cvf-hidden'))]",
                    )
                )
            )
            print("Wrong OTP")
            return False
        except:
            print("Correct OTP")
            return True

    except:
        return False


def get_date_time_and_otp(driver, xpath):
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

        success_pick_email_otp, otp = pick_email_otp(driver)
        if not success_pick_email_otp:
            return False, None, None

        return True, date_time_string, otp
    except:
        print("Email otp or time does not exist")
        return False, None, None
