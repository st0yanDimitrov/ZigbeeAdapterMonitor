from z2m_log_parser import z2m_log_parser as parser
import RPi.GPIO as gpio
import time
import json

import z2m_log_parser.z2m_log_parser

class Config():
    def __init__(self):
        self.log_path = str
        self.search_string = str
        self.gpio_output_number = int

def get_config(config_file_path):
    config = Config()
    with open(config_file_path, 'r') as config_file:
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

def main():
    config = get_config("./config.json")
    log_entries = parser.parse_latest_logs(config.log_path)
    log_entries = [x for x in log_entries if config.search_string in x.data.message]
    if any(log_entries):
        reset_adapter(config.gpio_output_number)
    time.sleep(10)

if __name__ == "__main__":
    main()