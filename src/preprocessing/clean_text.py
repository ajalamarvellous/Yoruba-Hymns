import logging
import yaml
from pathlib import Path

import pandas as pd


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


def read_file(file_address: str) -> pd.DataFrame:
    """
    Read file and add headers
    """
    df = pd.read_csv(file_address, names=['Title', 'Hymn'])
    logger.info("Dataframe read successfully...")
    return df


def format_title(title: str) -> str:
    """
    Clean and format the title column
    """ 
    word = title.split("-")[0]
    word = word.replace("<title>", "")
    return word


def format_hymn(hymn: str) -> str:
    """
    Format hymn and remove all HTML tags in it
    """
    hymn = hymn.replace("<p>", "")
    hymn = hymn.replace("</p>", "")
    hymn = hymn.replace("<br/>", " ")
    return hymn

def save_file(df: pd.DataFrame, file_destination: str) -> None:
    df.to_csv(file_destination, index=False)
    logger.info(f"File saved successfully to {file_destination}")
    return None


def main():
    df = read_file(configurations["hymn_file"])
    df["Title"] = df["Title"].apply(format_title)
    logger.info("Title formated successfully...")
    df["Hymn"] = df["Hymn"].apply(format_hymn)
    logger.info("Hymn formated successfully...")
    save_file(df, configurations["processed_file"])
    return None

if __name__ == "__main__":
    main()
