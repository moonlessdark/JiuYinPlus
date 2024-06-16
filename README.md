
# <div align='center'>九阴真经OL摸鱼小助手</div> 

<div align=center>
<img src="https://github.com/moonlessdark/JiuYinDance/blob/master/DeskPageV2/Resources/cover.png">
</div>

## 前言:  
本项目是用于学习opencv与PySide6的实操作品，仅供学习。免费作品,请勿用于商业。  

此脚本支持的功能较少，且不算稳定，抗干扰性较差，只适合在老区养老，不适合新区养号。  
若您需要更多的功能，建议参考以下2种收费的脚本:  
1、麦卡Mac助手，可以在淘宝购买。  
2、PC助手·九阴全系列解决方案，访问地址: https://www.ookan.com/  
注: 由于这2种脚本都是只能在win7可以后台绑定窗口，而win10/win11只能前台窗口，应该都是调用了大漠插件编写的。  

本脚本在win10系统开发，其他系统未做兼容和调试，不保证能正常使用。  
此脚本为“图色脚本”，不支持窗口绑定，不支持窗口最小化。  

## 系统硬件与设置  
### 硬件  
* 22年6月蜗牛更新之后，免费版大漠插件只能在win7系统使用，此脚本改为使用“幽灵键鼠”(一个小U盘)。  
“幽灵键鼠”请在淘宝购买，买最便宜的那款就行了。  

### 游戏设置
* 启动脚本前，一定要确认好客户端设置的游戏缩放模式是【经典模式】还是【极致模式】，如果游戏客户端缩放模式与启动的脚本不一致，会导致无法识别到图像的。  
&emsp;&emsp;Q: 如何确认自己游戏缩放设置?  
&emsp;&emsp;A: 游戏启动界面--左下角【游戏设置】-- 第一行【游戏缩放模式设置】，默认为【经典模式】  
注意: releases 只打包了“经典模式”，如果需要"极致模式"请自行打包，打包文件为“main_ultimate.spec”，打包库为Pyinstaller  

### 游戏窗口分辨率  

* 为了保证精度请确保分辨率大于 “1366*768” 。小于此分辨率切图会缩放变形，切图模板会无法识别。    
窗口或者全屏模式不影响脚本的运行。  

* 请保证游戏画面完整的显示在屏幕上，不要将窗口的部分画面移动到窗口之外，会影响画面识别。  

### 脚本设置  
* 模板的匹配阈值建议保持0.9(团练授业)和0.8(挖宝的修罗刀，望辉洲的跳舞)。  
如果出现识别不到按钮的情况，请下调0.1再尝试。但不要设置过高，毕竟切图后模板的精度不太高。  

##  功能说明事项
<div align=center>
<img src="https://github.com/moonlessdark/JiuYinDance/blob/master/DeskPageV2/Resources/cover2.PNG">
</div>


### 关于团练授业，隐士势力的修炼  
* 注意：功能列表中的“隐士势力”不是指隐士势力中的日常任务，而是某些隐士势力会有绿色的 “上下左右JK” 按钮。当前版本在 望辉洲 的舞蹈周长，天涯海阁的瀑布修炼，钓鱼。 挖宝活动中BOSS的修罗刀 存在此按钮。    

* 游戏过程中，如果切换了画质，请进出一下家园或者切换一下地图场景，让游戏渲染的画面重新加载一下，再重新打开脚本，避免识别异常。

* 授业时最多只支持2个号在同一个场景同时授业，因为不持支绑定窗口，所以只能按了一轮后再切换另一个窗口按按钮。  
3个号的时候时间来不及。建议要3开授业时，最好分开到2个场景。     

* 按钮执行时，请不要打开聊天框进行聊天，不然团练的按钮会直接输入到你的聊天框里面去了。  
同时，在按钮执行时，请不要干扰窗口，不要做其他操作，因为我只会在按钮执行前激活一次窗口，如果按钮在执行过程中窗口激活状态被干扰，会导致按钮失败。   

* 如果你的电脑双开时有窗口切换失败的问题，请参考 https://blog.csdn.net/qq_26013403/article/details/129122971 此教程的方法修改注册表并重启电脑，以管理员权限运行脚本。如果依旧有问题的话我暂时也没撤了，只能进行单开团练授业。  

### 关于键盘连按  
* 键盘连点器，暂时只支持字母和数字和F1-F12，CTRL和shift，支持组合键。 不支持鼠标。  

### 关于押镖任务  
*  押镖地图推荐: 洛阳和燕京。  
*  <b><font color=red>镖车打怪时，请不要用鼠标点击窗口，不然会导致“格挡”NPC技能的按键无效。</font></b>
*  <font color=red>在使用押镖之前，请先去脚本资源目录(\Resources\)下的“SkillGroup.json”文件修改一下您的技能按键。</font>  
字段说明:  
例如:  "梵心降魔": {"CD": 2, "active_cd": 1, "level": 2, "key": "Q"}  
1: 梵心降魔===>技能名称，用于判断这是哪个技能，String类型，填写时请确保有双引号。  
2: CD===>技能冷却时间，Int类型，请根据你这个技能的实际冷却时间填写。  
3: active_cd===>技能释放动作的时间(即:放技能时摆Pose的时间)，Int类型。技能按下之后，会根据此时间等待摆完Pose再按下一个。  
4: level===>技能释放有限度，Int类型。数字越小越先释放。  
5: key===>技能对应的键盘按键，String类型，填写时请确保有双引号。请根据实际情况填写。不支持组合键。  

