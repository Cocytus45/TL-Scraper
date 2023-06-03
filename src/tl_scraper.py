import pyotp
from requests import Session
from bs4 import BeautifulSoup


class Scraper:
    def __init__(self, 
                 username: str, 
                 password: str, 
                 auth_key: str = None, 
                 url: str = 'https://www.torrentleech.me'):
        """
        This is a constructor function that initializes the object with a URL,
        username, password, and an optional authentication key.
        
        :param username: A string representing the username of the user trying
        to access the website
        :type username: str
        :param password: The password parameter is a string that represents the
        user's password for their TorrentLeech account
        :type password: str
        :param auth_key: The auth_key parameter is an optional parameter that
        can be used to store an authentication key for the user. This key can be
        used to authenticate the user's requests to the website. If the auth_key
        is not provided, the user will need to authenticate themselves using
        their username and password each time they make
        :type auth_key: str
        """
        self.url = url
        self.username = username
        self.password = password
        self.auth_key = auth_key

    def get_verification_code(self) -> int:
        """
        This function returns a time-based one-time password (TOTP) generated
        using a given authentication key.
        :return: an integer which is the current time-based one-time password
        (TOTP) generated using the provided authentication key.
        """
        totp = pyotp.TOTP(self.auth_key)
        return totp.now()

    def login(self) -> list:  # sourcery skip: extract-method
        # with extraction caused a 17.0453% increase in speed on average.
        """
        The function logs into a website and returns a list of personal data
        from the navbar.
        :return: A list of links or menu items that are available after logging
        in, excluding some specific items like "Get a VPN" or "Get a Seedbox".
        If the login is unsuccessful, an empty list is returned.
        """
        session = Session()
        login_page = session.get(self.url)
        soup = BeautifulSoup(login_page.content, 'html.parser')

        form = soup.find('form', {'name': 'login-form'})
        formdata = {
            input_tag['name']: input_tag.get('value', '')
            for input_tag in form.find_all('input')
            if 'name' in input_tag.attrs
        }
        formdata['username'] = self.username
        formdata['password'] = self.password

        if self.auth_key is not None:
            formdata['otpkey'] = self.get_verification_code()

        response = session.post(self.url, data=formdata, allow_redirects=True)

        if response.status_code == 200:
            dashboard_soup = BeautifulSoup(response.content, 'html.parser')
            links = dashboard_soup.find_all('span', {'class': 'link'})
            links_dict = {link.text.strip(): link for link in links}
            value = list(links_dict)

            for div_item in dashboard_soup.find_all('div', {'class': 'div-menu-item'}):
                title = div_item.get('title')
                if title in ["Buffer", "Ratio", "Hit and Run"]:
                    value.append(div_item.text.strip())

            return [item
                    for item in value
                    if item not in ['', 'Get a VPN', 'Get a Seedbox']]
        return []