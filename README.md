# OrangePiZeroMFRC522
RFID-MFRC522 module on Orangepi Zero running **Armbian 5.27** Ubuntu Xenial.
  
<img src="gitImgs/644.jpg" alt="modulePinout" width="417" height="320"><img src="gitImgs/833.jpg" alt="modulePinout" width="417" height="320">

When trying to get an RFID module to work with Orangepi Zero, there was alot of mixed information across forums and instructions. Some directions didn't even specify board model, only referencing **OrangePi** but supplying GPIO pins.  
  
Additionally, at the time of this repo's creation, all tutorials found use some hodgepodge mix match of other GPIO (RPI.GPIO/PyA20.GPIO) libraries that require editing MFRC522's source code, etc... Anyways, this is an attempt to collect all that information, simplify it, correct it and document it in one place.

## Build Materials
  * **Module**: MFRC522 aka RFID-RC522 module [|Buy|](https://www.aliexpress.com/item/RC522-Card-Read-Antenna-RFID-Reader-IC-Card-Proximity-Module/1859133832.html?spm=2114.13010608.0.0.sZMQVW) 
  * **Board**: Orangepi Zero v1.4 [|Buy|](https://www.aliexpress.com/item/New-Orange-Pi-Zero-H2-Quad-Core-Open-source-512MB-development-board-beyond-Raspberry-Pi/32761500374.html?spm=2114.13010608.0.0.sZMQVW)
  * **Kernel**: Armbian 5.27 3.4.113-sun8i Ubuntu Xenial 16.04 [|Download|](https://www.armbian.com/orange-pi-zero/)
  
## Requirements
  * **GPIO Library for Orangepi Zero**: https://github.com/rm-hull/OPi.GPIO
  * **SPI Library**: https://github.com/lthiery/SPI-Py.git

Included in this repo is a modified clone of the above MFRC522 repo. The appropriate lines have been editted to work with Orangepi Zero. This includes replacing **line 1** `import RPI.GPIO as GPIO` with `import OPi.GPIO as GPIO` in all scripts and changing **Line 110** (in **MFRC522.py**) from `spidev0.0` to `spidev1.0`. 

## Pinout
This is the proper way to connect MFRC522 module to Orangepi Zero board via SPI. First column lists pin names as seen on module, verbatim. Second is the Orangepi Zero's literal pin number. Third column is the OPiZero's pin function as seen from a data sheet. Third column is especially useful when trying to match up modules pin titles to schematic of a different board.  
  
Both pin numbers and functions listed below are useful depending on reference material and if trying to determine proper pinout for a SPI/I2C module on a different board model. 

| MFRC522  | OPi Zero Pin Number  |     Pin Function   |
|:--------:|:-------------------:|:------------------:|
| SDA      | Pin 24 <strike>3</strike> | SPI1_CS/PA13       |
| SCK      | Pin 23 <strike>4</strike> | SPI1CLK/PA14       |
| RST      | Pin 22 <strike>5</strike> | UART2_RTS/PA02     |
| MISO     | Pin 21 <strike>6</strike> | SPI1_MISO/PA16     |
| MOSI     | Pin 19 <strike>8</strike> | SPI1_MOSI/PA15     |
| GND      | Pin 6 <strike>21</strike>| GND                |
| 3.3v     | Pin 1 <strike>26</strike>| 3.3v               |
-------------------------------------------------------
* The coordinantes that have been struck were based on [this](http://auseparts.com.au/image/cache/catalog/OrangePi/Orange-Pi-Zero-Pinout-banner2-700x700.jpg) popular, but misleading picture. 
<img src="gitImgs/821.jpg" alt="modulePinout">

## SPI interface activation

You can enable interface thru *armbian-config* or edit *armbianEnv.txt* file:

```sh 
sudo nano /boot/armbianEnv.txt
```

`overlays` string should contain `spi-spidev` and `spi-add-cs1`. If these values are not in the `overlays`, just add them separated by spaces.

You must also add the following lines:

```
param_spidev_spi_bus=1

param_spidev_spi_cs=0
```

As a result, you should get a file with the following contents (added lines are highlighted in yellow):

<img src="gitImgs/armbiarEnv.PNG" alt="armbianEnv" width="450" height="300" title="/boot/armbianEnv.txt">

Save and reboot your OrangePi.

Check that SPI is present:

```
ls /dev | grep spi
```
<img src="gitImgs/spi_check.png" alt="SPI check" width="400" height="44" title="SPI check">


## Installation

`git clone https://github.com/BiTinerary/OrangePiZeroMFRC522.git && bash ./OrangePiZeroMFRC522/getAllTheStuff.sh`

or the long manual way...

```sh
apt-get install python-dev -y
apt-get install python-pip -y
pip install --upgrade pip
pip install setuptools

git clone https://github.com/rm-hull/OPi.GPIO.git
cd OPi.GPIO
pip install .

cd ..
git clone https://github.com/lthiery/SPI-Py.git
cd SPI-Py
pip install .

cd ..
git clone https://github.com/BiTinerary/OrangePiZeroMFRC522.git
python ./OrangePiZeroMFRC522/MFRC522-python/Read.py
```

## Customizations

Swipe RFID chip >> Run command/script associated with that RFID tag. A hardware spin off of https://github.com/BiTinerary/PersonalAPI

[triggerRead.py](https://github.com/BiTinerary/OrangePiZeroMFRC522/blob/master/triggerRead.py) is the same source as original **Read.py** with a few modifications, mainly in the middle. Print statements were removed throughout the source files (dump/read/MFRC/Write) just to clean up the output. I added a **hashFile.txt** which stores the UID of RFID chips as keys and commands as values. So that effectively when a RFID chip is scanned, a corresponding command is executed. This all happens [line 45-58](https://github.com/BiTinerary/OrangePiZeroMFRC522/blob/master/triggerRead.py#L45-L58)

I'm using a practical version of this repo and the triggerRead.py script mentioned above for a Google Sheet/API punching TimeClock, over here: https://github.com/BiTinerary/TimeClockPi

## References
The main MFRC522 script in this repo is just a modified fork of https://github.com/mxgxw/MFRC522-python  
[RM-Hull](https://github.com/rm-hull) has some other cool repos with more coming down the pipe.
