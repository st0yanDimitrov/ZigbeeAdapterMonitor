# Zigbee adapter monitor for Raspberry Pi

**Setup:**

[Raspberry Pi B+] +5V    ->   IN  [DC-DC 5v-3.3v converter] OUT     ->  +3.3V [cc2530 + cc2591 Zigbee adapter]

[Raspberry Pi B+] GND    ->   GND [DC-DC 5v-3.3v converter] GND     ->  GND   [cc2530 + cc2591 Zigbee adapter]

[Raspberry Pi B+] TXD0   ->   TXD [cc2530 + cc2591 Zigbee adapter]

[Raspberry Pi B+] RXD0   ->   RXD [cc2530 + cc2591 Zigbee adapter] 

[Raspberry Pi B+] GPIO23 ->   EN  [DC-DC 5v-3.3v converter]


**Description**:

The script operates by searching in a contrller applicaion log file for speciffic message indicating that the zigbee adapter is not responsive.
If the message is found, the controlling GPIO pin of the Raspberry Pi disables and enables the power to the adapter via the DC-DC converter.
In result a power cycle reset is performed on the zigbee adapter.

**Configuration:**

The script is configured via the config.json file with the parameters as follows:


log_path [str] - full path to the log file under monitoring

search_string [str] - message under which presence the adapter must be reset

gpio_output_number [int]- number of the Raspberry Pi GPIO pin where the Enable pin of the DC-DC converter is connected


**Note:**

In case voltage conversion is not needed or the used DC-DC converter does not have Enable pin, a MOSFET switch can be used instead to cut the power to the zigbee adapter
