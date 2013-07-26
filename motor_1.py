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

def forward(steps):  
  for i in range(0, steps):
    setStep(1, 0, 1, 0)
    time.sleep(delay)
    setStep(0, 1, 1, 0)
    time.sleep(delay)
    setStep(0, 1, 0, 1)
    time.sleep(delay)
    setStep(1, 0, 0, 1)
    time.sleep(delay)

def backwards(steps):  
  for i in range(0, steps):
    setStep(1, 0, 0, 1)
    time.sleep(delay)
    setStep(0, 1, 0, 1)
    time.sleep(delay)
    setStep(0, 1, 1, 0)
    time.sleep(delay)
    setStep(1, 0, 1, 0)
    time.sleep(delay)

def setStep(w1, w2, w3, w4):
  GPIO.output(coil_A_1_pin, w1)
  GPIO.output(coil_A_2_pin, w2)
  GPIO.output(coil_B_1_pin, w3)
  GPIO.output(coil_B_2_pin, w4)

#time between coil phase changes
delay = .003


cont = "y"  #initial state to start while loop


print "--------------------------------------" #divider for UI purposes

try:

	while (cont == "y"):
		forsteps = raw_input("Forward rotation in steps: ")
		backsteps = raw_input("Backward rotation in steps: ")
		print "Confirm: %s steps forward. \n \t %s steps back." % (forsteps, backsteps)
		confirm = raw_input("y/n >> ")
		if (confirm == "y"):
			print "\n processing request...\n"
			forward(int(forsteps))
			backwards(int(backsteps))
		else:
			pass

		cont = raw_input("New input? y/n: ")

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