* 注意: 怒气招请的优先级请设置为最低。因为没有判断当前角色的“怒气值”是否足够。或者怒气招如果是加BUFF类型的，干脆就不填写此招式。  
* 如果您也是一个峨眉使用金鼎套路，那么就只需要修改对应的 “Key”(技能对应的键盘按键)即可。 
* 押镖时建议先按F8屏幕一下其他玩家，减少干扰。  
* <b><font color=red>目前押镖只支持“御风神水”，不支持骑马。</font></b>
* 每次执行押镖任务时，默认押镖次数为5次。如果需要修改，请在“配置”--“修改配置”--“最大押镖次数”输入您需要的次数。
* 目前还没有做过多的干扰项判断(比如垃圾四害的干扰)，在打劫镖的NPC时，会受到游戏内的横幅提示的影响。(例如：某某帮会发动了追杀，某某玩家砸蛋出了金丝粉)，横幅会的出现会遮挡劫镖NPC放技能的图标，导致人物无法格挡技能被击飞，影响后续的镖车判断。  

### 关于世界竞拍  
* 只会去竞拍关注列表中的物品，当关注列表中没有物品时将自动结束竞拍。  
* 请设置最大竞拍价格，当关注列表中的物品已经大于最大价格时，将跳过此物品不再加价。当前物品的竞拍人是本人时，跳过加价。  
* 最多同时支持7个物品的识别(关注列表1页刚好7个)。会识别这7个物品中的价格最低的物品进行加价，如果你有非常想要的物品，那么请只关注1个即可。
* 特别注意：此功能画面识别度较低，速度有点慢，适合咸鱼状态下的竞拍。如果你真的很急，请去找游戏内的商家或者购买收费的脚本。  

## 关于安全性
* 任何脚本都有被发现的风险。  
* 此脚本未绑定窗口，尽量减少被发现的几率。  
* 键盘操作调用幽灵键鼠，截图操作调用windowsapi，图片识别使用opencv处理。  
* 按钮之间增加随机等待时间，尽量表现的像个人(但是会影响执行速度，表现出的效果就是按键的时候时快时慢)  

# 更新日志  

2024年6月15日  
新增:  
1、押镖功能(测试版,有问题是正常的)  
2、世界竞拍  

2024年4月11日  
修复：  
1、Debug模式下日志文件反复创建失败的问题  
2、DeBug模式下区域阈值过低时日志打印太频繁的问题  


2024年4月10日  
新增：  
1、设置--配置信息 新增支持修改 按钮区域的识别阈值  
2、Debug模式改为在程序根目录写入Log文件  
修复：  
1、在win10系统上高分辨率(4K 150%缩放)下识别异常的问题(想用新方法，结果翻车了，还是用回旧方法)。   
2、修复键盘连点器 等待时间的判断逻辑错误  

2024年4月4日  
新增：  
1、键盘连点器，暂时只支持字母和数字和F1-F12，CTRL和shift，支持组合键。  
优化  
1、优化团练授业和隐士/势力跳舞的判断逻辑。  
修复：  
1、修复自动截图时没有判断黑屏引起的图片未判断为空的问题。  

2024年4月3日  
新增  
1、新增菜单配置，支持修改 匹配阈值，可以根据自身情况调整最适合自己的。  
2、支持Debug模式  
优化  
1、增加识别按钮的判断逻辑，会先大致判断画面中有几个按钮，再来具体的识别是哪些，避免阈值设置的过低识别到了一些错误的按钮。  
但是如果阈值设置的过高会导致部分按钮识别不到。  
已知BUG：  
1、隐士/势力的修炼还未调试，先不要使用。  


2024年3月21日  
优化：  
1、尝试兼容 峨眉场景晚上7点半开始的第二轮第8次授业时，从白天场景切换夜晚场景时画面更新引起的识别异常(通过降低识别阈值的暂时解决)  
2、尝试兼容 设置新的游戏画质后，在不切换场景重新加载画面时的识别率(通过降低识别阈值的暂时解决)  


2024年3月10日  
新增:  
1、新增底部状态栏进度条和统计本次执行识别到了几轮  
优化：  
1、重写了找图逻辑，按钮图标模板重新切图，优化了对不同分辨率的支持。  
2、优化了对窗口分辨率的检测，执行过程中当窗口分辨率小于1366*768或者窗口最小化时会有提示。    
已知BUG：  
1、峨眉场景授业，白天场景切换到夜晚场景时，按钮识别异常的问题。  
2、在当前场景切换了画质后(例如：中等画质切换到高级画质)，如果不重新加载一下地图(最简单的方法就是进入一下家园), 会导致脚本识别失败。  


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
