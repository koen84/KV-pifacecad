# KV-pifacecad

My personal collection of essential pifacecad scripts
Please follow install http://pifacecad.readthedocs.org/en/latest/index.html
Don't forget to turn on SPI via raspi-config.

* Modified sysinfo
* Shutdown message

<h3>sysinfo</h3>
Clone from https://github.com/piface/pifacecad/blob/master/examples/sysinfo.py
Removed prefix 'IP:' from first line, to guarantee that full IP address is visible.

Install by editing (sudo) /etc/init.d/pifacecadsysinfo with the correct path to SYSINFO_FILE
sudo update-rc.d pifacecadsysinfo defaults

<h3>ShutdownMessage</h3>
Displays logo + text on shutdown complete to indicate it's safe to remove power.
From http://swindon.hackspace.org.uk/blog/piface-shutdown-message/

Instally by : 
# Make sure the path to SCRIPT_FILE is correct in pifacecadshutdown
sudo cp pifacecadshutdown /etc/init.d/
sudo chmod +x /etc/init.d/pifacecadshutdown
sudo update-rc.d pifacecadshutdown stop 99 0 .
