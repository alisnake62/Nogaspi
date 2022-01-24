import logging

logging.basicConfig(level=logging.ERROR,
    filename="app.log",
    filemode="a",
    format='%(asctime)s - %(levelname)s - %(message)s')

