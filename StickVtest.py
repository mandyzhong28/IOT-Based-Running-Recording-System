import sensor, image ,time #forcam
import lcd #for lcd屏
from machine import I2C,UART
from fpioa_manager import fm #导入maipy的fm(fpioa manager)这个内置的对象，用于后续注册工作。

student_0={'student_number':'test1234567','student_0_name':'鍾思捷'}

#uart initial
fm.register(35, fm.fpioa.UART2_TX, force=True)
fm.register(34, fm.fpioa.UART2_RX, force=True)

uart_Port = UART(UART.UART2, 115200,8,0,0, timeout=1000, read_buf_len= 4096)
clock = time.clock()
lcd.init()
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QQVGA) # can be QVGA on M7...
sensor.set_vflip(1)
sensor.set_hmirror(1)
sensor.skip_frames(20)
sensor.run(1) #在OPENMV中會自動運行 miropython中不知道要不要加
sensor.set_auto_gain(False) #自动增益off
while(True):
    img = sensor.snapshot()
    #img.lens_corr(1.8) # strength of 1.8 is good for the 2.8mm lens.
    check =img.find_qrcodes()
    #print(check)
    if(len(check)>0):
        data=check[0].payload()
        print(data)
        uart_Port.write(data)
        time.sleep(2)
