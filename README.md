# Zigbee adapter monitor for Raspberry Pi

Used to monitor Zigbee2Mqtt log for speciffic message and perform power cycle resed via changing a state of a configured GPIO pin
  
*Setup:*

[Raspberry Pi B] +5V    ->   IN  [DC-DC 5v-3.3v converter] OUT     ->  +3.3V [cc2530 + cc2591 Zigbee adapter]

[Raspberry Pi B] GND    ->   GND [DC-DC 5v-3.3v converter] GND     ->  GND   [cc2530 + cc2591 Zigbee adapter]

[Raspberry Pi B] TXD0   ->   TXD [cc2530 + cc2591 Zigbee adapter]

[Raspberry Pi B] RXD0   ->   RXD [cc2530 + cc2591 Zigbee adapter] 

[Raspberry Pi B] GPIO23 ->   EN  [DC-DC 5v-3.3v converter]

The enable pin of the DC-DC converter is connected to a GPIO pin of the Raspberry Pi

