# Simple battery testing tool

This project aims to build a **complete** and affordable setup for DIY battery testing.

## Features

* Compatible with various battery types
* Battery capacity testing
* Internal resistance measurement
* Nice graphs
* Minimal component count, low cost

## Example test result

![Example test result](/example.png)

## Required parts

* Computer with Python 3
* Arduino Uno
* Constant current load (example schematic included in the hardware directory)

## Usage

* Connect all parts together (load is not applied until the software is started)
* Start the measurement with `python .\desktop\measurebattery.py [COM PORT] [CUTOFF VOLTAGE]`
* Battery will be discharged until it reaches specified voltage or *2.8V* if no voltage was specified
* Enter your battery name in the first line of the resulting file ( `battery_[TIME].txt` )
* Render the graph with `python .\desktop\rendergraph.py [FILE NAME]`

## Accuracy

Measurement accuracy depends heavily on how stable your PC USB voltage is, after calibration you should be able to get around 5% accuracy for capacity.

Accurate measurement of internal resistance requires good battery connection and good PCB design for your constant current load, stock design should be able to measure within 10%.

## Contributing

Contributions are welcome, feel free to submit your own test results or hardware/software improvements.