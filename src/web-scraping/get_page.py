import requests
import logging

logging.basicConfig(
    format= "%(asctime)s [%(levelname)s] \
				%(funcName)s: %(message)s",
    level=logging.DEBUG,
)
logger = logging.getLogger()


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
    page = get_page(url)
    print(page.content)