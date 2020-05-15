import sensor, image ,time #forcam
import lcd #for lcd屏
from machine import I2C,UART
from fpioa_manager import fm #导入maipy的fm(fpioa manager)这个内置的对象，用于后续注册工作。


#uart initial
fm.register(35, fm.fpioa.UART2_RX, force=True)
fm.register(34, fm.fpioa.UART2_TX, force=True)
uart_Port = UART(UART.UART2, 115200,8,0,0, timeout=1000, read_buf_len= 4096)

clock = time.clock()
lcd.init() #lcd initial
#set camera

sensor.reset()
sensor.set_pixformat(sensor.RGB565) #RGB565 
sensor.set_framesize(sensor.QQVGA) # can be QVGA on M7...
sensor.set_vflip(1) 
sensor.set_hmirror(1) 
sensor.skip_frames(20)
sensor.run(1)
sensor.set_auto_gain(False) #自动增益off
while(True):
    img = sensor.snapshot()
    fps =clock.fps() #
    check =img.find_qrcodes()#scan img find qrcode
    if(len(check)>0):
        try:
            tuplexboxa =check[0].rect()
            data0=check[0].payload()
            img.draw_string(15,20,"Scan Successfully!",(236,36,36),scale=1.0)
            img.draw_rectangle(tuplexboxa,(236,36,36))
            lcd.display(img)#在Lcd 屏中顯示鏡頭取得的圖片
            data=eval(data0)
            data2=data.get('Student')
            data3=data2.get("context")
            check1=('Student' in data)
            check2=('value' in data2)
            check3=('context' in data2)
            check4=('CardID' in data3)
            check5=('name' in data3)
            if(check1==True & check2==True & check3==True & check4==True & check5==True):
                 uart_Port.write(str(data))#uart发送解码资料
                 time.sleep(2)
        except:
            print("Invalid QR code") #如二维码格式不符
            strerror="Invalid QR code"#
            lcd.display(strerror)#
