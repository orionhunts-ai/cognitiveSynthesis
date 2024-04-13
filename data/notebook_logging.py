# notebook_logging.py
from IPython.display import display, HTML
import logging

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
        formatter = logging.Formatter(log_fmt.format("%(asctime)s - %(levelname)s - %(message)s"))
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
    file_handler = logging.FileHandler('application.log')
    file_handler.setLevel(logging.DEBUG)  # Set level to DEBUG for file output
    file_formatter = logging.Formatter(log_format)
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)

    return logger