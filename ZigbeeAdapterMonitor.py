from z2mLogParser import LogParser
import RPi.GPIO as gpio
import time
import json

class Config():
    def __init__(self):
        self.logPath = str
        self.searchString = str
        self.gpioOutputNumber = int

def getConfig(configFilePath):
    config = Config()
    with open(configFilePath, 'r') as configFile:
        configJson = json.load(configFile)
        config.logPath = configJson["logPath"]
        config.searchString = configJson["searchString"]
        config.gpioOutputNumber = configJson["gpioOutputNumber"]
        return config

def configureGpioOutoput(gpioOutputNumber = int):
    gpio.setmode(gpio.BCM)
    gpio.setup(gpioOutputNumber, gpio.OUT)

def resetAdapter(gpioOutputNumber = int):
    configureGpioOutoput(gpioOutputNumber)
    gpio.output(gpioOutputNumber, gpio.LOW)
    time.sleep(2)
    gpio.output(gpioOutputNumber, gpio.HIGH)

def main():
    parser = LogParser()
    config = getConfig("./config.json")
    logsEntries = parser.parseLogs(config.logPath)
    logsEntries = [x for x in logsEntries if config.searchString in x.data.message]
    if any(logsEntries):
        resetAdapter(config.gpioOutputNumber)
    time.sleep(10)

if __name__ == "__main__":
    main()