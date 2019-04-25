import itchat
import time
import RPi.GPIO as GPIO
'''set GPIO'''
GPIO.setmode(BCM)
GPIO.setwarnings(False)
open = 17

'''set itchat to login wechat and search group'''
itchat.auto_login(hotReload=True)
rooms = itchat.get_chatrooms(update=True)
rooms = itchat.search_chatrooms(name='itchat_test')
if rooms is not None:
    username = rooms[0]['UserName']
else:
    username = 'filehelper'

'''opendoor'''
def OpenDoor(angle):
	assert angle >=30 and angle <= 150
	pwm = GPIO.PWM(open, 50)
	pwm.start(8)
	dutyCycle = angle / 18. + 3.
	pwm.ChangeDutyCycle(dutyCycle)
	time.sleep(0.3)
	pwm.stop()

'''Listen wechat msg'''
@itchat.msg_register(itchat.content.TEXT,isGroupChat=True)
def reply_msg(msg):
    if msg['Content'] == u'开门':
            GPIO.setup(open, GPIO.OUT)
            OpenDoor(90)
            time.sleep(1.5)
            OpenDoor(30)
            itchat.send_msg("欢迎回家！",toUserName=username)
            GPIO.cleanup()

if __name__ == '__main__':
	itchat.run()