hatLED
======
RGB LED HAT

SOURCE: [https://www.waveshare.com/wiki/RGB_LED_HAT](https://www.waveshare.com/wiki/RGB_LED_HAT) 

https://github.com/jgarff/rpi_ws281x
``
sudo apt-get install build-essential python-dev scons swig
``
````
git clone https://github.com/jgarff/rpi_ws281x.git
cd rpi_ws281x
sudo scons
sudo ./test
````
````
cd python 
sudo python setup.py install
````

IF | BAD | ZIP
--- | --- | ---
*ERRO* | `wget` | **https://pypi.python.org/packages/source/s/setuptools/setuptools-5.7.zip**

````
python ./setup.py build
sudo python ./setup.py install
````
````
cd examples
sudo python lowlevel.py
````
##### config.txt
```
hdmi_force_hotplug=1
hdmi_force_edid_audio=1
```
Demo
----
```
cd RGB_LED_HAT
sudo python ws2812.py
```

Demo Web
--------
````
sudoapt-get install python-bottle
cd ~/RGB LED HAT/web-RGB
sudo python main
````
> http://raspberrypi.local:8000
      
