import ctypes
import os
import sys

from PySide6 import QtWidgets, QtCore, QtGui
from PySide6.QtCore import Qt, QObject, QEvent, QSettings
from PySide6.QtGui import QIcon, QAction
from PySide6.QtWidgets import QApplication, QListWidget, QMessageBox


class ListWidgetItemEventFilter(QObject):
    def __init__(self, parent):
        super().__init__(parent)
        self.list_widget: QListWidget = parent
        self.event_key_str_list: list = []  # 本次所有按下的按键
        self.event_key_sum: int = 0  # 按下的组合键数量

    def eventFilter(self, watched: QObject, event: QEvent) -> bool:
        if event.type() == QEvent.KeyPress:
            """
            如果是按钮按下
            """
            key_text = event.text()
            if event.modifiers():
                key_text = event.keyCombination().key().name.decode(encoding="utf-8")
            if key_text not in self.event_key_str_list:
                """
                如果本次按下的键是没有被按过的，就加入队列
                """
                self.event_key_str_list.append(key_text)
                self.event_key_sum += 1
                # print(f"键盘按下了 {key_text} {event.key()} 当前按钮数量{self.event_key_sum}")

        elif event.type() == QEvent.KeyRelease:
            """
            如果是按钮弹起
            """
            self.event_key_sum -= 1
            # print(f"键盘松开了一个键_当前按钮数量{self.event_key_sum}")
            if self.event_key_sum == 0:
                """
                如果所有的按钮都弹起了，那么就说明已经输入完毕
                """
                if self.list_widget.selectedItems():
                    item = self.list_widget.selectedItems()[0]
                    event_key_str = "+".join(self.event_key_str_list)
                    item.setText(event_key_str.upper())
                    self.event_key_str_list = []
            elif self.event_key_sum < 0:
                self.event_key_sum = 0
        return super().eventFilter(watched, event)


