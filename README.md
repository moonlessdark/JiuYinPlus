

九阴真经团练助手3开版  
九阴真经OL团练/授业脚本  
# 前言:  
本项目是我用于学习opencv的实操作品，仅供学习。请勿用于商业。

本脚本在1080分辨率下切图，图标切图后大小为40*40。  
由于大漠插件是免费的，不支持后台键盘输入，请不要最小化窗口。   
如果您的电脑此前已经注册过大漠插件，请卸载注册信息。避免出现冲突。  
&emsp;&emsp;说明：由于当年在用淘宝的团练脚本时(就是那个麦卡助手)。这玩意应该是工作室流出来的，会先把游戏窗口缩小再去团练，不是太喜欢这种方式(虽然有利于提高效率)，所以我这个就强制窗口全屏。

使用的技术为 python3.9+pyqt5+opencv。  
  
# 系统硬件支持  
1、本脚本在win10系统开发，其他系统未做兼容，不保证能正常使用。  
2、支持分辨率：  
&emsp;&emsp;普通版本(v0.0.8，已停更)1080P(100%缩放)，4K分辨率(150%缩放)，需要窗口最大化模式使用。    
&emsp;&emsp;说明：此脚本采用最笨的坐标切图方式，但执行效率会高一点。而windows系统不同的分辨率缩放在窗口全屏模式下会影响坐标点的位置，所以使用时请确保您的缩放为 1080P下100%缩放，4K下150%缩放。    
&emsp;&emsp;大图找小图版(v0.0.8.1 及以上版本)，理论上支持所有分辨率。可全屏可窗口模式，请确保分辨率大于1366*768。
&emsp;&emsp; 注意：请勿在极致模式下使用。我得找时间兼容一些极致模式。  
 
# 关于安全性
任何脚本都有被发现的风险。  
此脚本采用大漠插件非注册的方式调用。且未绑定窗口，尽量减少被发现的几率。  
大漠插件只用于按下按钮，截图操作调用windowsapi，图片识别使用opencv处理。  
按钮之间增加随机等待时间，尽量表现的像个人(但是会影响执行速度，表现出的效果就是按键的时候时快时慢)  

# 更新日志  
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
注意：授业时最多只支持2个号在同一个场景同时授业，因为免费版大漠不持支绑定窗口，所以只能按了一轮候再切换另一个窗口按按钮。3个号的时候时间来不及。  

请以管理员权限运行，不然大漠插件无法正常运行。
先开游戏再开脚本，不然脚本拿不到窗口handle

此脚本暂不支持win7，在win10系统运行良好  

团练授业完成后，请手动停止程序，没有做自动停止
