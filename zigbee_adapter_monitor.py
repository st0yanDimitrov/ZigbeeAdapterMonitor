from z2m_log_parser import *
import RPi.GPIO
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

    def __init__(self, logger: logging, gpio: RPi.GPIO):
        self.execution_path: str = os.path.dirname(os.path.realpath(__file__))
        self.logger: logging.Logger = self.__setup_logging("", logger)
        self.config: Config = self.__get_config("config.json")
        self.gpio = gpio

    def __setup_logging(sel, logger_name:str, logger: logging) -> logging.Logger:
        execution_path = os.path.dirname(os.path.realpath(__file__))
        logger.basicConfig(filename=execution_path + "/log.txt",
                        filemode='a',
                        encoding="UTF-8",
                        format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                        datefmt='%H:%M:%S',
                        level=logger.DEBUG)
        return logger.getLogger(logger_name)

    def __configure_gpio_output(self, gpio_output_number: int):
        self.gpio.setmode(self.gpio.BCM)
        self.gpio.setup(gpio_output_number, self.gpio.OUT)

    def __get_config(self, config_file_name: str) -> Config:
        config = Config()
        execution_path = os.path.dirname(os.path.realpath(__file__))
        with open(execution_path+"/"+config_file_name, 'r') as config_file:
            config_json = json.load(config_file)
            config.log_path = config_json["log_path"]
            config.search_string = config_json["search_string"]
            config.gpio_output_number = config_json["gpio_output_number"]
        return config

    def log_info(self, message: str):
        self.logger.info(message)

    def log_warning(self, message: str):
        self.logger.warn(message)
    
    def log_error(self, message: str):
        self.logger.error(message)

    def reset_adapter(self):
        self.__configure_gpio_output(self.config.gpio_output_number)
        self.gpio.output(self.config.gpio_output_number, self.gpio.HIGH)
        time.sleep(2)
        self.gpio.output(self.config.gpio_output_number, self.gpio.LOW)
        time.sleep(2)

    def check_if_string_in_log(self) -> bool:
        parser = Z2mLogParser()
        log_entries = parser.parse_latest_logs(self.config.log_path)
        log_entries = [x for x in log_entries if self.config.search_string in x.data.message]
        if any(log_entries):
            return True
        else:
            return False


def main():
    monitor = ZigbeeAdapterMonitor(logging, RPi.GPIO)
    monitor.log_info("Execution started.")

    if monitor.check_if_string_in_log():
        monitor.log_warning("Search string found in logs. Powering off the adapter.")
        monitor.reset_adapter()
        monitor.log_info("Power to the adapter restored.")
    else:
        monitor.log_info("Search string not found in logs.")
    time.sleep(2)
    monitor.log_info("Execution ended.")

if __name__ == "__main__":
    main()