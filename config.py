import json
import logging
import colorlog
import yaml
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
import time


def setup_logging():
    """
    Set up the logging configuration with colored output.

    :return: Configured logger object.
    """
    handler = colorlog.StreamHandler()
    handler.setFormatter(colorlog.ColoredFormatter(
        '%(log_color)s%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s',
        log_colors={
            'DEBUG': 'cyan',
            'INFO': 'green',
            'WARNING': 'yellow',
            'ERROR':'red',
            'CRITICAL':'red,bg_white',
        }
    ))
    logger = colorlog.getLogger()
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    return logger


def load_cookies():
    """
    Try to load cookies from the 'cookies.json' file.
    If the file is not found, open the login page, get cookies and save them.

    :return: Loaded cookies as a dictionary or None if an error occurs.
    """
    try:
        logging.info("Attempt to load cookies from cookies.json...")
        with open('cookies.json', 'r') as f:
            logging.info("Successfully loaded cookies from cookies.json.")
            return json.load(f)
    except FileNotFoundError:
        logging.info("cookies.json not found, no saved cookies.")
        cookies = open_login_page_and_get_cookies()
        return cookies


def save_cookies(cookies):
    """
    Save cookies to the '_cookies.json' file.

    :param cookies: Cookies to be saved, in dictionary format.
    """
    logging.info("Saving cookies to cookies.json...")
    with open('cookies.json', 'w') as f:
        json.dump(cookies, f)
    logging.info("Successfully saved cookies to cookies.json.")


def load_headers():
    """
    Load headers from the 'deepseek_headers.yml' file.

    :return: Loaded headers as a dictionary or None if the file is not found.
    """
    try:
        with open('deepseek_headers.yml', 'r', encoding='utf-8') as f:
            headers = yaml.safe_load(f)
            for key, value in headers.items():
                if not isinstance(value, (str, bytes)):
                    headers[key] = str(value)
            logging.info("Successfully loaded headers from deepseek_headers.yml.")
            logging.info(f"Loaded headers: {headers}")
            return headers
    except FileNotFoundError:
        logging.error("deepseek_headers.yml not found.")
        return None


def open_login_page_and_get_cookies():
    """
    Open the login page in Edge browser, wait for user to log in, and then get and save cookies.
    """
    try:
        with open('edge_driver.txt', 'r') as f:
            edge_driver_path = f.read().strip()
    except FileNotFoundError:
        logging.error("edge_driver.txt not found. Please check the file exists and contains the correct path.")
        return None

    edge_options = Options()
    service = Service(edge_driver_path)
    driver = webdriver.Edge(service=service, options=edge_options)

    try:
        driver.get('https://chat.deepseek.com/')
        logging.info("Opening the login page in Edge browser. Please log in manually.")
        input("Press Enter after you have logged in...")
        # Get the cookies
        cookies = driver.get_cookies()
        # Close the browser
        driver.quit()
        logging.info("Browser closed.")
        # Save the cookies
        save_cookies(cookies)
        return cookies
    except Exception as e:
        logging.error(f"An error occurred while getting cookies: {e}")
        return None
    finally:
        driver.quit()

logger = setup_logging()