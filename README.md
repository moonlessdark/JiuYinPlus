

# JiuYinPlus
九阴真经团练助手3开版  
九阴真经OL团练/授业脚本  
# 前言:  
本项目仅用于学习分享opencv的图片对比功能。请勿用于商业。

本脚本在1080分辨率下切图，请在1080p的分辨率下开启窗口模式，并双击窗口满屏(窗口最大化)显示。  
由于大漠插件是免费的，不支持后台键盘输入。   
如果您的电脑此前已经注册过大漠插件，请卸载注册信息。避免出现冲突。  
说明：由于当年在用淘宝的团练脚本时(就是那个麦卡助手)。这玩意应该是工作室流出来的，会先把游戏窗口缩小再去团练，不是太喜欢这种方式(虽然有利于提高效率)，所以我这个就强制窗口全屏。

使用的技术为 python3.9+pyqt5+opencv。  
  
# 系统硬件支持  
1、本脚本在win10系统开发，其他系统未坐兼容，不保证能正常使用。  
2、支持分辨率：1080P(100%缩放)，4K分辨率(150%缩放)。  
说明：此脚本采用最笨的坐标切图方式，而windows系统不同的分辨率缩放在窗口全屏模式下会影响坐标点的位置，所以使用时请确保您的缩放为 1080P下100%缩放，4K下150%缩放  
至于其他的分辨率，在我找到获取游戏窗口在不同分辨率的显示器下的缩放后再进行处理。  



# 更新日志  

2022年9月11日  
1、新增支持4K(3840*2160)在150%缩放下的支持  
2、移除自动检测团练/授业是否已经结束的逻辑  
3、支持双屏显示器同时团练/授业(已测试1080P+4K)  
注意：由于4K分辨率的识别速度会比1080P慢，所以如果是2个号同时授业的话，请将2个号放到不同的场景，不然我怕最后几轮的时候识别后按钮来不及按。团练就无所谓  

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
注意：授业时最多只支持2个号在同一个场景同时授业，因为免费版大漠不持支绑定窗口，所以只能按了一轮候再切换另一个窗口按按钮。3个号的时候时间来不及。  

请以管理员权限运行，不然大漠插件无法正常运行。
先开游戏再开脚本，不然脚本拿不到窗口handle

此脚本暂不支持win7，在win10系统运行良好  

团练授业完成后，请手动停止程序，没有做自动停止
