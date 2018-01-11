# KV-pifacecad

My personal collection of essential pifacecad scripts
Please follow install http://pifacecad.readthedocs.org/en/latest/index.html
Don't forget to turn on SPI via raspi-config.

* Modified sysinfo
* Shutdown message
* Sysinfo Advanced

<h3>sysinfo</h3>
Clone from https://github.com/piface/pifacecad/blob/master/examples/sysinfo.py
Removed prefix 'IP:' from first line, to guarantee that full IP address is visible.

Install by editing (sudo) /etc/init.d/pifacecadsysinfo with the correct path to SYSINFO_FILE
```
sudo update-rc.d pifacecadsysinfo defaults
```

<h3>ShutdownMessage</h3>
Displays logo + text on shutdown complete to indicate it's safe to remove power.
From http://swindon.hackspace.org.uk/blog/piface-shutdown-message/

Install by : 
*Make sure the path to SCRIPT_FILE is correct in pifacecadshutdown*
```
sudo cp etc/pifacecadshutdown /etc/init.d/
sudo chmod +x /etc/init.d/pifacecadshutdown
sudo update-rc.d pifacecadshutdown defaults
```

Jessie alternative : 
*Make sure the path to SCRIPT_FILE is correct in ShutdownMessage.service*
```
sudo cp etc/ShutdownMessage.service /etc/systemd/system
sudo chmod +x /etc/systemd/system/ShutdownMessage.service
sudo systemctl enable ShutdownMessage.service
```

NOTE : Raspbian Jessie can use both methods, the first seems to schedule the script slightly later.  For troubleshooting, see etc/Jessie.md in this repo.

<h3>sysinfo adv(anced)</h3>
Builds from the modified sysinfo.
- Shutdown prepare by pressing the toggle switch (5)
- Shutdown confirm by toggle switch press (5)or to right (7)
- Shutdown abort by any other button or display time-out
- Toggle display + backlight ON / OFF by right button (4)
- Show sysinfo by left button (0)
- Uses vars for time-out settings
- Returns to 2 default display lines, via vars
- On exit : says bye with name from name.txt

(DEBUG : also displays button number when pressed.)

Install by : as above OR
*Make sure the path to SCRIPT_FILE is correct in pifacecadsysinfoadv*
```
sudo cp etc/pifacecadsysinfoadv /etc/init.d/pifacecadsysinfoadv
sudo chmod +x /etc/init.d/pifacecadsysinfoadv
sudo update-rc.d pifacecadsysinfoadv defaults
```
