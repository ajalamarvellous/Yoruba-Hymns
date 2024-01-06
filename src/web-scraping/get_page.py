import yaml
import requests
import logging
import tempfile
from pathlib import Path

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
    except HTTPError as err:
        logging.error(f"An error occured: {err}")
    return page

def save_file(web_page: str):
    """Create a temp file to save the content retrieved from the internet"""

    file = tempfile.NamedTemporaryFile("w+", delete=False)
    file.write(web_page)
    file.seek(0)
    return file

if __name__ == "__main__":
    page = get_page(configurations["url"])
    file = save_file(page.text)
    print(file.name)