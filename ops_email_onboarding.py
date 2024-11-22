import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from initial_auth_utils import initial_setup_msops_fleetio_and_amazon_last_step, ms_ops_auth
from ops_utils import navigate_to_email_aliases_tab, add_email_alias


def add_username_on_ops_email(username=None):

    success_initial_setup_msops_fleetio_and_amazon_last_step, driver, wait = (
        initial_setup_msops_fleetio_and_amazon_last_step()
    )
    if not success_initial_setup_msops_fleetio_and_amazon_last_step:
        return False

    try:
        success_ms_ops_auth = ms_ops_auth(driver, wait)
        if not success_ms_ops_auth:
            return False

        success_navigate_to_email_aliases_tab = navigate_to_email_aliases_tab(
            driver, wait
        )
        if not success_navigate_to_email_aliases_tab:
            return False

        success_add_email_alias = add_email_alias(driver, wait, username)
        if not success_add_email_alias:
            return False
        
        return True
    except Exception as e:
        print("Something went wrong. Error:", str(e))
        return False

    finally:
        driver.quit()
