# `20180430a` - Pushing further

The aim of this experiment was to automate the acquisition using an arduino to update the piezo motor at each acquisition, set on Poff signal from Matty.

Then there's a bit of file processing to obtain the images.

* [Client side](/matty/20180430a/20180430a-Client.ipynb)
* [Server side](/matty/20180430a/20180430a-Server.ipynb)
  * [Example of the JSON of an acq](/matty/20180430a/wire/p_servo-23.json)
* [Arduino code (for a feather)](/matty/20180430a/ServoControl.ino)
* [PFGA bin](/matty/prog_flash/pMATTYtestRegisterasyn_nomoreadd_20180401.bin)

### File format

I'm improving the file capture format. Now using a JSON for acquired data, as well as keeping a track of all registers when possible. On the client side, improving the reconstruction of the acquisitions.

### Clock playing

Here's the signal I'm sending on matty on the two bits acquired from the TopTurn bits. Here, the piezo is at angle 22, that's a reference of the offset (60) + the position, so I should read 82 in binary. 

And that's what I'm getting, yeay!

![](/matty/20180430a/wire/clock_check_pos82.jpg)


### Wire - with [dataset](/matty/20180430a/wire/dataset.npz)

![](/matty/20180430a/wire/SCImage.jpg)



![](/matty/20180430a/wire/fft.jpg)

![](/matty/20180430a/wire/p_servo-23.json.jpg)


![](/matty/20180430a/image/20180430_181856.jpg)


### PU90 - with [dataset](/matty/20180430a/pu90/dataset.npz)

![](/matty/20180430a/pu90/SCImage.jpg)

![](/matty/20180430a/pu90/fft.jpg)


### PU30 - with [dataset](/matty/20180430a/pu30/dataset.npz)

![](/matty/20180430a/image/20180430_180856.jpg)

![](/matty/20180430a/pu30/SCImage.jpg)

![](/matty/20180430a/pu30/fft.jpg)

