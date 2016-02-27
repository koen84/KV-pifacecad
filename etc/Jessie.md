## Raspbian Jessie uses systemd, though has compatibility for sysV.
## So we can use both old init scripts as well as systemd unit files.
## Important change : something needs to run on start, to run something on stop.
## In the unit file, that's both "ExecStart=/bin/true" and "RemainAfterExit=yes".
## 		(could've used echo like in the init file)

# sysV - correct

$ sudo service pifacecadshutdown status
● pifacecadshutdown.service - LSB: Displays a shutdown message on the PiFace.
   Loaded: loaded (/etc/init.d/pifacecadshutdown)
   Active: active (exited) since <date + time>; <time> ago
  Process: <pid> ExecStart=/etc/init.d/pifacecadshutdown start (code=exited, status=0/SUCCESS)

<date + time> <hostname> pifacecadshutdown[328]: PiFace CAD shutdown message no action on start
<date + time> <hostname> systemd[1]: Started LSB: Displays a shutdown message on the PiFace..


# sysV - wrong

sudo service pifacecadshutdown status

● pifacecadshutdown.service - LSB: Displays a shutdown message on the PiFace.
   Loaded: loaded (/etc/init.d/pifacecadshutdown)
   Active: inactive (dead)


# systemd - correct

$ sudo systemctl status ShutdownMessage
● ShutdownMessage.service - Display message at shutdown complete on pifacecad
   Loaded: loaded (/etc/systemd/system/ShutdownMessage.service; enabled)
   Active: active (exited) since <date + time>; <time> ago
  Process: <pid> ExecStart=/bin/true (code=exited, status=0/SUCCESS)
 Main PID: <pid> (code=exited, status=0/SUCCESS)
   CGroup: /system.slice/ShutdownMessage.service

<date + time> <hostname> systemd[1]: Started Display message at shutdown complete on pifacecad.


# systemd - wrong

$ sudo systemctl status ShutdownMessage
● ShutdownMessage.service - Display message at shutdown complete on pifacecad
   Loaded: loaded (/etc/systemd/system/ShutdownMessage.service; disabled)
   Active: inactive (dead)
