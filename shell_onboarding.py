from initial_auth_utils import initial_setup_amazon_and_shell, shell_auth
from shell_utils import navigate_to_cards_and_add_driver


def driver_shell_onboarding(
    first_name, last_name, email, driver_license, license_expiry_date, phone_number
):
    success_initial_setup_amazon_and_shell, driver, wait = (
        initial_setup_amazon_and_shell()
    )
    if not success_initial_setup_amazon_and_shell:
        return False, None

    try:

        success_shell_auth = shell_auth(driver, wait)
        if not success_shell_auth:
            return False, None

        success_navigate_to_cards_and_add_driver, driver_prompt_id = (
            navigate_to_cards_and_add_driver(
                driver,
                wait,
                first_name,
                last_name,
                email,
                driver_license,
                license_expiry_date,
                phone_number,
            )
        )
        if not success_navigate_to_cards_and_add_driver:
            return False, None

        return True, driver_prompt_id
    except:
        print("Something went wrong in shell onboarding")
        return False, None
    finally:
        # Close the driver when done
        driver.quit()
