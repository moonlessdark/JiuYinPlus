import platform
import time

from PySide6 import QtWidgets, QtCore
from PySide6.QtGui import QTextCursor

from PySide6.QtWidgets import QMessageBox

from DeskPageV2.DeskGUIQth.UIQth import QProgressBarQth
from DeskPageV2.DeskGUIQth.danceQth import (DanceThByFindPic, ScreenGameQth)
from DeskPageV2.DeskGUIQth.keyAutoQth import AutoPressKeyQth
from DeskPageV2.DeskGUIQth.truckQth import (TruckCarTaskQth, TruckTaskFightMonsterQth)
from DeskPageV2.DeskGUIQth.marketQth import MarKetQth
from DeskPageV2.DeskPageGUI.MainPage import MainGui
from DeskPageV2.DeskTools.DmSoft.get_dm_driver import getDM, getWindows, getKeyBoardMouse
from DeskPageV2.DeskTools.GhostSoft.get_driver_v3 import GetGhostDriver, SetGhostBoards
from DeskPageV2.DeskTools.WindowsSoft.get_windows import GetHandleList, WindowsCapture
from DeskPageV2.Utils.dataClass import DmDll, GhostDll, Config
from DeskPageV2.Utils.keyEvenQTAndGhost import check_ghost_code_is_def
from DeskPageV2.Utils.load_res import GetConfig
from DeskPageV2.DeskFindPic.findAuctionMarket import FindAuctionMarket


