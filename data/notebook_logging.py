import os
from IPython.display import display, HTML
import logging
from datetime import datetime
import os

# Define the target directory for logs
target_directory = './data'

# Define the full path for the logs directory
logs_directory = os.path.join(target_directory, 'logs')

# Check if the current working directory is the target directory
if os.getcwd().endswith('/data'):
    # Check if the 'logs' directory exists
    if not os.path.exists(logs_directory):
        # Create the 'logs' directory if it does not exist
        os.makedirs(logs_directory)
        print(f"'logs' directory created in {target_directory}")
    else:
        # If 'logs' directory already exists, simply pass
        print("'logs' directory already exists.")
else:
    # If the current working directory is not 'data', navigate to 'data' and create 'logs'
    os.chdir(target_directory)  # Change to the target directory
    if not os.path.exists(logs_directory):
        os.makedirs(logs_directory)
        print(f"'logs' directory created in {target_directory}")
    else:
        print("'logs' directory already exists in the specified path.")


class HtmlFormatter(logging.Formatter):
    """Logging Formatter to add colors in HTML format for Jupyter Notebooks."""
    formats = {
        logging.DEBUG: "<div style='color: green; font-weight: bold; font-size: 16px;'>{}</div>",
        logging.INFO: "<div style='color: black'>{}</div>",
        logging.WARNING: "<div style='color: orange'>{}</div>",
        logging.ERROR: "<div style='color: red; font-weight: bold; font-size: 16px;'>{}</div>",
        logging.CRITICAL: "<div style='color: red; font-weight: bold;'>{}</div>",
    }

    def format(self, record):
        log_fmt = self.formats.get(record.levelno)
        formatter = logging.Formatter(log_fmt.format('%(asctime)s:%(levelname)s:%(message)s'))
        return formatter.format(record)

class JupyterHtmlHandler(logging.Handler):
    def emit(self, record):
        msg = self.format(record)
        display(HTML(msg))



def setup_logging():
    # Create a logger object
    logger = logging.getLogger('MyLogger')
    logger.setLevel(logging.DEBUG)  # Set the logger to capture all levels of logs

    # Log message format
    log_format = '%(asctime)s:%(levelname)s:%(message)s'

    # Create a stream handler for console output
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)  # Set level to INFO for console output
    stream_formatter = logging.Formatter(log_format)
    stream_handler.setFormatter(stream_formatter)
    logger.addHandler(stream_handler)

    # Create a file handler for output to a file
    if os.path.exists('./logs'):
        pass
    else:
        os.mkdir('./logs')
    file_handler = logging.FileHandler(f'./logs/application_{__name__}_{datetime.now().strftime("%Y%m%d%H%M%S")}.log')
    file_handler.setLevel(logging.DEBUG)  # Set level to DEBUG for file output
    file_formatter = logging.Formatter(log_format)
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)

    return logger