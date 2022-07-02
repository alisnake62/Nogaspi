import logging
import os

logging.basicConfig(level=logging.ERROR,
    filename=f"{os.environ['DIRECTORY_PROJECT']}app.log",
    filemode="a",
    format='%(asctime)s - %(levelname)s - %(message)s')