class Dance(MainGui):
    """
    团练授业
    """

    file_config = GetConfig()

    _fight_monster_qth_sub_thread = None  # 线程对象
    _find_track_qth_sub_thread = None  # 线程对象

    def __init__(self):
        super().__init__()
        # 初始化一些对象
        self.th = DanceThByFindPic()
        self.th_screen = ScreenGameQth()
        self.th_progress_bar = QProgressBarQth()
        self.th_key_press_auto = AutoPressKeyQth()
        self.th_market = MarKetQth()

        # 押镖
        self.th_truck_task = TruckCarTaskQth()  # 运镖
        self.th_truck_fight_monster = TruckTaskFightMonsterQth()  # 打怪

        # # 键盘驱动对象
        self.dm_window = getWindows()
        self.dm_key_board = getKeyBoardMouse()

        # 定义3个窗口的handle
        self.gui_windows_handle_list = []

        # 定义一些变量
        self.dm_driver = None  # 大漠驱动
        self.handle_dict: dict = {}
        self.execute_button_status_bool: bool = False  # 按钮状态，用于判断文字显示

        self.keyboard_type = None  # 加载的键盘驱动类型

        self.is_debug = False

        # 初始化一些控件的内容
        self.radio_button_school_dance.setChecked(True)

        # 初始化一些对象
        self.loading_driver()
        self.load_config()
        self.progress_bar_action(0)  # 先把进度条隐藏了

        # 信号槽连接
        self.th.status_bar.connect(self.print_status_bar)
        self.th.sin_out.connect(self.print_logs)
        self.th.sin_work_status.connect(self._th_execute_stop)
        self.th_screen.status_bar.connect(self.print_status_bar)
        self.th_screen.sin_out.connect(self.print_logs)
        self.th_progress_bar.thread_step.connect(self.progress_bar_action)

        self.th_key_press_auto.sin_out.connect(self.print_logs)
        self.th_key_press_auto.sin_work_status.connect(self._th_execute_stop)

        self.th_market.sin_out.connect(self.print_logs)
        self.th_market.sin_work_status.connect(self._th_execute_stop)

        # 押镖相关的信号槽
        self.th_truck_task.sin_out.connect(self.print_logs)
        self.th_truck_task.next_step.connect(self.truck_task_func_switch)
        self.th_truck_task.sin_work_status.connect(self._th_execute_stop)
        self.th_truck_task.sin_status_bar_out.connect(self.print_status_track_bar)

        self.th_truck_fight_monster.sin_out.connect(self.print_logs)
        self.th_truck_fight_monster.next_step.connect(self.truck_task_func_switch)

        self.text_browser_print_log.textChanged.connect(lambda: self.text_browser_print_log.moveCursor(QTextCursor.End))

        # click事件的信号槽
        self.push_button_start_or_stop_execute.clicked.connect(self.click_execute_button)
        self.push_button_get_windows_handle.clicked.connect(self.get_windows_handle)
        self.push_button_test_windows.clicked.connect(self.test_windows_handle)
        self.radio_button_key_auto.toggled.connect(self.set_ui_key_press_auto)

        self.radio_button_auction_market.toggled.connect(self.set_ui_market_goods_list)

        # 按钮设置
        self.push_button_save_key_press_add.clicked.connect(self.key_press_even_add)
        self.push_button_save_key_press_delete.clicked.connect(self.key_press_even_del)
        self.push_button_save_key_press_save.clicked.connect(self.key_press_even_save)

        # 其他的
        self.widget_dock_setting.visibilityChanged.connect(self.load_config)
        self.push_button_save_setting.clicked.connect(self.update_config)
        self.widget_dock.visibilityChanged.connect(self.on_top_level_changed)

        # 获取竞拍物品列表
        self.push_button_market_get_goods_list.clicked.connect(self.get_screen_market_goods_list)

        # 设置技能
        self._button_save_skill_table.clicked.connect(self.save_skill_table)
        self.action_edit_skill_list.triggered.connect(self.open_skill_table)

    def hot_key_event(self, data):
        # print(f"当前按下的键盘value是——{data}")
        if data == 7995392:
            self.click_execute_button()

    @staticmethod
    def on_application_about_to_quit():
        """
        资源释放: 正在关闭应用程序...
        在这里释放资源，比如文件句柄、数据库连接等。
        在这里主要是断开幽灵键鼠的连接
        """
        SetGhostBoards().release_all_key()  # 释放所有按钮
        SetGhostBoards().close_device()
        time.sleep(0.1)

    @staticmethod
    def get_windows_release() -> int:
        """
        获取windows版本
        :return: 7, 8, 10
        """
        return int(platform.release())

    @staticmethod
    def get_local_time():
        """
        获取当前时间
        :return:
        """
        time_string: str = time.strftime("%H:%M:%S", time.localtime(int(time.time())))
        return time_string

    def load_config(self, is_top_level=True):
        """
        加载配置文件
        :return:
        """
        if is_top_level:
            config_ini: Config = self.file_config.get_find_pic_config()
            is_debug: bool = config_ini.is_debug
            dance_threshold: float = config_ini.dance_threshold
            whz_dance_threshold: float = config_ini.whz_dance_threshold
            area_dance_threshold: float = config_ini.area_dance_threshold
            truck_car_max_sum: int = config_ini.truck_car_sum
            self.line_dance_threshold.setValue(dance_threshold)
            self.line_whz_dance_threshold.setValue(whz_dance_threshold)
            self.line_area_dance_threshold.setValue(area_dance_threshold)
            self.line_max_truck_car_sum.setValue(truck_car_max_sum)
            if is_debug:
                self.check_debug_mode.setChecked(True)
            else:
                self.check_debug_mode.setChecked(False)

    def show_dialog(self, tips: str):
        """
        创建一个消息框，并显示
        :param tips:
        :return:
        """
        QMessageBox.information(self, '提示', tips)

    def update_config(self):
        """
        更新配置文件
        :return:
        """

        dance_threshold = self.line_dance_threshold.value()
        whz_dance_threshold = self.line_whz_dance_threshold.value()
        area_dance_threshold = self.line_area_dance_threshold.value()
        truck_car_max_sum = self.line_max_truck_car_sum.value()
        is_debug = True if self.check_debug_mode.isChecked() else False

        self.file_config.update_find_pic_config(dance_threshold_tl=dance_threshold,
                                                dance_threshold_whz=whz_dance_threshold,
                                                dance_threshold_area=area_dance_threshold,
                                                truck_car_max_sum=truck_car_max_sum,
                                                debug=is_debug)

        self.show_dialog("更新成功")

    def loading_driver(self):
        """
        加载驱动
        :return:
        """
        self.push_button_get_windows_handle.setEnabled(False)
        is_load_keyboard_driver: bool = False

        self.print_logs("开始尝试加载幽灵键鼠")
        if self._loading_driver_ghost():
            is_load_keyboard_driver = True
        else:
            pass
            # if self.get_windows_release() == 7:
            #     if ctypes.windll.shell32.IsUserAnAdmin() == 1:
            #         self.print_logs("\n当前系统是win7，开始尝试加载大漠插件")
            #         # 如果当前系统是win7，那么就启用大漠插件，那么优先检查是否有幽灵键鼠，没有的话就使用大漠插件
            #         if self._loading_driver_dm():
            #             is_load_keyboard_driver = True
            #     else:
            #         QMessageBox.critical(None, "Error", "当前系统是win7，请以“管理员”权限运行此脚本")
            #         self.print_logs("\n")
        if is_load_keyboard_driver is True:
            self.push_button_get_windows_handle.setEnabled(True)

    def _loading_driver_ghost(self) -> bool:
        """
        加载幽灵键鼠标驱动
        :return:
        """
        ghost_tools_dir: GhostDll = self.file_config.get_dll_ghost()
        GetGhostDriver(dll_path=ghost_tools_dir.dll_ghost)
        if GetGhostDriver.dll is not None:
            SetGhostBoards().open_device()  # 启动幽灵键鼠标
            if SetGhostBoards().check_usb_connect():
                self.print_logs("幽灵键鼠加载成功。\n如有疑问，请查看“帮助”-“功能说明”")
                self.keyboard_type = "ghost"
                return True
            else:
                self.print_logs("未检测到usb设备,请检查后重试")
        else:
            self.print_logs("幽灵键鼠驱动加载失败,请确认是否缺失了驱动文件,请检查后重试")
        return False

    def _loading_driver_dm(self) -> bool:
        """
        加载大漠插件驱动
        注意：此免费版本不支持win7以上的系统
        :return:
        """
        dm_tools_dir: DmDll = self.file_config.get_dll_dm()
        self.dm_driver = getDM(dm_reg_path=dm_tools_dir.dll_dm_reg, dm_path=dm_tools_dir.dll_dm)

        dm_release: str = self.dm_driver.get_version()
        if dm_release is not None:
            self.print_logs("大漠驱动免注册加载成功")
            self.keyboard_type = "dm"
            return True
        else:
            return False

    def print_logs(self, text, is_clear=False):
        """
        打印日志的方法
        :param is_clear: 是否清除日志
        :param text: 日志内容
        :return:
        """
        if is_clear:
            self.text_browser_print_log.clear()
        self.text_browser_print_log.insertPlainText(f"{self.get_local_time()} {text}\n")

    def progress_bar_action(self, step: int):
        """
        进度条跑马灯
        :return:
        """

        if step == 0:
            self.progress_bar.setVisible(False)
            self.status_bar_label_left.setText("等待执行")
        else:
            self.status_bar_label_left.setText(self.get_local_time())
            if self.progress_bar.isVisible() is False:
                self.progress_bar.setVisible(True)
            self.progress_bar.setValue(step)

    def print_status_bar(self, text: str = None, find_button_count: int = 0):
        """
        打印底部状态栏的日志
        :param find_button_count: 已经找到了几个按钮了
        :param text: 打印的日志
        :return:
        """

        self.status_bar_label_right.setText(f"一共识别了 {find_button_count} 轮")

    def print_status_track_bar(self, text: str = None, find_button_count: int = 0):
        """
        打印底部状态栏的日志
        :param find_button_count: 已经找到了几个按钮了
        :param text: 打印的日志
        :return:
        """
        if text is not None:
            self.status_bar_label_right.setText(text)
        else:
            self.status_bar_label_right.setText(f"一共执行了 {find_button_count} 轮")

    def check_handle_is_selected(self) -> list:
        """
        看看哪些窗口已经勾选了
        :return:
        """
        windows_list = []
        if self.check_box_windows_one.isChecked():
            windows_list.append(self.handle_dict["windows_1"])
        if self.check_box_windows_two.isChecked():
            windows_list.append(self.handle_dict["windows_2"])
        if self.check_box_windows_three.isChecked():
            windows_list.append(self.handle_dict["windows_3"])
        return windows_list

    def __update_ui_changed_execute_button_text_and_status(self, button_status: bool):
        """
        更新执行按钮的文字和状态
        :param button_status:
        :return:
        """
        self.status_bar_print.showMessage("")
        if button_status is True:
            self.execute_button_status_bool = True  # 已经开始执行了
            self.push_button_start_or_stop_execute.setText("结束执行")
            self.push_button_get_windows_handle.setEnabled(False)
            self.push_button_test_windows.setEnabled(False)
        else:
            self.execute_button_status_bool = False  # 结束循环，等待执行
            self.push_button_start_or_stop_execute.setText("开始执行")
            self.push_button_get_windows_handle.setEnabled(True)
            self.push_button_test_windows.setEnabled(True)

    def click_execute_button(self):
        """
        判断开始还是结束
        :return:
        """
        if self.execute_button_status_bool is False:
            """
            如果当前状态是False，表示接下来需要开始执行循环,开始发出开始命令，等待开始
            """
            self._execute_start()
        else:
            """
            如果当前状态是True，说明正在执行，接下来需要停止，开始发出结束命令，等待结束
            """
            self.__qth_single_stop_status()

    def __qth_single_stop_status(self):
        """
        点击结束执行按钮，给线程发出停止命令
        :return:
        """
        self.print_logs("已发出停止指令，请等待")
        # 如果当前是截图模式
        self.th_screen.stop_execute_init()
        # 如果当前团练授业模式
        self.th.stop_execute_init()
        # 键盘连按
        self.th_key_press_auto.stop_execute_init()

        # 世界竞拍
        self.th_market.stop_execute_init()
        # 押镖
        self.truck_task_func_switch(step=0)
        self.th_truck_task.set_close()
        # 进度条跑马灯
        self.th_progress_bar.stop_init()
        self.__update_ui_changed_execute_button_text_and_status(False)

    def _execute_start(self):
        """
        点击开始执行按钮
        :return:
        """
        windows_list = self.check_handle_is_selected()
        if len(windows_list) == 0:
            self.print_logs("请选择您需要执行的游戏窗口")
        else:
            self.is_debug = True if self.check_debug_mode.isChecked() else False
            start_log_string: str = "开始执行"
            if self.is_debug:
                start_log_string: str = "开始执行Debug模式(仅限团练授业)，详情请查看程序根目录生成的日志文件"
            self.print_logs(start_log_string, is_clear=True)
            if self.radio_button_school_dance.isChecked() or self.radio_button_party_dance.isChecked():
                """
                如果是团练/授业
                """
                if self.radio_button_school_dance.isChecked():
                    dance_type = "团练"
                else:
                    dance_type = "望辉洲"
                self.th.start_execute_init(windows_handle_list=windows_list,
                                           dance_type=dance_type,
                                           key_board_mouse_driver_type=self.keyboard_type,
                                           debug=self.is_debug)
                self.th.start()
                self.__update_ui_changed_execute_button_text_and_status(True)
                # 开始执行跑马灯效果
                self.th_progress_bar.start_init()
                self.th_progress_bar.start()

            elif self.radio_button_game_screen.isChecked():
                """
                如果是截图
                """
                self.th_screen.get_param(windows_handle_list=windows_list, pic_save_path="./")
                self.th_screen.start()
                self.__update_ui_changed_execute_button_text_and_status(True)
                # 开始执行跑马灯效果
                self.th_progress_bar.start_init()
                self.th_progress_bar.start()

            elif self.radio_button_key_auto.isChecked():
                """
                如果是键盘连点器
                """
                key_selected_str = self.list_widget.currentItem()
                if key_selected_str is not None:
                    key_selected_str = key_selected_str.text()
                    if len(windows_list) == 1:
                        self.th_key_press_auto.get_param(windows_handle=windows_list[0],
                                                         key_press_list=key_selected_str,
                                                         press_count=self.line_key_press_execute_sum.value(),
                                                         press_wait_time=self.line_key_press_wait_time.value())
                        self.th_key_press_auto.start()
                        self.__update_ui_changed_execute_button_text_and_status(True)
                        # 开始执行跑马灯效果
                        self.th_progress_bar.start_init()
                        self.th_progress_bar.start()

                    else:
                        self.print_logs("键盘连按功能暂时只支持1个窗口运行")
                else:
                    self.print_logs("请选择需要执行的键盘按钮")
            elif self.radio_button_truck_car_task.isChecked():
                """
                如果是押镖
                """
                if len(windows_list) == 1:

                    __truck_car_sum: int = int(self.line_max_truck_car_sum.value())

                    if self.th_truck_task.isRunning() is False:
                        self.th_truck_task.get_param(windows_list[0], int(__truck_car_sum))
                        self.th_truck_task.start()
                        self.__update_ui_changed_execute_button_text_and_status(True)
                        # 开始执行跑马灯效果
                        self.th_progress_bar.start_init()
                        self.th_progress_bar.start()
            elif self.radio_button_auction_market.isChecked():
                """
                如果是世界竞拍
                """
                res_dict = self.__market_check_goods_max_price()
                if len(res_dict) > 0:
                    if len(windows_list) == 1:
                        self.th_market.get_param(windows_list[0], res_dict)
                        self.th_market.start()

                        self.__update_ui_changed_execute_button_text_and_status(True)
                        # 开始执行跑马灯效果
                        self.th_progress_bar.start_init()
                        self.th_progress_bar.start()
            else:
                self.print_logs("还未选择需要执行的功能")

    def _th_execute_stop(self, execute_status: bool):
        """
        进程的停止状态
        :param execute_status:
        :return:
        """
        if execute_status is False:
            self.__qth_single_stop_status()

    def get_windows_handle(self):
        """
        获取游戏窗口数量
        :return:
        """
        handle_list = GetHandleList().get_windows_handle()
        self.handle_dict = {}
        # handle_list = getWindows().enum_window(0, "", "FxMain", 2)
        if 0 < len(handle_list) <= 3:
            self.push_button_test_windows.setEnabled(True)
            self.push_button_start_or_stop_execute.setEnabled(True)
            for index_handle in range(len(handle_list)):
                self.handle_dict["windows_" + str(index_handle + 1)] = str(handle_list[index_handle])
            self.print_logs("已检测到了 %d 个获取到的窗口" % len(self.handle_dict.keys()), is_clear=True)
        elif len(handle_list) > 4:
            self.print_logs("检测到 %d 个游戏窗口，请减少至3个再次重试" % len(handle_list), is_clear=True)
        else:
            self.print_logs("未发现游戏窗口，请登录游戏后再次重试", is_clear=True)
        self.set_check_box_by_game_windows_enable()

    def set_check_box_by_game_windows_enable(self):
        """
        将窗口handle设置到控件是否为启用
        :return:
        """
        windows_check_element = [self.check_box_windows_one, self.check_box_windows_two, self.check_box_windows_three]
        self.set_ui_load_windows_check_box_init()
        self.push_button_test_windows.setEnabled(False)
        self.push_button_start_or_stop_execute.setEnabled(False)
        if len(self.handle_dict.keys()) > 0:
            for index_key in range(len(self.handle_dict.keys())):
                windows_check_element[index_key].setEnabled(True)
            self.push_button_test_windows.setEnabled(True)
            self.push_button_start_or_stop_execute.setEnabled(True)

    def test_windows_handle(self):
        """
        检测游戏窗口.对当前活跃的游戏窗口进行检测
        :return:
        """

        handle_list = self.check_handle_is_selected()
        if len(handle_list) == 0:
            self.print_logs("请勾选需要测试的窗口", is_clear=True)
        else:
            self.print_logs("开始测试窗口", is_clear=True)
            for i in handle_list:
                for execute_num in range(5):
                    r = GetHandleList().activate_windows(i)
                    if r is False:
                        self.print_logs(f"{i} 激活失败，正在进行第{execute_num}次重试")
                        continue
                    else:
                        if self.keyboard_type == "ghost":

                            SetGhostBoards().click_press_and_release_by_key_name("K")
                        else:
                            getKeyBoardMouse().key_press_char("K")
                        self.print_logs("窗口(%s)已激活，并尝试按下了'K'按钮" % i)
                        break
                time.sleep(1)
                GetHandleList().set_allow_set_foreground_window()  # 取消置顶

    def key_press_even_add(self):
        """
        新增列表
        :return:
        """
        self.list_widget.addItem(QtWidgets.QListWidgetItem(f"请输入按钮"))

    def key_press_even_del(self):
        """
        删除
        :return:
        """
        if self.list_widget.selectedItems():
            item = self.list_widget.currentRow()
            self.list_widget.takeItem(item)
        else:
            self.show_dialog("请选择需要删除的记录")

    def key_press_even_save(self):
        """
        保存按钮
        :return:
        """

        def get_all_items(list_widget):
            items = []
            for i in range(list_widget.count()):
                item_text = list_widget.item(i)
                items.append(item_text.text())
            return items

        key_list: list = []
        all_items = get_all_items(self.list_widget)

        if all_items is not None:
            for item in all_items:
                key_word: str = str(item)
                if key_word != "请输入按钮":
                    key_list.append(key_word)
            if len(key_list) > 0:

                # 判断一下输入的 按钮我有没有定义
                res_list: list = check_ghost_code_is_def(key_list)
                if len(res_list) == 0:
                    self.file_config.save_key_even_code_auto_list(key_list)
                    self.show_dialog("保存成功")
                else:
                    error_key: str = " 和 ".join(res_list)
                    self.show_dialog(f"按钮 {error_key} 暂不支持,请更换按钮")
            else:
                self.show_dialog("请先设置按钮再保存")
        else:
            self.show_dialog("没有需要保存的按钮")
        self.on_top_level_changed()

    def on_top_level_changed(self):
        """
        加载一下配置文件
        :return:
        """
        self.list_widget.clear()
        if self.widget_dock.isTopLevel():
            res_file: str = self.file_config.get_key_even_code_auto_list()
            res_list: list = list(eval(res_file))
            for res in res_list:
                self.list_widget.addItem(res)

    def truck_task_func_switch(self, step: int):
        """
        切换方法
        :param step: 1 是扫描打怪。
                     2 是重新查找 镖车并开车,
                     3: 打怪中，暂时查找车辆，
                     4：打怪结束，重新查找车辆
        """
        # 前面已经做了判断，只能有一个窗口执行，所以这里直接获取
        windows_handle = self.check_handle_is_selected()[0]
        if step == 1:
            # self.print_logs("开启线程:等待劫镖NPC...")
            if self.th_truck_fight_monster.isRunning() is False:
                self.th_truck_fight_monster.get_param(windows_handle, True)
                self.th_truck_fight_monster.start()
        elif step == 2:
            # self.print_logs("开启线程:查找镖车...")
            pass
        elif step == 3:
            # self.print_logs("开启线程:保持镖车在屏幕中心...")
            pass
        elif step == 4:
            # self.print_logs("关闭线程:保持镖车在屏幕中心...")
            pass
        elif step == 5:
            # self.print_logs("关闭线程:查找镖车...")
            pass
        elif step == 0:
            """
            如果是其他值，一般是 0，就表示结束
            """
            # self.print_logs("本次押镖结束,即将关闭所有线程")
            self.th_truck_fight_monster.get_param(windows_handle, False)  # 停止打怪

    def get_screen_market_goods_list(self):
        """
        获取当前游戏窗口的竞拍物品
        """
        handle_list = self.check_handle_is_selected()
        if len(handle_list) != 1:
            self.print_logs("请勾选需要的窗口(只支持1个窗口)", is_clear=True)
        else:
            __res: dict = FindAuctionMarket().find_goods(WindowsCapture().capture(handle_list[0]).pic_content)
            __goods_name_list: list = []
            if len(__res) > 0:
                for __good_line in __res:
                    __goods_name = __res[__good_line]["goods_name"]
                    __goods_name_list.append(__goods_name)
            if len(__goods_name_list) == 0:
                self.print_logs("游戏窗口未检测到世界竞拍列表", is_clear=True)
                return False
            self.set_market_goods_list(__goods_name_list)

    def __market_check_goods_max_price(self):
        """
        检测是否填写了最大价格
        """
        _goods_price_list: list = []
        for row in range(self.list_widget_market.rowCount()):
            __goods_name_obj: QtWidgets.QLabel = self.list_widget_market.cellWidget(row, 0)
            __goods_max_price_obj: QtWidgets.QLineEdit = self.list_widget_market.cellWidget(row, 1)

            __goods_name, __goods_max_price = "", ""

            __goods_name: str = __goods_name_obj.text()
            __goods_max_price: str = __goods_max_price_obj.text()
            if __goods_max_price != "":
                _goods_price_list.append({__goods_name: __goods_max_price})
                continue
            self.print_logs("还有物品没有设置价格")
            return None
        return _goods_price_list

    def __load_skill_table(self):
        _skill_obj: dict = self.file_config.get_skill_group_list().get("打怪套路")  # 当前正在使用的技能组

        self._skill_table.clear()
        self._skill_table.setHorizontalHeaderLabels(['技能名', '技能冷却(秒)', '释放时间(秒)', '释放优先级', '键盘Key'])

        row_index: int = 0
        for skill_name in _skill_obj:
            if self._skill_table.rowCount() < row_index + 1:
                self._skill_table.insertRow(self._skill_table.rowCount())

            # 技能名称
            item = QtWidgets.QTableWidgetItem(str(skill_name).format(row_index, 1))
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            self._skill_table.setItem(row_index, 0, QtWidgets.QTableWidgetItem(item))

            _skill: dict = _skill_obj.get(skill_name)
            # 技能CD
            if _skill.get("CD") is not None:
                column_index: int = 1
                item = QtWidgets.QTableWidgetItem(str(_skill.get("CD")).format(row_index, column_index))
                item.setTextAlignment(QtCore.Qt.AlignCenter)
                self._skill_table.setItem(row_index, column_index, QtWidgets.QTableWidgetItem(item))

            # 技能释放时间
            if _skill.get("active_cd") is not None:
                column_index: int = 2
                item = QtWidgets.QTableWidgetItem(str(_skill.get("active_cd")).format(row_index, column_index))
                item.setTextAlignment(QtCore.Qt.AlignCenter)
                self._skill_table.setItem(row_index, column_index, QtWidgets.QTableWidgetItem(item))
            # 技能释放优先级
            if _skill.get("level") is not None:
                column_index: int = 3
                item = QtWidgets.QTableWidgetItem(str(_skill.get("level")).format(row_index, column_index))
                item.setTextAlignment(QtCore.Qt.AlignCenter)
                self._skill_table.setItem(row_index, column_index, QtWidgets.QTableWidgetItem(item))
            # 技能释放优先级
            if _skill.get("key") is not None:
                column_index: int = 4
                item = QtWidgets.QTableWidgetItem(str(_skill.get("key")).format(row_index, column_index))
                item.setTextAlignment(QtCore.Qt.AlignCenter)
                self._skill_table.setItem(row_index, column_index, QtWidgets.QTableWidgetItem(item))
            row_index += 1

    def open_skill_table(self):
        if self.dialog_skill_table.isVisible() is False:
            self.__load_skill_table()
            self.dialog_skill_table.setVisible(True)

    def save_skill_table(self):
        """
        保存技能设置
        {
  "打怪套路": {
    "梵心降魔": {"CD": 2, "active_cd": 1, "level": 2, "key": "Q"},
    "三阳开泰": {"CD": 6, "active_cd": 1.8, "level": 1, "key": "R"},
    "五气呈祥": {"CD": 2, "active_cd": 1, "level": 2, "key": "1"},
    "罡风推云": {"CD": 6, "active_cd": 1, "level": 3, "key": "3"},
    "气贯长虹": {"CD": 8, "active_cd": 1, "level": 2, "key": "2"}
  }
}
        """
        skill_dict_json: dict = {}
        for row in range(self._skill_table.rowCount()):

            _skill_name: str = ""
            _skill_cd: int = 0
            _skill_active_cd: float = 0.0
            _skill_level: int = 0
            _skill_key: str = ""

            for cum in range(self._skill_table.columnCount()):
                __content = self._skill_table.item(row, cum).text()
                if cum == 0:
                    _skill_name = __content
                elif cum == 1:
                    _skill_cd = int(__content)
                elif cum == 2:
                    _skill_active_cd = float(__content)
                elif cum == 3:
                    _skill_level = int(__content)
                elif cum == 4:
                    _skill_key = __content
            skill_dict_json[str(_skill_name)] = {"CD": _skill_cd, "active_cd": _skill_active_cd, "level": _skill_level,
                                                 "key": _skill_key}
        self.file_config.update_skill_group_list(_skill_dict=skill_dict_json)
        self.show_dialog("保存成功,请重启脚本")
