"""Running the Xetra ETL Application"""

import logging
import logging.config

import yaml


def main():
    """Entry point to run the xetra ETL Job
    """
    # Parsing the Yaml file 
    config_path = '/Users/ronoved/Desktop/ETL_Python_AWS_ccourse/2_repo_github/xetra_1234/configs/xetra_report1_config.yml'
    config = yaml.safe_load(open(config_path))
    # Configure our Logging
    log_config = config['logging']
    logging.config.dictConfig(log_config)
    logger = logging.getLogger(__name__)
    logger.info('this is a test.')


if __name__ == '__main__':
    main()
