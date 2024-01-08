import yaml
import csv
import requests
import logging
import tempfile
import warnings
from pathlib import Path

from bs4 import BeautifulSoup

warnings.filterwarnings("ignore")

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


def extract_info(page: str, csv_writer: object):
    """Extracts and returns the desired information only"""
    # define soup object
    soup = BeautifulSoup(page, "html.parser")
    # get page title
    logger.info(f"Page title: {soup.title}")
    # get the content of the page
    content = soup.select(".elementor-widget-container p")
    # recontruct the content
    content_n = ""
    for i, p in enumerate(content):
        # check if the content of the p tag selected is between the second and
        # third to the last. This is because the first and last two values are 
        # redundant values that do not include the hymns we want 
        if (i > 0) and (i < len(content) - 2):
            content_n += f"{p} "
    # print(f"Page content {content_n} \n\n")

    # save the content to a csv file
    csv_writer.writerow([soup.title, content_n])
    # get links to new pages to crawl also
    next_link = soup.select(".elementor-post-navigation__next.elementor-post-navigation__link a")[0].get("href")
    prev_link = soup.select(".elementor-post-navigation__prev.elementor-post-navigation__link a")[0].get("href")
    logger.info(f"The new links to crawl {next_link, prev_link}")
    return [prev_link, next_link]


def create_csv(file_address: str):
    """Create a csv file to save the hymns content into"""
    file = open(file_address, "w+")
    csv_writer = csv.writer(file)
    logger.info("File and csv_writer created successfully")
    return file, csv_writer


def update_list(returned_links: list, parsed_pages: list, unparsed_pages: list):
    """
    Update the different lists by removing parsed page from the unparsed_pages list 
    and adding the new returned list to unparsed_pages list given that they have not 
    been parsed before 
    """
    # add the first link on the unparsed_pages to the list of parsed_pages
    parsed_pages.append(unparsed_pages[0])
    # delete the link from unparsed_pages list
    del unparsed_pages[0]
    # for the links in the returned_list, check if they've not been parsed before
    for link in returned_links:
        if link not in parsed_pages:
            # if they haven't, add to unparsed_list
            unparsed_pages.append(link)
    logger.info(f"Lists modified respectively... \n parsed_pages: {parsed_pages}, \nunparsed_pages: {unparsed_pages}")
    return parsed_pages, unparsed_pages


def main():
    parsed_pages, unparsed_pages = [], []
    unparsed_pages.append(configurations["url"])
    file, csv_writer = create_csv(configurations["hymn_file"])
    while unparsed_pages != []:
        page = get_page(unparsed_pages[0])
        # file = save_file(page.text)
        returned_links = extract_info(page.content, csv_writer)
        parsed_pages, unparsed_pages = update_list(
                                            returned_links, 
                                            parsed_pages, 
                                            unparsed_pages
                                            )
    file.close()


if __name__ == "__main__":
    main()