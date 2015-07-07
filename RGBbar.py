#!/usr/bin/env python
import RPi.GPIO as GPIO
import PCF8591 as ADC

Rpin = 11
Gpin = 12
Bpin = 13

GPIO.setmode(GPIO.BOARD)
GPIO.setup(Rpin, GPIO.OUT)
GPIO.setup(Gpin, GPIO.OUT)
GPIO.setup(Bpin, GPIO.OUT)

Rpwm = GPIO.PWM(Rpin, 2000)
Gpwm = GPIO.PWM(Rpin, 2000)
Bpwm = GPIO.PWM(Bpin, 5000)

def setup():
	ADC.Setup(0x48)
	Rpwm.start(100)
	Gpwm.start(100)
	Bpwm.start(100)

def map(x, in_min,in_max, out_min, out_max):
	return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

def setColor(R,G,B):
	Rpwm.ChangeDutyCycle(100-R)
	Gpwm.ChangeDutyCycle(100-G)
	Bpwm.ChangeDutyCycle(100-B)
	print R, G, B



def loop():
	while True:
		tmp = ADC.read(0)
		if tmp < 44:
			R = 100
			G = map(tmp,0, 43, 0, 100)
			B = 0
		elif tmp < 86:
			R = 100-map(tmp, 44, 85, 0, 100)
			G = 100
			B = 0
		elif tmp < 128:
			R = 0
			G = 100
			B = map(tmp, 86, 127, 0, 100)
		elif tmp < 170:
			R = 0
			G = 100-map(tmp, 128, 169, 0, 100)
			B = 100
		elif tmp < 212:
			R = map(tmp, 170, 211, 0, 100)
			G = 0
			B = 100
		elif tmp < 256:
			R = 100
			G = 0
			B = 100-map(tmp, 212, 255, 0, 100)
		
		setColor(R,G,B)
		print tmp

def destroy():
	ADC.write(0)
	Rpwm.stop
	Gpwm.stop
	Bpwm.stop
	GPIO.output(Rpin, GPIO.HIGH)
	GPIO.output(Gpin, GPIO.HIGH)
	GPIO.output(Bpin, GPIO.HIGH)
	GPIO.cleanup

if __name__ == "__main__":
	try:
		setup()
		loop()
	except KeyboardInterrupt:
		destroy()
