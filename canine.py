import cwiid
import os
import pygame
import pygame.mixer
import random
from pygame.mixer import Sound
from gpiozero import Robot
from gpiozero import LED
from gpiozero import Button
from signal import pause
from time import sleep

robot = Robot(left=(10, 9), right=(8, 7))
red = LED(27)
blue = LED(22)
button = Button(17)
button_delay = 0.1

def barking():
    randomfile = random.sample(os.listdir("/home/pi/K9audio/"), 1)[0]
    wooffile = '/home/pi/K9audio/'+ randomfile
    woof = Sound(wooffile)
    woof.play()

red.on()
blue.on()
pygame.mixer.init()
randomfile = ''
wooffile = ''
file = '/home/pi/K9audio/i-am-k9-mk-3.wav'
bark = Sound(file)
bark.play()
sleep(5)

button.when_pressed = barking

blue.blink()
try:
    wii=cwiid.Wiimote()

except RuntimeError:
    # Uncomment this line to shutdown the Pi if pairing fails
    #os.system("sudo halt")
    quit()

wii.led = 1
blue.on()
yesfile = '/home/pi/K9audio/affirmative.wav'
yes = Sound(yesfile)
yes.play()

wii.rpt_mode = cwiid.RPT_BTN

while True:
    buttons = wii.state['buttons']

    # If Plus and Minus buttons pressed
    # together then rumble and quit.
    if (buttons - cwiid.BTN_PLUS - cwiid.BTN_MINUS == 0):
        wii.rumble = 1
        sleep(1)
        wii.rumble = 0
        red.off()
        blue.off()
        os.system("sudo halt")
        exit(wii)

    if (buttons & cwiid.BTN_LEFT):
        robot.left()
        sleep(button_delay)

    elif(buttons & cwiid.BTN_RIGHT):
        robot.right()
        sleep(button_delay)

    elif (buttons & cwiid.BTN_UP):
        robot.forward()
        sleep(button_delay)

    elif (buttons & cwiid.BTN_DOWN):
        robot.backward()
        sleep(button_delay)

    elif (buttons & cwiid.BTN_A):
        barking()
        sleep(button_delay)

    else:
        robot.stop()
