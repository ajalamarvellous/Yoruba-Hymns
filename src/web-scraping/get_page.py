import yaml
import csv
import requests
import logging
import tempfile
from pathlib import Path

from bs4 import BeautifulSoup

logging.basicConfig(
    format= "%(asctime)s [%(levelname)s] \
				%(funcName)s: %(message)s",
    level=logging.DEBUG,
)
logger = logging.getLogger()

# get configurations from config.yml
config_file_path = Path(__file__).parents[2]/ "config.yml"
with open(config_file_path) as config_file:
    configurations = yaml.safe_load(config_file)

def get_page(url: str):
    """Gets the url page requested for"""
    page = ""
    try:
        page = requests.get(url, verify=False)
        logger.info(f"{url} retreived successfully")
    except requests.ConnectionError as err:
        logger.error(f"A connection Error occured: {err}")
    except requests.HTTPError as err:
        logger.error(f"An HTTP error occured: {err}")
    except requests.Timeout:
        logger.error(f"Connection timed out")
    except requests.RequestException as err:
        logger.error(f"An unknown error occured: {err}")
    return page


def save_file(web_page: str):
    """Create a temp file to save the content retrieved from the internet"""

    file = tempfile.NamedTemporaryFile("w+", delete=False)
    file.write(web_page)
    file.seek(0)
    logger.info(f"page saved as temporary file to {file.name}")
    return file


def extract_info(page: str):
    """Extracts and returns the desired information only"""
    # define soup object
    soup = BeautifulSoup(page, "html.parser")
    # get page title
    print(f"Page title: {soup.title}")
    # get the content of the page
    content = soup.select(".elementor-widget-container p")
    print(f"Page content {content} \n\n")
    # get links to new pages to crawl also
    next_link = soup.select(".elementor-post-navigation__next.elementor-post-navigation__link a")
    prev_link = soup.select(".elementor-post-navigation__prev.elementor-post-navigation__link a")[0]["href"]
    print(f"The new links to crawl {next_link[0].get("href"), prev_link}")


def create_csv(file_address: str):
    """Create a csv file to save the hymns content into"""
    file = open(file_address, "w+")
    csv_writer = csv.writer(file)
    return file, csv_writer


if __name__ == "__main__":
    page = get_page(configurations["url"])
    file = save_file(page.text)
    extract_info(page.content)
    print(file.name)