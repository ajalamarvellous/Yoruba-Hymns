import yaml
import requests
import logging
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

if __name__ == "__main__":
    page = get_page(configurations["url"])
    print(page.content)