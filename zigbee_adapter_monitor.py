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
        self.execution_path: str = os.path.dirname(os.path.realpath(__file__))
        self.logger: logging.Logger = self.__setup_logging("")
        self.config: Config = self.__get_config("config.json")

    def __setup_logging(sel, logger_name:str) -> logging.Logger:
        execution_path = os.path.dirname(os.path.realpath(__file__))
        logging.basicConfig(filename=execution_path + "/log.txt",
                        filemode='a',
                        encoding="UTF-8",
                        format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                        datefmt='%H:%M:%S',
                        level=logging.DEBUG)
        return logging.getLogger(logger_name)

    def __configure_gpio_output(self, gpio_output_number: int):
        gpio.setmode(gpio.BCM)
        gpio.setup(gpio_output_number, gpio.OUT)

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
        gpio.output(self.config.gpio_output_number, gpio.LOW)
        time.sleep(2)
        gpio.output(self.config.gpio_output_number, gpio.HIGH)
        time.sleep(2)

    def check_if_string_in_log(self) -> bool:
        parser = z2m_log_parser.Z2mLogParser(self.execution_path)
        log_entries = parser.parse_latest_logs(self.config.log_path)
        log_entries = [x for x in log_entries if self.config.search_string in x.data.message]
        if any(log_entries):
            return True
        else:
            return False


def main():
    monitor = ZigbeeAdapterMonitor()
    monitor.__log_info("Execution started.")
    
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