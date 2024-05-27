from z2m_log_parser import z2m_log_parser
import RPi.GPIO as gpio
import time
import json
import logging
import os


class Config():
    def __init__(self):
        self.log_path: str = str
        self.search_string: str = str
        self.gpio_output_number: int = int


class ZigbeeAdapterMonitor:

    def __init__(self):
        self.execution_path = os.path.dirname(os.path.realpath(__file__))
        self.logger = self.setup_logging("")

    def setup_logging(sel, logger_name:str) -> logging.Logger:
        execution_path = os.path.dirname(os.path.realpath(__file__))
        logging.basicConfig(filename=execution_path + "/log.txt",
                        filemode='a',
                        encoding="UTF-8",
                        format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                        datefmt='%H:%M:%S',
                        level=logging.DEBUG)
        return logging.getLogger(logger_name)
    
    def log_info(self, message: str):
        self.logger.info(message)

    def log_warning(self, message: str):
        self.logger.warn(message)
    
    def log_error(self, message: str):
        self.logger.error(message)

    def get_config(self, config_file_name: str) -> Config:
        config = Config()
        execution_path = os.path.dirname(os.path.realpath(__file__))
        with open(execution_path+"/"+config_file_name, 'r') as config_file:
            config_json = json.load(config_file)
            config.log_path = config_json["log_path"]
            config.search_string = config_json["search_string"]
            config.gpio_output_number = config_json["gpio_output_number"]
        return config

    def configure_gpio_output(self, gpio_output_number: int):
        gpio.setmode(gpio.BCM)
        gpio.setup(gpio_output_number, gpio.OUT)

    def reset_adapter(self, gpio_output_number: int):
        self.configure_gpio_output(gpio_output_number)
        gpio.output(gpio_output_number, gpio.LOW)
        time.sleep(2)
        gpio.output(gpio_output_number, gpio.HIGH)
        time.sleep(2)

def main():
    monitor = ZigbeeAdapterMonitor()
    monitor.log_info("Execution started.")
    config = monitor.get_config("config.json")
    execution_path = os.path.dirname(os.path.realpath(__file__))
    parser = z2m_log_parser.Z2mLogParser(execution_path)
    log_entries = parser.parse_latest_logs(config.log_path)
    log_entries = [x for x in log_entries if config.search_string in x.data.message]
    if any(log_entries):
        monitor.log_warning("Search string found in logs. Powering off the adapter.")
        monitor.reset_adapter(config.gpio_output_number)
        monitor.log_info("Power to the adapter restored.")
    else:
        monitor.log_info("Search string not found in logs.")
    time.sleep(2)
    monitor.log_info("Execution ended.")

if __name__ == "__main__":
    main()