import json
import logging
import colorlog
import yaml


def setup_logging():
    """
    Set up the logging configuration with colored output.

    :return: Configured logger object.
    """
    handler = colorlog.StreamHandler()
    handler.setFormatter(colorlog.ColoredFormatter(
        '%(log_color)s%(asctime)s - %(levelname)s - %(message)s',
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

    :return: Loaded cookies as a dictionary or None if the file is not found.
    """
    try:
        logging.info("Attempt to load cookies from cookies.json...")
        with open('cookies.json', 'r') as f:
            logging.info("Successfully loaded cookies from cookies.json.")
            return json.load(f)
    except FileNotFoundError:
        logging.info("cookies.json not found, no saved cookies.")
        return None


def save_cookies(cookies):
    """
    Save cookies to the 'cookies.json' file.

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


logger = setup_logging()