import OPi.GPIO as GPIO
import datetime, time, sys, os

dtNow = datetime.datetime.now()
punchTime = [dtNow.strftime("%m-%d-%Y"), dtNow.strftime("%H:%M")]

GPIO.setmode(GPIO.BOARD)
GPIO.setup(7, GPIO.OUT)

def blink(color, blink):

        #GPIO.setmode(GPIO.BOARD)
        #GPIO.setup(color, GPIO.OUT)
        for x in range(blink):
                time.sleep(.2)
                os.system('echo 1 > /sys/class/leds/green_led/brightness')
                GPIO.output(color, GPIO.HIGH)
                time.sleep(.2)
                os.system('echo 0 > /sys/class/leds/green_led/brightness')
 #GPIO.cleanup()

def clock(action):
        if action == True:
            word = "CLOCKIN"

        elif action == False:
            word = "CLOCKOUT"

        with open('MasterTimeClockLog.csv', 'a+') as MasterLog:
                MasterLog.write("%s,%s,%s,%s\n" % ("Mieka", str(word), str(punchTime[0]), str(punchTime[1])))
        MasterLog.close()

        print '%s success!' % word

        if word == "CLOCKIN":
                blink(15, 5)

        elif word == "CLOCKOUT":
                blink(7, 5)
        else:
                print word




