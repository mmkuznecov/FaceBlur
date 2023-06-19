import yaml
import logging


def read_config(config_path):
    # Initialize a logger
    logger = logging.getLogger(__name__)

    # Set the level of logger
    logger.setLevel(logging.DEBUG)

    # Create a file handler
    handler = logging.FileHandler('logfile.log')
    handler.setLevel(logging.DEBUG)

    # Create a logging format
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)

    # Add the handlers to the logger
    logger.addHandler(handler)

    try:
        with open(config_path, 'r') as stream:
            config = yaml.safe_load(stream)
    except yaml.YAMLError:
        logger.exception("Error loading YAML file")
        config = None  # Return None if an exception is caught

    return config
