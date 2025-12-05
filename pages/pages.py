from typing import Union
from playwright.sync_api import Page, Locator

from pages.controls import RadioButton, SearchFlightsControl
from utils.utils import load_config

DEFAULT_TIMEOUT = load_config("test.json").get("timeout", 20000)

class BasePage:
    """Base page class with common methods"""
    
    def __init__(self, page: Page):
        self.page = page
    
    def navigate_to(self, url: str):
        """Navigate to a URL"""
        self.page.goto(url)
    
    def get_title(self) -> str:
        """Get page title"""
        return self.page.title()
    
    def wait_for_load(self, timeout: int = DEFAULT_TIMEOUT):
        """Wait for page to load"""
        self.page.wait_for_load_state("networkidle", timeout=timeout)

class PrivacyPage(BasePage):
    '''Page object for privacy settings'''

    def __init__(self, page: Page):
        super().__init__(page)
        self.accept_cookies_button = self.page.locator('[data-test="CookiesPopup-Accept"]')

    def accept_cookies(self):
        """Accept cookies if the popup is visible"""
        if self.accept_cookies_button.is_visible():
            self.accept_cookies_button.click()
            self.accept_cookies_button.wait_for(state="hidden")

class KiwiStartPage(BasePage):
    """Page object for Kiwi.com start page"""
    
    def __init__(self, page: Page):
        super().__init__(page)
        self.SearchFlightsControl = SearchFlightsControl(page)
    
    def wait_for_load(self, timeout: int = DEFAULT_TIMEOUT):
        self.SearchFlightsControl.wait_until_visible(timeout=timeout)

    def navigate_to(self, accept_cookies: bool = True, url: Union[str, None] = None):
        if url is None:
            url = load_config("test.json").get("base_url", "https://www.kiwi.com/en/")
        super().navigate_to(url)
        self.wait_for_load()
        if accept_cookies:
            PrivacyPage(self.page).accept_cookies()

class SearchResultsPage(BasePage):
    """Page object for search results functionality"""
    
    def __init__(self, page: Page):
        super().__init__(page)
        self.loading_line = self.page.locator('[data-test="LoadingLine"]')
        self.results_list = self.page.locator('[data-test="ResultList-results"]')
    
    def wait_for_results(self, timeout: int = DEFAULT_TIMEOUT):
        """Wait for search results to load"""
        self.loading_line.wait_for(timeout=timeout)
        self.results_list.wait_for()
