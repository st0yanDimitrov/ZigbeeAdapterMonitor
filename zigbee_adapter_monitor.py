from z2m_log_parser import z2m_log_parser
import RPi.GPIO as gpio
import time
import json
import logging
import os


class Config():
    def __init__(self):
        self.log_path = str
        self.search_string = str
        self.gpio_output_number = int

def setup_logging(logger_name = str):
    execution_path = os.path.dirname(os.path.realpath(__file__))
    logging.basicConfig(filename=execution_path + "/log.txt",
                    filemode='a',
                    encoding="UTF-8",
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.DEBUG)
    return logging.getLogger(logger_name)

def get_config(config_file_name):
    config = Config()
    execution_path = os.path.dirname(os.path.realpath(__file__))
    with open(execution_path+"/"+config_file_name, 'r') as config_file:
        config_json = json.load(config_file)
        config.log_path = config_json["log_path"]
        config.search_string = config_json["search_string"]
        config.gpio_output_number = config_json["gpio_output_number"]
    return config

def configure_gpio_output(gpio_output_number = int):
    gpio.setmode(gpio.BCM)
    gpio.setup(gpio_output_number, gpio.OUT)

def reset_adapter(gpio_output_number = int):
    configure_gpio_output(gpio_output_number)
    gpio.output(gpio_output_number, gpio.LOW)
    time.sleep(2)
    gpio.output(gpio_output_number, gpio.HIGH)
    time.sleep(2)

def main():
    logger = setup_logging("")
    logger.info("Execution started.")
    config = get_config("config.json")
    execution_path = os.path.dirname(os.path.realpath(__file__))
    parser = z2m_log_parser.Z2mLogParser(execution_path)
    log_entries = parser.parse_latest_logs(config.log_path)
    log_entries = [x for x in log_entries if config.search_string in x.data.message]
    if any(log_entries):
        logger.warning("Search string found in logs. Powering off the adapter.")
        reset_adapter(config.gpio_output_number)
        logger.info("Power to the adapter restored.")
    else:
        logger.info("Search string not found in logs.")
    time.sleep(2)
    logger.info("Execution ended.")

if __name__ == "__main__":
    main()