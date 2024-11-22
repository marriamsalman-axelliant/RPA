from amazon_last_step_onboarding_utils import (
    email_search,
    check_phone_number_requirement,
    pick_number_and_fill_otp_from_ping_me,
    pick_otp_and_submit_otp,
    sign_out_from_amazon_driver,
    open_folder,
    open_create_account_link_and_submit_form,
    pick_and_open_top_search_result,
    accept_invitation,
)
from initial_auth_utils import (
    initial_setup_msops_fleetio_and_amazon_last_step,
    ms_ops_auth,
    ping_me_initial_process_and_auth,
)


def amazon_onboarding_password_set(
    first_name, last_name, email, password, phone_number
):

    success_initial_setup_msops_fleetio_and_amazon_last_step, driver, wait = (
        initial_setup_msops_fleetio_and_amazon_last_step()
    )
    if not success_initial_setup_msops_fleetio_and_amazon_last_step:
        return False

    success_ms_ops_auth = ms_ops_auth(driver, wait)
    if not success_ms_ops_auth:
        return False

    success_open_onboarding_folder = open_folder(driver, wait, "onboarding")
    if not success_open_onboarding_folder:
        return False

    try:
        search_string = f"To accept this invitation, open the link below and use your email address ({email}) to create a new account."
        success_email_search = email_search(driver, search_string)
        if not success_email_search:
            return False

        success_pick_and_open_top_search_result = pick_and_open_top_search_result(
            driver,
            "/html/body/div[1]/div/div[2]/div/div[2]/div[2]/div/div/div/div[3]/div/div[2]/div[1]/div[1]/div/div/div/div/div/div/div/div[2]/div/div[2]/div/div/div/div/div[2]",
        )
        if not success_pick_and_open_top_search_result:
            return False

        success_open_create_account_link_and_submit_form = (
            open_create_account_link_and_submit_form(
                driver, wait, first_name, last_name, password
            )
        )
        if not success_open_create_account_link_and_submit_form:
            return False

        success_open_sign_in_notifications_folder = open_folder(
            driver, wait, "sign-in notifications"
        )
        if not success_open_sign_in_notifications_folder:
            return False

        search_string = f"To verify your email address, please use the following One Time Password (OTP)"

        success_email_search = email_search(driver, search_string)
        if not success_email_search:
            return False

        success_pick_otp_and_submit_otp = pick_otp_and_submit_otp(driver, wait)
        if not success_pick_otp_and_submit_otp:
            return False

        success_phone_number_field, phone_number_field = check_phone_number_requirement(
            wait
        )
        if not success_phone_number_field:
            print("Worked without phone number verification.")

            success_accept_invitation = accept_invitation(driver, wait)
            if not success_accept_invitation:
                return False

            success_sign_out_from_amazon_driver = sign_out_from_amazon_driver(wait)
            if not success_sign_out_from_amazon_driver:
                return False
            return True

        else:

            success_ping_me_initial_process_and_auth = ping_me_initial_process_and_auth(
                driver
            )
            if not success_ping_me_initial_process_and_auth:
                return False

            success_pick_number_from_ping_me = pick_number_and_fill_otp_from_ping_me(
                driver, wait, phone_number_field
            )
            if not success_pick_number_from_ping_me:
                return False

            success_accept_invitation = accept_invitation(driver, wait)
            if not success_accept_invitation:
                return False

            success_sign_out_from_amazon_driver = sign_out_from_amazon_driver(wait)
            if not success_sign_out_from_amazon_driver:
                return False
            return True

    except:
        return False
    finally:
        driver.quit()
