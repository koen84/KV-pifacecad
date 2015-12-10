### INSALL
# "copy file into homedir"
# sudo cp /etc/init.d/pifacecadsysinfo /etc/init.d/pifacecadsysinfoadv
# sudo nano /etc/init.d/pifacecadsysinfoadv		## correct SYSINFO_FILE path
# sudo update-rc.d pifacecadsysinfoadv defaults

### button functions
# 0 (left) :		show sysinfo
# 1 (2nd left) :	
# 2 (middle) :		
# 3 (2nd right) :
# 4 (right) :		toggle display

# 5 (top press) :	shutdown initiate and shutdown confirm
# 6 (top left) :	(shutdown abort - any not confirm button)
# 7 (top right) :	shutdown confirm


## libraries
import pifacecad
import sys
import subprocess
from time import sleep
import atexit


## CMD / VAR
SHUTDOWN_MSG = 'sudo shutdown -h now "System halted by GPIO action"'
READ_NAME = "cat name.txt"
DDISPLAY1_MSG = "Koen backup sys"
DDISPLAY2_MSG = "You pressed: "

#BACKLIGHT = False
INFO_TIME = 2
DISPLAY_TIME = 2
OFF_TIME = 10


## interact via shell

def input_cmd(cmd):
	return subprocess.check_output(cmd, shell=True).decode('utf-8')
	
def output_cmd(cmd):
	return subprocess.call(cmd, shell=True)

## button handler
def button_press(event):

	global SHUTDOWN
	global BACKLIGHT
	global IS_RUNNING
	IS_RUNNING = 0
	
	# handle display + state var
	cad.lcd.display_on()
	cad.lcd.backlight_on()
	if event.pin_num != 4:
		BACKLIGHT = True	## because else pin 4 disfunctional

	# re-init display (when erased by shutdown)
	if (SHUTDOWN):
		SHUTDOWN = 0
		display_default()

		# confirm shutdown
		if event.pin_num == 7 or event.pin_num == 5 :
			cmd_shutdown()
			return

		# abort shutdown + end IS_RUNNING
		else:
			cad.lcd.home()
			cad.lcd.write("Shutdown aborted")
			sleep(INFO_TIME)
			display_default()

	# display pin number
	cad.lcd.set_cursor(13,1)
	cad.lcd.write(str(event.pin_num))

	# initiate shutdown
	if event.pin_num == 5 :
		IS_RUNNING = True
		cad.lcd.clear()

		SHUTDOWN = 1
		cad.lcd.write("Left: abort")
		cad.lcd.set_cursor(0, 1)
		cad.lcd.write("Right: shutdown")

	# backlight toggle
	if event.pin_num == 4 :
		if BACKLIGHT:
			cad.lcd.backlight_off()
			BACKLIGHT = False
			cad.lcd.display_off()
		else:
			cad.lcd.display_on()
			cad.lcd.backlight_on()
			BACKLIGHT = True
		
		# keep the status for at least INFO_TIME
		sleep(INFO_TIME)
	
	# sysinfo
	# backlight toggle
	if event.pin_num == 0 :
		show_sysinfo()

# shutdown function
def cmd_shutdown():
	cad.lcd.home()
	cad.lcd.write("Shutting down...")
	#sleep(1)
	output_cmd(SHUTDOWN_MSG)

# default-display-text function
def display_default(DISPLAY_ON=True):
	global BACKLIGHT
	cad.lcd.clear()
	cad.lcd.write(DDISPLAY1_MSG)
	cad.lcd.set_cursor(0, 1)
	cad.lcd.write(DDISPLAY2_MSG)
	
	if DISPLAY_ON:
		cad.lcd.display_on()
		cad.lcd.backlight_on()
		BACKLIGHT = True
		sleep(DISPLAY_TIME)
		cad.lcd.backlight_off()
		BACKLIGHT = False

# button-listener-init function
def start_routine():
	global listener
	listener = pifacecad.SwitchEventListener(chip=cad)

	for i in range(8):
		listener.register(i, pifacecad.IODIR_FALLING_EDGE, button_press)

	listener.activate()

