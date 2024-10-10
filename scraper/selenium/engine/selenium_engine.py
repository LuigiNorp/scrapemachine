import time
import random
import logging
from selenium import webdriver
from selenium.common import (
    TimeoutException, StaleElementReferenceException,
    ElementNotInteractableException, NoSuchElementException)
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService
from django.contrib import messages


logger = logging.getLogger(__name__)


class SeleniumEngine:
    def __init__(self, driver_path: str, request):
        """Initialize Selenium engine."""
        self.pagination = None
        self.driver_path = driver_path
        self.driver = self._setup_driver()
        self.request = request

    def _setup_driver(self):
        """Sets up the Selenium WebDriver."""
        opts = Options()
        opts.add_argument('--no-sandbox')
        opts.add_argument('--headless')
        service = ChromeService(executable_path=self.driver_path)
        return webdriver.Chrome(service=service, options=opts)

    @staticmethod
    def random_sleep(min_time=1, max_time=3):
        """Pauses execution for a random amount of time."""
        time.sleep(random.uniform(min_time, max_time))

    @staticmethod
    def handle_exceptions(exception, message, request):
        """Handles different exceptions and logs errors."""
        logger.error(exception)
        messages.error(request, message)

    def find_next_page_button(self, page):
        """Finds the pagination button for the specified page."""
        try:
            self.random_sleep(1, 2)  # Random wait
            self.pagination = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, f'//a[@data-page="{page}"]'))
            )
            print(f"Entering page {page}")
            return True
        except (NoSuchElementException, TimeoutException) as e:
            self.handle_exceptions(e, f'Error: Page {page} button not found or timeout. Ending loop.', self.request)
            return False

    def go_to_next_page(self, page):
        """Navigates to the next page."""
        try:
            # Wait for and find the pagination button for the current page
            self.pagination = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, f'//a[@data-page="{page}"]'))
            )
            self.random_sleep(1, 2)
            self.pagination.send_keys(Keys.ENTER)
            print(f"Leaving page {page}")
            return True
        except (
                NoSuchElementException, TimeoutException,
                StaleElementReferenceException, ElementNotInteractableException
        ) as e:
            self.handle_exceptions(e, f"Error navigating to page {page}. Stopping.", self.request)
            return False

    def quit(self):
        """Quits the WebDriver."""
        self.driver.quit()
