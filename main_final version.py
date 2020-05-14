from m5stack import *
from m5ui import *
from uiflow import *
import wifiCfg
from m5mqtt import M5mqtt
import json
import time
import unit
import machine
from numbers import Number
def Wifi_reconnect():
  while (wifiCfg.wlan_sta.isconnected()) != 1:
    wifiCfg.reconnect()
  label0.setText('Wifi connected')

data = Noneial

#rfid init
rfid0 = unit.get(unit.RFID, unit.PORTA)

uart = None
t1 = None 
t2 = None


student_checkag=[] #存人数的列表
#mqtt initial
m5mqtt = M5mqtt('random', 'industrial.api.ubidots.com', 1883, 'BBFF-HXOoqxfhftjZSub2lDqbK019M3KHFg', '', 300)

#Label and tile set 
setScreenColor(0x000000)
label0 = M5TextBox(69, 33, "Running System", lcd.FONT_Comic,0x89eee1, rotate=0)
label1 = M5TextBox(40, 86, "Name :", lcd.FONT_DejaVu18,0xff66d2, rotate=0)
label2 = M5TextBox(76, 124, "ID :", lcd.FONT_DejaVu18,0xff66d2, rotate=0)
label3 = M5TextBox(40, 165, "Count :", lcd.FONT_DejaVu18,0xff66d2, rotate=0)
label4 = M5TextBox(135, 86, "", lcd.FONT_DejaVu18,0xff66d2, rotate=0)
label5 = M5TextBox(135, 124, "", lcd.FONT_DejaVu18,0xff66d2, rotate=0)
label6 = M5TextBox(135, 165, "", lcd.FONT_DejaVu18,0xff66d2, rotate=0)
label7 = M5TextBox(30, 188, "", lcd.FONT_DejaVu18,0xffd400, rotate=0)
label10 = M5TextBox(20, 35, "123", lcd.FONT_Default,0xFFFFFF, rotate=0)
label10.hide()
title10 = M5Title(title="Today runner list:", x=3 , fgcolor=0xFFFFFF, bgcolor=0x0000FF)
title10.hide()

#uart initial
uart = machine.UART(2, tx=17, rx=16) 
uart.init(115200, bits=8, parity=None, stop=1)

#var set
wifistatus = None
Name = None
count = None
uid = None
A = None
uartmsg=None
A_J = None
qruid=None
qrName=None
qrcount=None

m5mqtt.start()

#label hide and show 
def showlist():
  title10.show()
  label10.show()

def hidelist():
  title10.hide()
  label10.hide()
  
def showmainui():
  label0.show()
  label1.show()
  label2.show()
  label3.show()
  label4.show()
  label5.show()
  label6.show()
  label7.show()
  label8.show()
  label9.show()
  
def hidemainui():
  label0.hide()
  label1.hide()
  label2.hide()
  label3.hide()
  label4.hide()
  label5.hide()
  label6.hide()
  label7.hide()
  label8.hide()
  label9.hide()
  
def buttonA_wasPressed():
  showlist()

  global list_run
  list_run = ''
  student_checkag.sort()
  for i in range(len(student_checkag)):
    if(i==0):
      list_run=str(i+1)+'. '+student_checkag[i]+' '
      
    elif(i%4==0):
      list_run=str(i+1)+'. '+student_checkag[i]+' '+'\n'
      
    else:
      list_run=str(i+1)+'. '+student_checkag[i]+' '
      
  label10.setText(str(list_run))
  
  hidemainui()
  pass
btnA.wasPressed(buttonA_wasPressed)




def mainproamg():
  while True:
    while wifistatus == 0: #wifi set
      wifiCfg.auto_connect()
      Wifi_reconnect()
    try :
      if rfid0.isCardOn(): #如有卡片接触
        rgb.setColorAll(0xff0000)
        #rfid0.writeBlock(1,'213173444')
        #rfid0.writeBlock(2,'yangmi')
        
        uid = rfid0.readBlockStr(1)   #读UID
        if(str(uid) not in student_checkag):#该人本日是否有跑操记录
          Name = rfid0.readBlockStr(2) #读Name
          count = int((rfid0.readBlockStr(4))) #读跑操次數
          count = count + 1
          rfid0.writeBlock(4,str(count)) #刷新跑操次數 写入卡
          A = {"Student":{"value":count, "context":{"CardID":uid, "name" :Name }}}
          A_J = json.dumps(A) #生成JSON包
          label5.setText(str(uid))
          label4.setText(str(Name))
          label6.setText(str(count))
          m5mqtt.publish(str('/v1.6/devices/esp32'),str(A_J)) #publish mqtt
  
          student_checkag.append(str(uid)) #跑操者 寫入 列表
          speaker.sing(392, 1)  #铃声
          speaker.sing(349, 1)
          speaker.sing(330, 1)
          speaker.sing(294, 1)  
          wait_ms(1000)
          label7.setText(str(""))
        else: 
          #提示本日已經有拍卡
          label7.setText(str("Please do not scan again!"))
          wait_ms(2000)
          label7.setText(str(""))
    	
      elif(uart.any()): #如uart有资料
        #label5.setText(str("enter qr"))
        uartmsg = str((uart.read()).decode())#qrcode msg
        #label5.setText(str(uartmsg))
        save_d =eval(uartmsg)
        #label5.setText(str(uartmsg))
        qruid=save_d.get('Student').get('context').get('CardID')
        label5.setText(str(qruid))
        if(str(qruid) not in student_checkag): #该人本日是否有跑操记录
          qrcount=save_d.get('Student').get('value')#解释dict 取其中的关键值
          qrName=save_d.get('Student').get('context').get('name')
          qrcount=int(qrcount+1)
          label5.setText(str(qruid))
          label4.setText(str(qrName)) 
          label6.setText(str(qrcount))
          
          B = {"Student":{"value":qrcount, "context":{"CardID":qruid, "name" :qrName }}}
          B_J = json.dumps(B)
          m5mqtt.publish(str('/v1.6/devices/esp32'),str(B_J)) 
          student_checkag.append(str(qruid))
          wait_ms(2)
        else:
          label7.setText(str("Please do not scan again!"))
          wait_ms(2000)
          label7.setText(str(""))
        pass
    
    except:
      wait(1)
    wait_ms(2)
    
def buttonB_wasPressed():
  hidelist()
  showmainui()
  mainproamg()
  pass
btnB.wasPressed(buttonB_wasPressed)


mainproamg()