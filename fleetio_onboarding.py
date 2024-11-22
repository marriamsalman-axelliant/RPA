import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from initial_auth_utils import (
    initial_setup_msops_fleetio_and_amazon_last_step,
    fleetio_auth,
)
from fleetio_utils import navigate_to_fleetio_dashboard, add_contact


def driver_fleetio_onboarding(first_name, last_name, location, username, password):

    success_initial_setup_msops_fleetio_and_amazon_last_step, driver, wait = (
        initial_setup_msops_fleetio_and_amazon_last_step()
    )
    if not success_initial_setup_msops_fleetio_and_amazon_last_step:
        return False

    try:
        success_fleetio_auth = fleetio_auth(driver, wait)
        if not success_fleetio_auth:
            return False

        # success_navigate_to_fleetio_dashboard = navigate_to_fleetio_dashboard(
        #     driver, wait
        # )
        # if not success_navigate_to_fleetio_dashboard:
        #     return False

        success_add_contact = add_contact(
            driver, wait, first_name, last_name, location, username, password
        )
        if not success_add_contact:
            return False

        return True

    except Exception as e:
        print(f"Something went wrong in fleetio onboarding:{e}")
        return False
    finally:
        driver.quit()
