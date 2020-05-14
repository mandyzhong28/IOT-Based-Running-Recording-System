# IOT-Based-Running-Recording-System
This is a repository for an IOT based Running Recording System

# 项目目标
1.通过ESP32作为主控芯片实现打卡系统的基本逻辑功能
2.利用RFID Unit 实现IC卡的信息识别、读取功能
3.基于MQTT信息传输技术实现跑操信息的”线下-云平台“交互功能
4.使用M5 StickV实现二维码识别技术

# 项目意义
我们所设计的跑操打卡系统是针对学校的现有的人工跑操打卡系统所作出的改善。在现有的校内人工打卡系统当中，每一位参与跑操的同学需要持校园一卡通到达跑操点，手动“拍卡”后，再由体育系相关负责老师手动将打卡数据上传至体育系数据库。以上打卡流程存在较明显的问题：
1） 由于系统数据更新的时效性较差，同学们无法实现跑操次数实时查询的愿望，甚至有部分同学一周后仍然无法查到自己的打卡情况，耽误后面的跑操计划；
2）由于打卡机的功能老旧，仅支持“拍卡”打卡，部分同学由于个人疏漏出现忘带卡的情况，直接导致当日跑操记录作废。针对以上问题，我们想借助本次竞赛完成对现有跑操系统的改善，从而实现：
1）线上线下同步打卡：现场完成打卡后，系统后台自动联网更新，实时保存打卡记录，并通过短息或微信消息通知打卡人；
2）多途径打卡：实体卡打卡不再是唯一打卡方式，同学们还可以通过扫描二维码或条形码的方式实现电子打卡。

# 项目原理
设置MQTT伺服器有三个步骤：
1.设置MQTT伺服器
 设置MQTT伺服器的三大要素是：服务器ID，用户名和密码。其他要素，比如端口号是1883，一般都是用这个的，还有服务器是该平台的网址。
2.发布数据
 发布数据的两个要点是主题和数据格式。主题的格式不同的平台会有不同的要求，建议参考平台的API参数。第二是数据格式，一般都是用JSON格式。
3.订阅数据
订阅数据和发布数据基本相同，也是设置主题和数据。但发布和订阅的主题不同。因为MQTT是比较简单的通讯协议，所以安全性要由中间人来提供。
订阅数据会返回Mid, Result两个值，可以透过这两个值检查数据有没有错误和有没 有上传成功，具体语句可以看PahoMQTT库。

# M5StickV
设置M5StickV识别二维码的步骤：
1.使用micropython自带的sensor和image库，分别设置摄影镜头和图像的参数。而LCD库为控制屏幕显示的参数。我们我镜头参数设定如下
 图像色彩格式:选择是RGB565色彩图。
 设置图像像素大小，sensor.QQVGA: 160x120。
2.把img设为获取摄影机的图像。
 使用img库的find_qrcode是检测图上是否有qrcode，如果有则会返回一系列的qrcode的参数，如解析的数据,规格等。
3.因为我们主要用的是解码的代码，所以单独取解码结果来作下一步使用。

# RFID
RFID卡的结构有UID和BLOCKS。 UID是每张卡的唯一识别码，只可读不可写。 BLOCKS是可读可写的，因此我们把学生的资料放在BLOCKS里。值得注意的时要加入延时，否则如果进行可累加的操作，会因为射频处理识别的频率高而多次识别。

# UART
通用异步收发传输器（Universal Asynchronous Receiver/Transmitter，通常称作UART） 是一种串行异步收发协议，应用十分广泛。 UART工作原理是将数据的二进制位一位一位的进行传输。在UART通讯协议中信号线上的状态位高电平代表’1’低电平代表’0’。当然两个设备使用UART串口通讯时，必须先约定好传输速率和一些数据位。
在进行传输前必须要对硬件进行连接，连接方式如图所示：
![image](https://github.com/mandyzhong28/IOT-Based-Running-Recording-System/blob/master/uart%E5%8E%9F%E7%90%86%E5%9C%96.png)
 TX：发送数据端，要接对面设备的RX
 RX：接收数据端，要接对面设备的TX
 GND：保证两设备共地，有统一的参考平面

我们先分析我们使用到的器件的接口，可以从硬件设计图中找到我们使用到的器件，M5Go Lite的TX和RX接口为GPIO17和GPIO16，而M5StickV的TX和RX为GPIO35和GPIO34。
使用方法为调用Micropython带有的uart库，设置好相应平台。
# 设计简图
![image](https://github.com/mandyzhong28/IOT-Based-Running-Recording-System/blob/master/design%20diagram.png)
