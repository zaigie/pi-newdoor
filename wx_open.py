import itchat
import time
import RPi.GPIO as GPIO
'''set GPIO'''
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
open = 12
fPWM = 50
a = 10
b = 2
GPIO.setup(open, GPIO.OUT)
pwm = GPIO.PWM(open, fPWM)
def setup():
    global pwm
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(open, GPIO.OUT)
    pwm = GPIO.PWM(open, fPWM)
    pwm.start(0)

'''set itchat to login wechat and search group'''
itchat.auto_login(hotReload=True)
rooms = itchat.get_chatrooms(update=True)
rooms = itchat.search_chatrooms(name='door')  #name='你的微信群名'
if rooms is not None:
    username = rooms[0]['UserName']
else:
    username = 'filehelper' #如果微信群名不存在就通过文件助手发

'''opendoor'''
def OpenDoor(direction):
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(open, GPIO.OUT)
    pwm.start(0)
    duty = a / 180 * direction + b
    pwm.ChangeDutyCycle(duty)
    print("direction =", direction, "-> duty =", duty)
    time.sleep(1)

'''Listen wechat msg'''
@itchat.msg_register(itchat.content.TEXT,isGroupChat=True)
def reply_msg(msg):
    if msg['Content'] == u'开门':
            OpenDoor(150)
            time.sleep(1)
            OpenDoor(0)
            itchat.send_msg("欢迎回来！" ,toUserName=username)
            GPIO.cleanup()

if __name__ == '__main__':
	itchat.run()