import logging
from datetime import date
import yaml
from pathlib import Path

def yaml_var(var : str, filepath : str = "secrets/config.yaml"):
    """
    This function reads the specified variable from the YAML file.

    Args:
        var: The name of the variable to read.
        filepath: The path to the YAML file.

    Returns:
        The value of the specified variable if found, 
        None otherwise.
    """
    try:
        with open(filepath, 'r') as f:
            yaml_data = yaml.safe_load(f)

        def get_yaml_value(data, path):
            """
            Recursively retrieves a value from a nested YAML dictionary.

            Args:
                data: The root YAML dictionary.
                path: A dot-separated string representing the path to the desired value.

            Returns:
                The value at the specified path, or None if the path is invalid.
            """
            if not path:
                return data

            key = path.split(".", 1)[0]
            if key in data:
                remaining_path = path[len(key)+1:] 
                return get_yaml_value(data[key], remaining_path) 
            else:
                return None

        # Replace with the actual filepath
        value = get_yaml_value(yaml_data, var)

        if value:
            return value
        else:
            return None
    except FileNotFoundError:
        exit()
    except yaml.YAMLError as e:
        exit()


def create_logger(name: str,log_level, file_handler_level, file_log_format, stream_log_format, log_file_path, stream_handler_level=None):
    """
    This function creates a logger object.

    args:
        name: The name of the log
        log_level: setting the level of at which logging will happen
        log_format: the format in which log data will be written
        log_file_path: the path where log file will be stored
        stream_handler_level: Optional level for the stream handler (defaults to log_level)

    returns: A log object
    """

    # Create a logger
    logger = logging.getLogger(name)

    # Check if logger has already been configured
    if not logger.hasHandlers():
        # Setting logging level
        logger.setLevel(log_level)

        # File handler
        file_handler = logging.FileHandler(log_file_path)
        # Setting file handler log level
        file_handler.setLevel(file_handler_level)

        # Logfile data format
        formatter = logging.Formatter(file_log_format)

        # Putting the file formatter in filehandler
        file_handler.setFormatter(formatter)

        # Adding the above handler to logger
        logger.addHandler(file_handler)

        # Stream handler (for console output)
        if stream_handler_level is None:
            stream_handler_level = log_level
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(stream_handler_level)
        stream_formatter = logging.Formatter(stream_log_format)
        stream_handler.setFormatter(stream_formatter)
        logger.addHandler(stream_handler)

    return logger



# prd log
log_format_prd = yaml_var(var="log.prd.format")
stream_format = yaml_var(var="log.prd.stream_format")

folder_path = Path(str(yaml_var(var='log.prd.filepath')))


# creating log folder if it doesn't exit
try:
    folder_path.mkdir(parents=True, exist_ok=True) 
except PermissionError:
    raise Exception (f"--- TOOL -- | action : creating folder |  folder path : {folder_path} | error : Permission denied to create folder")
    exit()
except OSError as e:
    raise Exception(f"--- TOOL -- | action : creating folder | status : Failed |  folder path : {folder_path} | error : {e}")
    exit()

today = date.today()
date_string = today.strftime("%d-%m-%Y") 

log_file_path_prd = f"{yaml_var(var='log.prd.filepath')}{date_string}.log"
log = create_logger(name="SQLBOT", 
                    log_level=logging.DEBUG, 
                    file_handler_level=logging.INFO,
                    file_log_format=log_format_prd,
                    stream_log_format=stream_format,
                    log_file_path=log_file_path_prd, 
                    stream_handler_level=logging.DEBUG)
