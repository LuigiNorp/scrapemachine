import logging
from progress.models import Posts
from scraper.models import Property
from django.contrib import messages
from django.db import IntegrityError
from selenium.webdriver.common.by import By
from selenium.common import NoSuchElementException
from scraper.selenium.engine.selenium_engine import SeleniumEngine


logger = logging.getLogger(__name__)


class CBCScraper:
    """Class to scrape data from CBC Real Estate website."""
    def __init__(self, url: str, chromedriver_path: str, request, website):
        """Initializes the scraper with base URL, driver path, request for messages, and website instance.

        Args:
            url (str): The base URL of the website to scrape.
            chromedriver_path (str): The path to the chromedriver executable.
            request: The request object for messages.
            website: The Website model instance
        """
        self.base_url = url
        self.engine = SeleniumEngine(chromedriver_path, request)
        self.request = request
        self.page = 1
        self.website = website

    def _extract_data(self):
        """Extracts data from the current page and saves it to the database."""
        try:
            posts = self.engine.driver.find_elements(By.XPATH, '//div[@aria-label="Property"]')
            for post in posts:
                post_content = post.text

                try:
                    # Extract the name of the post
                    _name = post.find_element(By.XPATH, './/h3[@class="cbc1__price cbc1__price-2"]').text.split(" - ")[0]

                    # Verify if post already exists
                    if Posts.objects.filter(post_title=_name, website=self.website).exists():
                        messages.warning(self.request, f"Post '{_name}' already exists. Skipping.")
                        continue

                    # Extract the address of the post
                    address = post.find_element(By.XPATH, './div[2]/div[3]').text
                    _address = f'{_name} {address}'

                    # Extract the price of the post
                    price = post.find_element(By.XPATH, './div[2]/div[2]').text

                    # Extract the URL of the post
                    url = post.find_element(By.XPATH, './a').get_attribute('href')

                    # Save the post content in the database
                    new_post = Posts.objects.create(
                        website=self.website,
                        post_title=_name,
                        post_content=post_content  # Guardamos el contenido completo
                    )

                    # Save in the Property model associated with the post
                    Property.objects.create(
                        post=new_post,
                        property_name=_name,
                        property_price=price,
                        property_address=_address,
                        property_url=url
                    )

                    messages.success(self.request, f"Post '{_name}' and associated Property saved successfully.")

                except NoSuchElementException as e:
                    self.engine.handle_exceptions(
                        e, 'NoSuchElementException: Missing field in this post. Skipping.', self.request)

                except IntegrityError as e:
                    self.engine.handle_exceptions(
                        e, f'IntegrityError: Error saving post. Skipping', self.request)

        except NoSuchElementException as e:
            self.engine.handle_exceptions(
                e, 'NoSuchElementException: No posts found on this page.', self.request)

    def start(self):
        """Starts the scraping process and loops through all available pages."""
        self.engine.driver.get(self.base_url)

        while True:
            # Find and navigate to the next page
            if not self.engine.find_next_page_button(self.page):
                break

            # Extract data from the current page
            self._extract_data()

            # Go to the next page
            if not self.engine.go_to_next_page(self.page):
                break

            self.page += 1

        # Quit the driver when done
        self.engine.quit()
        print("Scraping completed.")
