import json
import os
from config import FILE_PATH
from logger import setup_logger

logger = setup_logger()

# Credentials Handling
def load_credentials():
    credentials_file = os.path.join(FILE_PATH, 'filelist_credentials.json')
    try:
        with open(credentials_file, mode='r', encoding='UTF-8') as file:
            credentials = json.load(file)
            logger.debug('Credentials loaded from file.')
    except FileNotFoundError:
        logger.debug('Using default credentials for authentication.')
        credentials = {'username': 'write_here_your_account_username', 'password': 'write_here_your_account_password'}
    return credentials