# DEBUG function
def stop_routine():
	listener.deactivate()

	NAME = input_cmd(READ_NAME)
	cad.lcd.clear()
	cad.lcd.write("Bye {}" . format(NAME))
	output_cmd('echo "Bye {}"' . format(NAME))


# CTRL+C
atexit.register(stop_routine)


## sysinfo - CMD / VAR
#UPDATE_INTERVAL = 60 * 5  # 5 mins
GET_IP_CMD = "hostname --all-ip-addresses"
GET_TEMP_CMD = "/opt/vc/bin/vcgencmd measure_temp"
TOTAL_MEM_CMD = "free | grep 'Mem' | awk '{print $2}'"
USED_MEM_CMD = "free | grep '\-\/+' | awk '{print $3}'"

## sysinfo - custom symbols
temperature_symbol = pifacecad.LCDBitmap(
	[0x4, 0x4, 0x4, 0x4, 0xe, 0xe, 0xe, 0x0])
memory_symbol = pifacecad.LCDBitmap(
	[0xe, 0x1f, 0xe, 0x1f, 0xe, 0x1f, 0xe, 0x0])
temp_symbol_index, memory_symbol_index = 0, 1

## sysinfo functions

def sysinfo_get_ip():
	return input_cmd(GET_IP_CMD)[:-1]

def sysinfo_get_temp():
	return input_cmd(GET_TEMP_CMD)[5:9]

def sysinfo_get_free_mem():
	total_mem = float(input_cmd(TOTAL_MEM_CMD))
	used_mem = float(input_cmd(USED_MEM_CMD))
	mem_perc = used_mem / total_mem
	return "{:.1%}".format(mem_perc)

def sysinfo_wait_ip():
	ip = ""
	while len(ip) <= 0:
		ip = sysinfo_get_ip()
		sleep(1)

def show_sysinfo():
	global BACKLIGHT
	global IS_RUNNING
	IS_RUNNING = 0
	# init
	cad.lcd.store_custom_bitmap(temp_symbol_index, temperature_symbol)
	cad.lcd.store_custom_bitmap(memory_symbol_index, memory_symbol)
	cad.lcd.clear()
	cad.lcd.display_on()
	cad.lcd.backlight_on()
	BACKLIGHT = True
	cad.lcd.write("Waiting for IP..")
	sysinfo_wait_ip()
	#show_sysinfo()
	
	# display + update		## TODO : break while ?
	#while True:
	cad.lcd.clear()
	cad.lcd.write("{}\n".format(sysinfo_get_ip()))

	cad.lcd.write_custom_bitmap(temp_symbol_index)
	cad.lcd.write(":{}C ".format(sysinfo_get_temp()))

	cad.lcd.write_custom_bitmap(memory_symbol_index)
	cad.lcd.write(":{}".format(sysinfo_get_free_mem()))
	#sleep(UPDATE_INTERVAL)
	sleep(INFO_TIME)
	display_default()


### MAIN function

if __name__ == "__main__":
	cad = pifacecad.PiFaceCAD()
	cad.lcd.blink_off()
	cad.lcd.cursor_off()

	if "clear" in sys.argv:
		cad.lcd.clear()
		cad.lcd.display_off()
		cad.lcd.backlight_off()
		BACKLIGHT = False
		
	else:
		cad.lcd.backlight_on()
		
		# init vars
		BACKLIGHT = True
		IS_RUNNING = 0
		SHUTDOWN = 0

		# init functions
		display_default()	# write identification on display		
		start_routine()		# button listeners
		
		# keep running
		while True:
			sleep(1)
			IS_RUNNING += 1
			if IS_RUNNING > OFF_TIME:
				IS_RUNNING = 0
				
				if SHUTDOWN:
					SHUTDOWN = 0	# abort shutdown before display off
					display_default(False)	# reset text, but don't display now
					
				cad.lcd.backlight_off()
				BACKLIGHT = False
				cad.lcd.display_off()
		
		# DEBUG function
		#sleep(10)
		stop_routine()
