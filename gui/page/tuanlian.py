from PyQt5 import QtCore, QtWidgets, QtGui


class Ui_main_page_gui(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()
        self.setupUi()

    def setupUi(self):
        self.setObjectName("Form")
        self.resize(260, 400)
        self.groupBox = QtWidgets.QGroupBox(self)
        self.groupBox.setGeometry(QtCore.QRect(10, 10, 241, 51))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(9)
        self.groupBox.setFont(font)
        self.groupBox.setObjectName("groupBox")
        self.execute_button = QtWidgets.QPushButton(self.groupBox)
        self.execute_button.setGeometry(QtCore.QRect(170, 20, 60, 20))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.execute_button.setFont(font)
        self.execute_button.setObjectName("execute_button")
        self.type_select_button = QtWidgets.QComboBox(self.groupBox)
        self.type_select_button.setGeometry(QtCore.QRect(10, 20, 60, 20))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.type_select_button.setFont(font)
        self.type_select_button.setObjectName("type_select_button")
        self.type_select_button.addItem("")
        self.type_select_button.addItem("")
        self.select_windows_button = QtWidgets.QPushButton(self.groupBox)
        self.select_windows_button.setGeometry(QtCore.QRect(90, 20, 60, 20))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.select_windows_button.setFont(font)
        self.select_windows_button.setObjectName("select_windows_button")
        self.groupBox_2 = QtWidgets.QGroupBox(self)
        self.groupBox_2.setGeometry(QtCore.QRect(10, 70, 241, 41))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(9)
        self.groupBox_2.setFont(font)
        self.groupBox_2.setObjectName("groupBox_2")
        self.widget = QtWidgets.QWidget(self.groupBox_2)
        self.widget.setGeometry(QtCore.QRect(30, 10, 201, 31))
        self.widget.setObjectName("widget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.windows_1_check = QtWidgets.QCheckBox(self.widget)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(8)
        self.windows_1_check.setFont(font)
        self.windows_1_check.setObjectName("windows_1_check")
        self.horizontalLayout.addWidget(self.windows_1_check)
        self.windows_2_check = QtWidgets.QCheckBox(self.widget)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(8)
        self.windows_2_check.setFont(font)
        self.windows_2_check.setObjectName("windows_2_check")
        self.horizontalLayout.addWidget(self.windows_2_check)
        self.windows_3_check = QtWidgets.QCheckBox(self.widget)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(8)
        self.windows_3_check.setFont(font)
        self.windows_3_check.setObjectName("windows_3_check")
        self.horizontalLayout.addWidget(self.windows_3_check)
        self.groupBox_3 = QtWidgets.QGroupBox(self)
        self.groupBox_3.setGeometry(QtCore.QRect(10, 120, 241, 271))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(9)
        self.groupBox_3.setFont(font)
        self.groupBox_3.setObjectName("groupBox_3")
        self.log_textBrowser = QtWidgets.QTextBrowser(self.groupBox_3)
        self.log_textBrowser.setGeometry(QtCore.QRect(10, 20, 221, 241))
        self.log_textBrowser.setObjectName("log_textBrowser")

        self.setWindowTitle("自动团练Plus多开版")
        self.groupBox.setTitle("设置")
        self.execute_button.setText("开始执行")
        self.type_select_button.setItemText(0, "团练")
        self.type_select_button.setItemText(1, "授业")
        self.select_windows_button.setText("获取窗口")
        self.groupBox_2.setTitle("窗口列表")
        self.windows_1_check.setText("1号窗")
        self.windows_2_check.setText("2号窗")
        self.windows_3_check.setText("3号窗")
        self.groupBox_3.setTitle("日志")

        self.windows_3_check.setEnabled(False)
        self.windows_2_check.setEnabled(False)
        self.windows_1_check.setEnabled(False)
        self.execute_button.setEnabled(False)