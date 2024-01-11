from http.client import HTTPResponse
from http.cookiejar import CookieJar
from urllib.parse import urlencode
from urllib.request import HTTPCookieProcessor, build_opener
import re

from config import USER_AGENT, MAX_REQ_RETRIES, MAX_PAGES
from logger import setup_logger
from credentials import load_credentials
from regex_patterns import RE_PATTERNS
from novaprinter import prettyPrinter

class Filelist:
    url = 'https://filelist.io'
    name = 'FileList'
    supported_categories = {
        'all': '0', 'movies': '19', 'tv': '21',
        'music': '11', 'games': '9', 'anime': '24', 'software': '8'
    }
    url_dl = url + '/download.php?id='
    url_login = url + '/login.php'
    url_login_post = url + '/takelogin.php'
    url_search = url + '/browse.php?search'
    url_details = url + '/details.php?id='
    url_download = url + '/download.php?id='
    critical_error = False
    request_retry = 0

    cj = CookieJar()
    session = build_opener(HTTPCookieProcessor(cj))
    session.addheaders = [USER_AGENT]

    def __init__(self):
        self.logger = setup_logger()
        self.credentials = load_credentials()
        self.logger.debug('New Filelist object created.')
        self._login()

    def _login(self):
        if self.credentials['username'] == 'your_username_here' or self.credentials['password'] == 'your_password_here':
            self.logger.critical('Please provide a username or password.')
            self.critical_error = True
            return

        login_page = self._make_request(self.url_login)
        if not login_page:
            self.logger.critical("Could not access login page!")
            self.critical_error = True
            return

        validator_match = re.search(RE_PATTERNS['validator'], login_page)
        if not validator_match:
            self.logger.critical('Could not retrieve validator key!')
            self.critical_error = True
            return

        payload = {
            'unlock': '1',
            'returnto': '%2F',
            'username': self.credentials['username'],
            'password': self.credentials['password'],
            'validator': validator_match.group(1)
        }

        encoded_payload = urlencode(payload).encode()
        main_page = self._make_request(self.url_login_post, data=encoded_payload)
        if main_page:
            self.logger.info('Logged in successfully.')

    def _make_request(self, url, data=None, decode=True):        
        if data:
            self.logger.debug(f"POST request to {url}")
        else:
            self.logger.debug(f"GET request to {url}")

        if self.request_retry > MAX_REQ_RETRIES:
            self.request_retry = 0
            return None

        try:
            with self.session.open(url, data=data, timeout=10) as response:
                response: HTTPResponse
                self.logger.debug(f"Response status: {response.status}")
                if response.status != 200:
                    self.logger.error(f"HTTP error {response.status}")
                    self.critical_error = True
                    return None

                content = response.read()
                return content.decode('UTF-8', 'replace') if decode else content

        except HTTPError as e:
            self.logger.error(f"HTTP error: {e}")
            self.critical_error = True
        except URLError as e:
            self.logger.error(f"URL error: {e.reason}")
            self.request_retry += 1
            return self._make_request(url, data, decode)
        except TimeoutError:
            self.logger.error("Request timed out")
            self.request_retry += 1
            return self._make_request(url, data, decode)

    def download_torrent(self, url):
        if self.critical_error:
            self._return_error()
            return

        response = self._make_request(url, decode=False)
        if response:
            with NamedTemporaryFile(suffix=".torrent", delete=False) as temp_file:
                temp_file.write(response)
                self.logger.info(f"Torrent downloaded: {temp_file.name}")
                print(f"{temp_file.name} {url}")

    def search(self, what, cat='all'):
        if self.critical_error:
            self._return_error()
            return

        what = what.replace(' ', '+')
        cat = self.supported_categories.get(cat, '0')

