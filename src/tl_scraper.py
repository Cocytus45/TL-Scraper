import requests
from bs4 import BeautifulSoup
import logging

class Scraper:
    def __init__(self) -> None:
        self.url = 'https://www.torrentleech.me'
        
    def login(self, username, password) -> list:
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
        form = soup.find('form', {'name': 'login-form'})
        formdata = {input_tag['name']: input_tag.get('value', '')
                    for input_tag in form.find_all('input')
                    if 'name' in input_tag.attrs}
        formdata['username'] = username
        formdata['password'] = password
        formdata['action'] = 'login'
        formdata['submit'] = 'login'
        response = session.post(self.url, data=formdata)
        if response.status_code == 200:
            original_list = self._extract_(session)
            return [item
                    for item in original_list
                    if item not in ['', 'Get a VPN', 'Get a Seedbox']]
        else:
            logging.error("Login failed.")

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