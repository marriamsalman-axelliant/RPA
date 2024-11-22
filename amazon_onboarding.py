import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains


from initial_auth_utils import amazon_auth, initial_setup_amazon_and_shell
from amazon_utils import (
    navigate_to_add_associate_page,
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
    success_initial_setup_amazon_and_shell, driver, wait = (
        initial_setup_amazon_and_shell()
    )
    if not success_initial_setup_amazon_and_shell:
        return False

    try:
        success_amazon_auth = amazon_auth(driver, wait)
        if not success_amazon_auth:
            return False

        success_navigate_to_add_associate_page = navigate_to_add_associate_page(
            driver, wait
        )
        if not success_navigate_to_add_associate_page:
            return False

        basic_info_onboarding_success, amazon_profile_url = basic_info_onboarding(
            driver, wait, location, first_name, last_name, email
        )
        if not basic_info_onboarding_success:
            return False

        # amazon_profile_url = "https://logistics.amazon.ca/account-management/delivery-associates/detail/amzn1.flex.provider.v1.5d432363-0268-464c-8dae-3ee4ff35fa71"

        edit_photo_success = edit_photo(driver, wait, amazon_profile_url)
        if not edit_photo_success:
            return False

        edit_dob_and_licence_details_success = edit_dob_and_licence_details(
            driver, wait, amazon_profile_url, dob, license_expiry_date, driver_license
        )
        if not edit_dob_and_licence_details_success:
            return False

        verify_and_update_associate_settings_success = (
            verify_and_update_associate_settings(
                driver, wait, amazon_profile_url, location
            )
        )
        if not verify_and_update_associate_settings_success:
            return False

        expand_onboarding_section_success = expand_onboarding_section(
            driver,
            wait,
            amazon_profile_url,
            '//*[@id="dsp-onboarding"]/div/main/div/div[4]/div/div[1]/i',
        )
        if not expand_onboarding_section_success:
            return False

        verify_onboarding_initial_progress_success = verify_onboarding_progress(
            driver,
            wait,
            amazon_profile_url,
            onboarding_progress_xpath="//span[contains(@class, 'af-accordion__right-label')]",
            expected_progress="4 of 11 Completed",
        )
        if not verify_onboarding_initial_progress_success:
            return False

        driver_record_verification_task_success = complete_task(
            driver,
            wait,
            amazon_profile_url,
            "Driver record verification",
            '//*[@id="dsp-onboarding"]/div/main/div/div[4]/div/div[2]/div/div[1]/div[1]/div[1]/div/h3/a',
            '//*[@id="manual-task-yes"]',
            '//*[@id="dsp-onboarding"]/div/main/div/span[5]/div/div/div[2]/div[2]/button[1]',
        )
        if not driver_record_verification_task_success:
            return False

        drug_test_task_success = complete_task(
            driver,
            wait,
            amazon_profile_url,
            "Drug test",
            '//*[@id="dsp-onboarding"]/div/main/div/div[4]/div/div[2]/div/div[1]/div[6]/div[1]/div/h3/a',
            '//*[@id="manual-task-yes"]',
            '//*[@id="dsp-onboarding"]/div/main/div/span[5]/div/div/div[2]/div[2]/button[1]',
        )
        if not drug_test_task_success:
            return False

        background_check_task_success = complete_task(
            driver,
            wait,
            amazon_profile_url,
            "Background check",
            '//*[@id="dsp-onboarding"]/div/main/div/div[4]/div/div[2]/div/div[1]/div[7]/div[1]/div/h3/a',
            '//*[@id="manual-task-yes"]',
            '//*[@id="dsp-onboarding"]/div/main/div/span[5]/div/div/div[2]/div[2]/button[1]',
        )
        if not background_check_task_success:
            return False

        training_task_success = complete_task(
            driver,
            wait,
            amazon_profile_url,
            "Training",
            '//*[@id="dsp-onboarding"]/div/main/div/div[4]/div/div[2]/div/div[1]/div[8]/div[1]/div/h3/a',
            '//*[@id="manual-task-yes"]',
            '//*[@id="dsp-onboarding"]/div/main/div/span[5]/div/div/div[2]/div[2]/button[1]',
        )
        if not training_task_success:
            return False

        verify_onboarding_final_progress_success = verify_onboarding_progress(
            driver,
            wait,
            amazon_profile_url,
            onboarding_progress_xpath="//span[contains(@class, 'af-accordion__right-label')]",
            expected_progress="8 of 11 Completed",
        )
        if not verify_onboarding_final_progress_success:
            return False

        # logout_success = logout(driver, wait)     #  in progress
        # if not logout_success:
        #     return False
        return True
    except Exception as e:
        print("Something went wrong. Error:", str(e))
        return False

    finally:
        driver.quit()
