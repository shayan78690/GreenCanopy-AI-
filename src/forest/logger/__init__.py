# import logging  # to tracking error info warning
# import os # to interact with file system
# from from_root import from_root # to get the root directory of the project, allows create absolute paths
# from datetime import datetime # to get the current date and time


# LOG_FILE = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log" # set the log file name with current date and time
# logs_path = os.path.join(from_root(), "logs", LOG_FILE) # create a logs directory in the root of the project and set the log file name
# # it will take the current root and create a folder called logs with the log file name

# os.makedirs(logs_path, exist_ok=True) # create the logs directory if it does not exist

# LOG_FILE_PATH = os.path.join(logs_path, LOG_FILE) # set the full path for the log file

# logging.basicConfig(
#     file_name=LOG_FILE_PATH, # set the log file path
#     format="[ %(asctime)s ] %(name)s - %(levelname)s - %(message)s ", # set the log format
#     level=logging.DEBUG,  # set the logging level to DEBUG
# )

# # s is a string formatting method that allows to format the log messages
# # it is a placeholders that python logging module uses to format the log messages



import logging
import os

from from_root import from_root
from datetime import datetime

LOG_FILE = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"
logs_path = os.path.join(from_root(), "logs", LOG_FILE)

os.makedirs(logs_path, exist_ok=True)

LOG_FILE_PATH = os.path.join(logs_path, LOG_FILE)

logging.basicConfig(
    filename=LOG_FILE_PATH,
    format="[ %(asctime)s ] %(name)s - %(levelname)s - %(message)s",
    level=logging.DEBUG,
)