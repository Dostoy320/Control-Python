import RPi.GPIO as GPIO
import time

# set pin formatting system (vs BOARD)
GPIO.setmode(GPIO.BCM)

#assign names to pins in use
enable_pin = 18
coil_A_1_pin = 4
coil_A_2_pin = 17
coil_B_1_pin = 23
coil_B_2_pin = 24

#set pins to output
GPIO.setup(enable_pin, GPIO.OUT)
GPIO.setup(coil_A_1_pin, GPIO.OUT)
GPIO.setup(coil_A_2_pin, GPIO.OUT)
GPIO.setup(coil_B_1_pin, GPIO.OUT)
GPIO.setup(coil_B_2_pin, GPIO.OUT)

GPIO.output(enable_pin, 1)


def forward(steps, position): 
	global postion 
	for i in range(0, steps):
		setStep(1, 0, 1, 0)
		time.sleep(delay)
		setStep(0, 1, 1, 0)
		time.sleep(delay)
		setStep(0, 1, 0, 1)
		time.sleep(delay)
		setStep(1, 0, 0, 1)
		time.sleep(delay)
		position = position + 1

	return position


def backwards(steps, position):  
	for i in range(0, steps):
		setStep(1, 0, 0, 1)
		time.sleep(delay)
		setStep(0, 1, 0, 1)
		time.sleep(delay)
		setStep(0, 1, 1, 0)
		time.sleep(delay)
		setStep(1, 0, 1, 0)
		time.sleep(delay)
		position = position - 1

	return position

def setStep(w1, w2, w3, w4):
	GPIO.output(coil_A_1_pin, w1)
	GPIO.output(coil_A_2_pin, w2)
	GPIO.output(coil_B_1_pin, w3)
	GPIO.output(coil_B_2_pin, w4)


def savefile(position):
	w = open("position.sav", "w")
	w.write(str(position))
	w.close()

def processing():
	print "\n processing request...\n"



#rotation speed (time between coil phase changes) smaller number faster.  max = .002
delay = .003


print "-----------------------------------------" #divider for UI purposesposition = 0


try:
	
	f = open("position.sav")
	r = int(f.read())
	position = r

	cont = "y"  #initial state to start while loop

	while (cont == "y"):
		try:
			forsteps = int(raw_input("Forward rotation in steps: "))
		except ValueError:
			print "\n !!! Not Valid !!! \n Please type a natural number.\n"
			forsteps = int(raw_input("Forward rotation in steps: "))
		try:
			backsteps = int(raw_input("Backward rotation in steps: "))
		except ValueError:
			print "\n !!! Not Valid !!! \n Please type a natural number.\n"
			backsteps = int(raw_input("Backward rotation in steps: "))
		print "Confirm: %s steps forward. \n \t %s steps back." % (forsteps, backsteps)
		confirm = raw_input("y/n >> ")
		if (confirm == "y"):
			processing()
			position = forward(forsteps, position)
			position = backwards(backsteps, position)
		else:
			pass

		cont = raw_input("New input? y/n: ")

	zero = raw_input("back to zero? y/n: ")

	if (zero == "y"):
		if (position > 0):
			backsteps = position
			processing()
			position = backwards(backsteps, position)
			savefile(position)
		else:
			forsteps = -position
			processing()
			position = forward(forsteps, position)
			savefile(position)
	else:
		savefile(position)
	

finally:
# IMPORTANT!!
#
# .cleanup un-initializes the GPIO pins.
#
# Without this, the motor coils stay energized
# while the program is waiting long periods 
# for an input, or if the program throws an error.
# The energized coils can become surprisinly hot!
##################################################
	GPIO.cleanup()