class MainGui(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()

        self.setFixedSize(280, 420)
        # self.setWindowTitle("蜗牛跳舞小助手")
        # 加载任务栏和窗口左上角图标
        self.setWindowIcon(QIcon("./_internal/Resources/logo/logo.ico"))
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("myappid")

        """
        加载事件筛选器
        """
        self.list_widget = QtWidgets.QListWidget()
        event_filter = ListWidgetItemEventFilter(self.list_widget)
        self.list_widget.installEventFilter(event_filter)

        """
        顶部菜单栏
        """
        menu_bar = self.menuBar()

        file_menu = QtWidgets.QMenu("&配置", self)
        about_menu = QtWidgets.QMenu("&帮助", self)

        menu_bar.addMenu(file_menu)
        menu_bar.addMenu(about_menu)

        action_open_config_file = QtGui.QAction("打开资源文件目录", self)
        file_menu.addAction(action_open_config_file)
        action_open_config_file.triggered.connect(self.open_config_file)

        action_edit_config_file = QtGui.QAction("修改配置", self)
        file_menu.addAction(action_edit_config_file)
        action_edit_config_file.triggered.connect(self.edit_config_file)

        action_open_url = QtGui.QAction("访问项目github", self)
        about_menu.addAction(action_open_url)
        action_open_url.triggered.connect(self.open_url_project)

        action_open_url_get_fore_ground_window_fail = QtGui.QAction("修复窗户激活失败", self)
        about_menu.addAction(action_open_url_get_fore_ground_window_fail)
        action_open_url_get_fore_ground_window_fail.triggered.connect(self.open_url_get_fore_ground_window_fail)

        """
        底部状态栏显示区域
        """
        self.status_bar_print = QtWidgets.QStatusBar(self)
        self.setStatusBar(self.status_bar_print)

        # 左侧区域
        # 给状态栏显示文字用的
        self.status_bar_label_left = QtWidgets.QLabel()
        # 状态栏本身显示的信息 第二个参数是信息停留的时间，单位是毫秒，默认是0（0表示在下一个操作来临前一直显示）
        # 在状态栏左侧新增显示控件
        self.status_bar_print.addWidget(self.status_bar_label_left, stretch=1)
        # 加载一个进度条
        self.progress_bar = QtWidgets.QProgressBar(self)
        self.progress_bar.setInvertedAppearance(False)  # 进度条的走向
        self.progress_bar.setOrientation(QtCore.Qt.Orientation.Horizontal)  # 进度条的方向
        # 出现跑马灯的效果
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(0)
        self.progress_bar.setFixedHeight(15)
        self.progress_bar.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.status_bar_print.addWidget(self.progress_bar, stretch=3)

        # 右侧区域
        self.status_bar_label_right = QtWidgets.QLabel()
        self.status_bar_label_right.setText("一共识别了 0 轮")
        self.status_bar_label_right.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.status_bar_print.addWidget(self.status_bar_label_right, stretch=1)

        self.status_bar_print.setContentsMargins(8, 0, 0, 0)

        """
        选择类型
        """
        self.group_box_functional_area = QtWidgets.QGroupBox(self)  # 功能区
        self.group_box_functional_area.setGeometry(QtCore.QRect(10, 25, 260, 70))
        self.group_box_functional_area.setTitle("选择功能")

        self.radio_button_school_dance = QtWidgets.QRadioButton()
        self.radio_button_school_dance.setText("团练授业")
        # 隐士/势力/修罗刀
        self.radio_button_party_dance = QtWidgets.QRadioButton()
        self.radio_button_party_dance.setText("隐士势力")
        # 游戏截图
        self.radio_button_game_screen = QtWidgets.QRadioButton()
        self.radio_button_game_screen.setText("游戏截图")
        # 按键宏
        self.radio_button_key_auto = QtWidgets.QRadioButton()
        self.radio_button_key_auto.setText("键盘连按")

        """
        增加一下布局框
        """
        # 一个网格布局
        self.gridLayout_group_box_functional_area = QtWidgets.QGridLayout(self.group_box_functional_area)
        self.gridLayout_group_box_functional_area.setContentsMargins(0, 0, 0, 5)
        self.gridLayout_group_box_functional_area.addWidget(self.radio_button_school_dance, 0, 0, QtCore.Qt.AlignRight)
        self.gridLayout_group_box_functional_area.addWidget(self.radio_button_party_dance, 0, 1, QtCore.Qt.AlignCenter)
        self.gridLayout_group_box_functional_area.addWidget(self.radio_button_game_screen, 0, 2, QtCore.Qt.AlignCenter)
        self.gridLayout_group_box_functional_area.addWidget(self.radio_button_key_auto, 1, 0, QtCore.Qt.AlignRight)

        self.setLayout(self.gridLayout_group_box_functional_area)

        """
        选择游戏窗口与执行
        """
        self.group_box_get_windows = QtWidgets.QGroupBox(self)
        self.group_box_get_windows.setGeometry(QtCore.QRect(10, 100, 260, 70))
        self.group_box_get_windows.setTitle("选择游戏窗口")

        # 获取窗口按钮
        self.push_button_get_windows_handle = QtWidgets.QPushButton()
        self.push_button_get_windows_handle.setText("获取窗口")
        # 测试窗口
        self.push_button_test_windows = QtWidgets.QPushButton(self.group_box_get_windows)
        self.push_button_test_windows.setText("测试窗口")
        self.push_button_test_windows.setEnabled(False)
        # 开始执行/停止执行
        self.push_button_start_or_stop_execute = QtWidgets.QPushButton(self.group_box_get_windows)
        self.push_button_start_or_stop_execute.setText("开始执行")
        self.push_button_start_or_stop_execute.setEnabled(False)

        # 加载一个横向的布局
        self.layout_group_box_get_windows = QtWidgets.QHBoxLayout(self.group_box_get_windows)
        self.layout_group_box_get_windows.addWidget(self.push_button_get_windows_handle)
        self.layout_group_box_get_windows.addWidget(self.push_button_test_windows)
        self.layout_group_box_get_windows.addWidget(self.push_button_start_or_stop_execute)

        self.setLayout(self.layout_group_box_get_windows)

        # 获取到的游戏窗口要如何加载
        self.group_box_select_windows = QtWidgets.QGroupBox(self)
        self.group_box_select_windows.setGeometry(QtCore.QRect(10, 170, 260, 40))

        # 窗口A/B/C
        self.check_box_windows_one = QtWidgets.QCheckBox()
        self.check_box_windows_two = QtWidgets.QCheckBox()
        self.check_box_windows_three = QtWidgets.QCheckBox()

        self.check_box_windows_one.setText("窗口1")
        self.check_box_windows_two.setText("窗口2")
        self.check_box_windows_three.setText("窗口3")
        self.check_box_windows_one.setEnabled(False)
        self.check_box_windows_two.setEnabled(False)
        self.check_box_windows_three.setEnabled(False)

        # 加载一个横向的布局
        self.layout_group_box_select_windows = QtWidgets.QHBoxLayout(self.group_box_select_windows)
        self.layout_group_box_select_windows.addStretch(1)
        self.layout_group_box_select_windows.addWidget(self.check_box_windows_one)
        self.layout_group_box_select_windows.addWidget(self.check_box_windows_two)
        self.layout_group_box_select_windows.addWidget(self.check_box_windows_three)
        self.layout_group_box_select_windows.addStretch(1)
        self.setLayout(self.layout_group_box_select_windows)

        """
        日志打印区      
        """
        self.text_browser_print_log = QtWidgets.QTextBrowser(self)
        self.text_browser_print_log.setGeometry(QtCore.QRect(10, 220, 260, 178))

        """
        按键连按
        """
        widget_key_press_auto = QtWidgets.QWidget()
        # 最大随机等待事件
        self.line_key_press_wait_time = QtWidgets.QDoubleSpinBox(widget_key_press_auto)
        self.line_key_press_wait_time.setValue(1.5)  # 双精度
        self.line_key_press_wait_time.setRange(0.5, 99)  # 双精度
        self.line_key_press_wait_time.setSuffix("秒")  # 单位

        self.line_key_press_execute_sum = QtWidgets.QSpinBox(widget_key_press_auto)
        self.line_key_press_execute_sum.setValue(10)
        self.line_key_press_execute_sum.setRange(1, 999999)
        self.line_key_press_execute_sum.setSuffix("次")

        lay_out_input = QtWidgets.QHBoxLayout()
        lay_out_input.addWidget(self.line_key_press_execute_sum)
        lay_out_input.addWidget(self.line_key_press_wait_time)

        self.push_button_save_key_press_add = QtWidgets.QPushButton("新增", widget_key_press_auto)
        self.push_button_save_key_press_delete = QtWidgets.QPushButton("删除", widget_key_press_auto)
        self.push_button_save_key_press_save = QtWidgets.QPushButton("保存", widget_key_press_auto)

        layout_input = QtWidgets.QGridLayout(widget_key_press_auto)
        layout_input.addLayout(lay_out_input, 0, 0, 1, 1)
        layout_input.addWidget(self.list_widget, 1, 0, 3, 1)
        layout_input.addWidget(self.push_button_save_key_press_add, 1, 1)
        layout_input.addWidget(self.push_button_save_key_press_delete, 2, 1)
        layout_input.addWidget(self.push_button_save_key_press_save, 3, 1)
        layout_input.setAlignment(QtCore.Qt.AlignHCenter)

        self.widget_dock = QtWidgets.QDockWidget("键盘按钮设置",self)
        self.widget_dock.setWidget(widget_key_press_auto)
        self.widget_dock.setFloating(True)  # 独立于主窗口之外
        self.addDockWidget(QtCore.Qt.DockWidgetArea.RightDockWidgetArea, self.widget_dock)
        self.widget_dock.setVisible(False)
        self.widget_dock.setFeatures(QtWidgets.QDockWidget.DockWidgetClosable)  # dockWidget窗口禁止回到主窗口

        """
        设置配置文件窗口
        """
        widget_setting = QtWidgets.QWidget()
        self.label_dance_threshold = QtWidgets.QLabel("团练授业阈值", widget_setting)
        self.line_dance_threshold = QtWidgets.QDoubleSpinBox(widget_setting)
        self.line_dance_threshold.setRange(0.01, 1.00)

        self.label_whz_dance_threshold = QtWidgets.QLabel("势力修炼阈值", widget_setting)
        self.line_whz_dance_threshold = QtWidgets.QDoubleSpinBox(widget_setting)
        self.line_whz_dance_threshold.setRange(0.01, 1.00)

        self.check_debug_mode = QtWidgets.QCheckBox("Debug", widget_setting)
        self.push_button_save_setting = QtWidgets.QPushButton("保存设置", widget_setting)

        layout_setting = QtWidgets.QGridLayout(widget_setting)
        layout_setting.addWidget(self.label_dance_threshold, 0, 0)
        layout_setting.addWidget(self.line_dance_threshold, 0, 1)
        layout_setting.addWidget(self.label_whz_dance_threshold, 1, 0)
        layout_setting.addWidget(self.line_whz_dance_threshold, 1, 1)
        layout_setting.addWidget(self.check_debug_mode, 2, 0)
        layout_setting.addWidget(self.push_button_save_setting, 2, 1)

        self.widget_dock_setting = QtWidgets.QDockWidget("配置信息", self)
        self.widget_dock_setting.setWidget(widget_setting)
        self.widget_dock_setting.setFloating(True)  # 独立于主窗口之外
        self.addDockWidget(QtCore.Qt.DockWidgetArea.RightDockWidgetArea, self.widget_dock_setting)
        self.widget_dock_setting.setVisible(False)
        self.widget_dock_setting.setFeatures(QtWidgets.QDockWidget.DockWidgetClosable)  # dockWidget窗口禁止回到主窗口

    def open_config_file(self):
        """
        打开配置文件
        :return:
        """
        config_file: str = '.\\_internal\\Resources\\'
        if not os.path.exists(config_file):  # 如果主目录+小时+分钟这个文件路径不存在的话
            config_file = ".\\DeskPageV2\\Resources\\"
        QtWidgets.QFileDialog.getOpenFileName(self, "资源文件", config_file,
                                              "Text Files (*.yaml;*.bat;*.png;*.ico;*.dll)")

    def edit_config_file(self):
        if self.widget_dock_setting.isVisible() is False:
            self.widget_dock_setting.setVisible(True)

    @staticmethod
    def open_url_get_fore_ground_window_fail(self):
        """
        激活窗口失败
        :param self:
        :return:
        """
        QtGui.QDesktopServices.openUrl(QtCore.QUrl("https://blog.csdn.net/qq_26013403/article/details/129122971"))

    @staticmethod
    def open_url_project():
        """
        打开网页
        :return:
        """
        QtGui.QDesktopServices.openUrl(QtCore.QUrl("https://github.com/moonlessdark/JiuYinDance"))

    def set_ui_load_windows_check_box_init(self):
        """
        选择按钮初始化，全部禁用
        :return:
        """
        self.check_box_windows_one.setCheckState(QtCore.Qt.CheckState.Unchecked)
        self.check_box_windows_one.setEnabled(False)
        self.check_box_windows_two.setCheckState(QtCore.Qt.CheckState.Unchecked)
        self.check_box_windows_two.setEnabled(False)
        self.check_box_windows_three.setCheckState(QtCore.Qt.CheckState.Unchecked)
        self.check_box_windows_three.setEnabled(False)

    def set_ui_load_windows_check_box_by_single(self):
        """
        只能选择一个窗口，用在游戏截图这个功能
        :return:
        """
        if self.check_box_windows_one.isChecked():
            self.check_box_windows_two.setCheckState(QtCore.Qt.CheckState.Unchecked)
            self.check_box_windows_two.setEnabled(False)
            self.check_box_windows_three.setCheckState(QtCore.Qt.CheckState.Unchecked)
            self.check_box_windows_three.setEnabled(False)
        elif self.check_box_windows_two.isChecked():
            self.check_box_windows_one.setCheckState(QtCore.Qt.CheckState.Unchecked)
            self.check_box_windows_one.setEnabled(False)
            self.check_box_windows_three.setCheckState(QtCore.Qt.CheckState.Unchecked)
            self.check_box_windows_three.setEnabled(False)
        elif self.check_box_windows_three.isChecked():
            self.check_box_windows_one.setCheckState(QtCore.Qt.CheckState.Unchecked)
            self.check_box_windows_one.setEnabled(False)
            self.check_box_windows_two.setCheckState(QtCore.Qt.CheckState.Unchecked)
            self.check_box_windows_two.setEnabled(False)

    def set_ui_key_press_auto(self):
        """
        设置dockWidget是否显示
        :return:
        """
        if self.radio_button_key_auto.isChecked():
            self.widget_dock.setVisible(True)
        else:
            self.widget_dock.setVisible(False)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_gui = MainGui()
    main_gui.show()
    sys.exit(app.exec_())
