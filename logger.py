import logging
import os
from config import FILE_PATH

def setup_logger():
    logging.basicConfig(
        filename=os.path.join(FILE_PATH, 'filelist.log'),
        filemode='w',
        format='%(asctime)s %(levelname)-8s %(message)s',
        datefmt='%d.%m %H:%M:%S',
        level=logging.DEBUG
    )
    return logging.getLogger(__name__)
