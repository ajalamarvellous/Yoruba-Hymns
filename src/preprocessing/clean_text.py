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
