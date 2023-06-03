import requests
from bs4 import BeautifulSoup
import pyotp
import logging

class Scraper:
    def __init__(self, username:str, password:str, auth_key:str = None) -> None:
        self.url = 'https://www.torrentleech.me'
        self.username = username
        self.password = password
        self.auth_key = auth_key
        
    def login(self) -> list:
        """
        The function logs in a user with a given username and password using
        requests and BeautifulSoup libraries.
        
        :param username: The username of the user trying to log in
        :param password: The password parameter is a string that represents the
        user's password for the login process
        :return: A list is being returned, which is the result of calling the
        `_extract_` method with the `session` object as an argument.
        """
        session = requests.Session()
        login_page = session.get(self.url)
        soup = BeautifulSoup(login_page.content, 'html.parser')
        if self.auth_key is not None:
            response = self.login_with_otp(soup, session)
        else:
            formdata = self.extracted_from_login(soup, 'login-form', 'login', 'login')
            response = session.post(self.url, data=formdata, allow_redirects=True)
        if response.status_code == 200:
            original_list = self._extract_(session)
            return [item
                    for item in original_list
                    if item not in ['', 'Get a VPN', 'Get a Seedbox']]

    def login_with_otp(self, soup, session):
        """
        This function logs in a user with a one-time password (OTP) by
        extracting form data from a login page and submitting it along with the
        OTP to the server.
        
        :param soup: A BeautifulSoup object representing the HTML content of a
        webpage
        :param session: The session parameter is an instance of the
        requests.Session class, which is used to persist certain parameters
        across multiple requests, such as cookies and headers. It allows the
        user to maintain a session with the server and perform multiple requests
        without having to re-authenticate or resend certain data
        :return: the response of a POST request made to a URL with the data
        extracted from the OTP form.
        """
        formdata = self.extracted_from_login(soup, 'login-form', 'login', 'action')
        formdata['submit'] = 'login'
        init_response = session.post(self.url, data=formdata, allow_redirects=False)
        if init_response.status_code == 302 and 'Location' in init_response.headers:
            redirect_url = init_response.headers['Location']
            init_response = session.get(redirect_url)
        soup = BeautifulSoup(init_response.content, 'html.parser')
        code = self.get_verification_code()
        otp_formdata = self.extracted_from_login(soup, 'otp-form', code, 'otpkey')
        continue_button = soup.find('button', {'class': 'button2facontinue'})
        continue_button['disabled'] = ''
        return session.post(self.url, data=otp_formdata, allow_redirects=True)

    def extracted_from_login(self, soup, arg1, arg2, arg3):
        """
        The function extracts input values from a login form and adds the
        username, password, and an additional argument before returning the
        result.
        
        :param soup: A BeautifulSoup object representing the HTML content of a
        webpage
        :param arg1: The value of arg1 is a string representing the name of the
        form that needs to be extracted from the soup object
        :param arg2: It is a value that will be assigned to a key in the
        dictionary named `result`. The specific key is determined by the value
        of the parameter `arg3`
        :param arg3: arg3 is a string parameter that represents the name of a
        form input field that will be added to the dictionary returned by the
        function. The value of this field will be the value of the arg2
        parameter
        :return: The function `extracted_from_login` returns a dictionary
        containing the values of input tags found in a form element of a given
        `soup` object, with additional keys `username`, `password`, and `arg3`
        and their corresponding values.
        """
        form = soup.find('form', {'name': arg1})
        result = {
            input_tag['name']: input_tag.get('value', '')
            for input_tag in form.find_all('input')
            if 'name' in input_tag.attrs
        }
        result['username'] = self.username
        result['password'] = self.password
        result[arg3] = arg2
        return result


    def _extract_(self, session) -> list:
        """
        The function extracts personal data from the webpage and returns them
        as a list.
        
        :param session: The session parameter is an object representing a user's
        session on a website. It is used to make HTTP requests and maintain
        state between requests. In this specific code, it is used to make a GET
        request to a dashboard page and extract information from it
        :return: A list of personal data extracted from the navbar.
        """
        logging.info("Login successful!")
        dashboard_page = session.get(self.url)
        dashboard_soup = BeautifulSoup(dashboard_page.content, 'html.parser')
        links = dashboard_soup.find_all('span', {'class': 'link'})
        links_dict = {link.text.strip(): link for link in links}
        value = list(links_dict)
        for div_item in dashboard_soup.find_all('div', {'class': 'div-menu-item'}):
            title = div_item.get('title')
            if title in ["Buffer", "Ratio", "Hit and Run"]:
                value.append(div_item.text.strip())
        return value
    
    def get_verification_code(self) -> int:
        """
        This function generates a time-based one-time password (TOTP) using the
        provided authentication key and returns it as an integer.
        
        :param auth_key: The auth_key parameter is a string that represents the
        secret key used to generate the verification code. This key is typically
        provided by a two-factor authentication service, such as Google
        Authenticator or Authy. The key is used to generate a time-based
        one-time password (TOTP) that is used to
        :type auth_key: str
        :return: an integer which is the current time-based one-time password
        (TOTP) generated using the provided authentication key.
        """
        totp = pyotp.TOTP(self.auth_key)
        return totp.now()