# TODOs

## Certif
  * OSH Certification

## Comm
  * Contact Lattice
  * TaZ / Hack'Im Bey

## TOMOD

* Footprints
  * Check clock footprint (quelle raison pour plantage par Macrofab?)
  * Correct HV Module footprint (reversed)
* Simplification
  * Remove i2c components / lines
    * Seul i2c: RPi's line
  * REMOVE U118, U131, U134
* Checks
  * Vérifier U143 et U160 (seemed to bug when using IO4 as CS)
* Headers (2x6 as PMODs, exposing) ( J9 and J19 split ):
  * PMOD 1 (close to SMA)
    * TopTurn 1, 2, 3
    * Out 1, 2, 3
    * Pon
    * Poff
    * 5V, 3.3V and GND
  * PMOD 2 (somewhere else)
    * IO 1 to 4
    * In 1, 2, 3, Trig
    * 5V, 3.3V and GND
* Reorga
  * RPi header reversed + OLED reversed (écran loin)
    * Mounting holes for RPi0
    * Décaler / splitter J10
* Interfaces
  * RESET button for FPGA ? 
  * LED for chip enable on SPI FLASH
    * LED on flash/fpga CS
    * LED on RPi / USB select



## RPI:

PMOD RPI:
* IO1
* IO2
* IO3
* IO4

remains 9 pins, namely 15, 18, 23, 24, 5, 7, 16, 10, 21



## FPGA

PMOD standards:
- https://www.digilentinc.com/Pmods/Digilent-Pmod_%20Interface_Specification.pdf
6x2
  - i2c : The connection standard for system boards that provide I2C connectors is to use a 2x4 male, 100 mil spaced, pin header connector with straight pins
- See p6 of doc for standard maps
- GPIOs: Pmod Interface Type 1 (GPIO) organisation x2 (see Fig2)


### Remodel IN1-3 and OUT1-3 + PonPoff
- Have those onto a 12pin PMOD

### Remains

1 extraPMOD with 4+4 IOs

#### IOL - 6 pins not mapped
3B
5B
GBIN7
23A
23B
24A

#### - 6 pins not mapped

IOB63
IOB64
IOB71
IOB91
IOB95


