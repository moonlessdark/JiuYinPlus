
九阴真经OL团练/授业脚本  

# 前言:  
本项目是本人用于学习opencv的实操作品，仅供学习。请勿用于商业。  
现在本人随缘玩九阴，所以脚本也随缘更新了。  

本脚本在经典模式 1.0缩放 1080P分辨率下切图，图标切图后大小为40*40。  
此脚本不支持后台键盘输入，请不要最小化窗口。   
在脚本执行过程中，请勿操作其他窗口，避免打断按钮的连续性。该过程中请让电脑自己运行，该去喝水的喝水，该玩手机的玩手机。  

  
# 系统硬件支持  
1、本脚本在win10系统开发，其他系统未做兼容和调试，不保证能正常使用。  
2、支持分辨率：  
&emsp;&emsp;理论上所有分辨率。可全屏可窗口模式，为了保证精度请确保分辨率大于1366*768。  
&emsp;&emsp;请保证游戏画面完整的显示在屏幕上，不要将窗口的部分画面移动到窗口之外，会影响画面识别。  
3、由于22年6月，瓜牛更新后导致免费版【大漠插件】已经不能在win10系统使用，只能在win7有效，所以后续版本决定移除大漠插件，改为使用【幽灵键鼠】，【幽灵键鼠】请去淘宝购买，最便宜的那一款就行了。  
4、请在启动脚本时，一定要确认好客户端设置的游戏缩放模式是【经典模式】还是【极致模式】，如果游戏客户端缩放模式与启动的脚本不一致，会导致无法识别到图像的。  
如何确认自己游戏缩放设置：游戏启动界面--左下角【游戏设置】-- 第一行【游戏缩放模式设置】，默认为【经典模式】  

# 注意
1、请勿在极致模式下使用。  
2、授业时最多只支持2个号在同一个场景同时授业，因为不持支绑定窗口，所以只能按了一轮后再切换另一个窗口按按钮。3个号的时候时间来不及。建议要3开授业时，最好分开到2个场景。     
3、运行时，请勿最小化游戏窗口，不然无法识别游戏画面。  
4、按钮执行时，请不要打开聊天框进行聊天，不然团练的按钮会直接输入到你的聊天框里面去了。  
同时，在按钮执行时，请不要干扰窗口，不要做其他操作，因为我只会在按钮执行前激活一次窗口，如果按钮在执行过程中窗口激活状态被干扰，会导致按钮失败。    
 
# 关于安全性
任何脚本都有被发现的风险。  
此脚本未绑定窗口，尽量减少被发现的几率。  
键盘操作调用幽灵键鼠，截图操作调用windowsapi，图片识别使用opencv处理。  
按钮之间增加随机等待时间，尽量表现的像个人(但是会影响执行速度，表现出的效果就是按键的时候时快时慢)  

# 更新日志  
2024年3月2日   
新增  
1、现在支持极致模式了。  
压缩包解压后，客户端设置了极致模式，请运行 JiuDancing_ultimate.exe 启动程序  
压缩包解压后，客户端设置了经典模式，请运行 JiuDancing_classics.exe 启动程序  
注意：极致模式并没有太多样本进行测试，如有问题请反馈。  
优化  
1、优化了使用工具截图时保存图片的逻辑，避免出现太多文件夹，每次使用截图功能，只会生成一个文件夹  


2024年1月20日  
1、优化获取游戏窗口画面的逻辑，理论上支持“经典模式”下的不同显示器缩放的分辨率。(已经测试100%缩放1080P，150%缩放4K分辨率，其他分辨率请自行测试，之前的版本只支持100%缩放下的分辨率)  
注意：实现的方法逻辑请看 DeskPage/DeskTools/WindowsSoft/windows.py 模块中 WindowsCapture().capture_and_clear_black_area() 方法  

2023年12月29日  
1、新增窗口激活失败时的重试机制(虽然我自己的电脑没有出现过窗口激活失败的问题)  


2023年12月7日  
1、修复在游戏客户端更新后游戏窗口句柄无法获取的问题  


2023年8月13日  
1、框架升级为Pyside6,Python版本为3.11(64位),放弃对win7的兼容  
2、幽灵键鼠的驱动更新为64位的3.0版本  
3、由于不再兼容win7，将不再调用大漠插件，只使用幽灵键鼠，所以对管理员权限的要求一并移除。  


2023年8月1日  
1、新增幽灵键鼠驱动(该模式需要配合usb硬件设备使用)。win10/win11下默认使用此驱动。win7系统依旧调用大漠插件。    
2、优化代码逻辑。  
3、移除微信公众号签到模块。  
注意：  
在win10/win11系统下，多开时有可能出现窗口切换失败的问题。在使用此脚本多开时，最好先自己测试一下，避免团练时坑到别人。  
如果真的会切换失败，要么换win7系统，要么每次只勾选一个窗口进行团练授业。

2023年6月6日  
瓜牛更新了一下版本，大漠插件在 win10/win11 系统已经不能使用了。只有win7还能使用。  

2022年11月5日  
1、新增对win7的支持  

2022年10月7日  
1、修复游戏窗口减少后重新获取时不正确的问题  
2、修复测试激活窗口时不能指定某个窗口的问题  


2022年9月12日  
1、优化大图找小图模式的执行速度(v0.0.9)  
2、释放公众号签到功能(签到28天有包裹拿哦)


2022年9月11日  
1、新增查找方式为大图找小图的版本(v0.0.8.1)  
&emsp;&emsp;该版本理论上支持所有分辨率，具体效果请自行测试


2022年9月11日  
1、新增支持4K(3840*2160)在150%缩放下的支持  
2、移除自动检测团练/授业是否已经结束的逻辑  
3、支持双屏显示器同时团练/授业(已测试1080P+4K)  
&emsp;&emsp;注意：由于4K分辨率的识别速度会比1080P慢，所以如果是2个号同时授业的话，请将2个号放到不同的场景，不然我怕最后几轮的时候识别后按钮来不及按。团练就无所谓  

2022年7月31日  
1、移除引用的第三方大漠插件的库，改为自行封装  
2、移除启动时注册大漠插件，改为免注册的方法调用  
3、移除pywin32库，其中包括win32gui和win32com  
4、使用大漠插件自带的方法获取窗口句柄  
5、优化按钮间隔时间

2022年4月3日  
1、更新了最新的代码  
2、修改了调用大漠的逻辑  
3、去除了差值哈希的对比逻辑，只保留均值和感知  
4、新增了判断团练和授业结束的逻辑

本脚本引用了：https://github.com/bode135/pydamo  

团练授业完成后，请手动停止程序，没有做自动停止
