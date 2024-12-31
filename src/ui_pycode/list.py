# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'list.ui'
#
# Created by: PyQt5 UI code generator 5.15.11
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_List(object):
    def setupUi(self, List):
        List.setObjectName("List")
        List.resize(380, 602)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(List.sizePolicy().hasHeightForWidth())
        List.setSizePolicy(sizePolicy)
        List.setMinimumSize(QtCore.QSize(380, 600))
        List.setMaximumSize(QtCore.QSize(380, 16777215))
        List.setSizeIncrement(QtCore.QSize(0, 0))
        List.setBaseSize(QtCore.QSize(0, 0))
        List.setWindowTitle("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/favicon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        List.setWindowIcon(icon)
        List.setStyleSheet("background-color:#f4f9fa;")
        self.verticalLayout = QtWidgets.QVBoxLayout(List)
        self.verticalLayout.setObjectName("verticalLayout")
        self.widget_list = QtWidgets.QWidget(List)
        font = QtGui.QFont()
        font.setFamily("FreeSans")
        font.setPointSize(12)
        self.widget_list.setFont(font)
        self.widget_list.setFocusPolicy(QtCore.Qt.NoFocus)
        self.widget_list.setStyleSheet("")
        self.widget_list.setObjectName("widget_list")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.widget_list)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.label_list_type = QtWidgets.QLabel(self.widget_list)
        font = QtGui.QFont()
        font.setFamily("Sans Serif")
        font.setPointSize(6)
        font.setBold(False)
        font.setWeight(50)
        self.label_list_type.setFont(font)
        self.label_list_type.setFocusPolicy(QtCore.Qt.NoFocus)
        self.label_list_type.setStyleSheet("color:transparent;")
        self.label_list_type.setText("")
        self.label_list_type.setObjectName("label_list_type")
        self.verticalLayout_4.addWidget(self.label_list_type)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setContentsMargins(0, 8, -1, 8)
        self.horizontalLayout_3.setSpacing(10)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.button_new = QtWidgets.QPushButton(self.widget_list)
        self.button_new.setMaximumSize(QtCore.QSize(125, 16777215))
        font = QtGui.QFont()
        font.setFamily("Sans Serif")
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.button_new.setFont(font)
        self.button_new.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.button_new.setFocusPolicy(QtCore.Qt.NoFocus)
        self.button_new.setStyleSheet("QPushButton{\n"
"    border:1px solid #006EFF;\n"
"    border-radius:8px;\n"
"    height:25px;\n"
"    padding:0 5px 0 5px;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color:rgb(216, 216, 216); \n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: white; \n"
"}\n"
"\n"
"")
        self.button_new.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/icons/plus_blue.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.button_new.setIcon(icon1)
        self.button_new.setIconSize(QtCore.QSize(20, 20))
        self.button_new.setCheckable(True)
        self.button_new.setAutoExclusive(True)
        self.button_new.setObjectName("button_new")
        self.horizontalLayout_3.addWidget(self.button_new)
        self.input_search = QtWidgets.QLineEdit(self.widget_list)
        self.input_search.setMinimumSize(QtCore.QSize(250, 0))
        self.input_search.setMaximumSize(QtCore.QSize(400, 16777215))
        font = QtGui.QFont()
        font.setFamily("Sans Serif")
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.input_search.setFont(font)
        self.input_search.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.input_search.setStyleSheet("border:1px solid #006EFF;\n"
"background-color: rgb(255, 255, 255);\n"
"border-radius:6px;\n"
"height:25px\n"
"")
        self.input_search.setMaxLength(100)
        self.input_search.setClearButtonEnabled(True)
        self.input_search.setObjectName("input_search")
        self.horizontalLayout_3.addWidget(self.input_search)
        spacerItem = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem)
        self.verticalLayout_4.addLayout(self.horizontalLayout_3)
        self.table_list = QtWidgets.QTableWidget(self.widget_list)
        self.table_list.setBaseSize(QtCore.QSize(640, 600))
        font = QtGui.QFont()
        font.setFamily("Sans Serif")
        font.setPointSize(9)
        font.setBold(False)
        font.setWeight(50)
        self.table_list.setFont(font)
        self.table_list.viewport().setProperty("cursor", QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.table_list.setFocusPolicy(QtCore.Qt.NoFocus)
        self.table_list.setStyleSheet("QHeaderView::section{\n"
"    background-color:#006EFF;\n"
"    color:white;\n"
"    border:1px solid white;\n"
"}\n"
"\n"
"QTableWidget{\n"
"    background-color:#f4f9fa;\n"
"}\n"
"\n"
"QTableWidget::item {\n"
"    background-color:rgb(230, 234, 255);\n"
"    border:4px solid #f4f9fa;\n"
"    border-right:0px;\n"
"    border-left:0px;\n"
"    border-bottom:0px;\n"
"}\n"
"\n"
"QTableWidget::item:selected {\n"
"    background-color: #006EFF;\n"
"    color: white;\n"
"}")
        self.table_list.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.table_list.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.table_list.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.table_list.setTabKeyNavigation(False)
        self.table_list.setProperty("showDropIndicator", False)
        self.table_list.setDragDropOverwriteMode(False)
        self.table_list.setDefaultDropAction(QtCore.Qt.IgnoreAction)
        self.table_list.setAlternatingRowColors(True)
        self.table_list.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.table_list.setTextElideMode(QtCore.Qt.ElideRight)
        self.table_list.setShowGrid(False)
        self.table_list.setGridStyle(QtCore.Qt.NoPen)
        self.table_list.setRowCount(0)
        self.table_list.setObjectName("table_list")
        self.table_list.setColumnCount(2)
        item = QtWidgets.QTableWidgetItem()
        self.table_list.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.table_list.setHorizontalHeaderItem(1, item)
        self.table_list.horizontalHeader().setDefaultSectionSize(340)
        self.table_list.horizontalHeader().setMinimumSectionSize(31)
        self.table_list.verticalHeader().setVisible(False)
        self.verticalLayout_4.addWidget(self.table_list)
        spacerItem1 = QtWidgets.QSpacerItem(20, 10, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout_4.addItem(spacerItem1)
        self.line_5 = QtWidgets.QFrame(self.widget_list)
        font = QtGui.QFont()
        font.setFamily("FreeSans")
        font.setPointSize(12)
        self.line_5.setFont(font)
        self.line_5.setFocusPolicy(QtCore.Qt.NoFocus)
        self.line_5.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_5.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_5.setObjectName("line_5")
        self.verticalLayout_4.addWidget(self.line_5)
        spacerItem2 = QtWidgets.QSpacerItem(20, 10, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout_4.addItem(spacerItem2)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setSpacing(15)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.button_close = QtWidgets.QPushButton(self.widget_list)
        self.button_close.setMaximumSize(QtCore.QSize(125, 16777215))
        font = QtGui.QFont()
        font.setFamily("Sans Serif")
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.button_close.setFont(font)
        self.button_close.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.button_close.setFocusPolicy(QtCore.Qt.NoFocus)
        self.button_close.setStyleSheet("QPushButton{\n"
"    color:#006EFF;\n"
"    height:30px;\n"
"    padding:0 5px 0 5px;\n"
"    border:1px solid #006EFF;\n"
"    border-radius:8px;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color:rgb(216, 216, 216); \n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: white; \n"
"}")
        self.button_close.setIconSize(QtCore.QSize(20, 20))
        self.button_close.setCheckable(False)
        self.button_close.setAutoExclusive(False)
        self.button_close.setObjectName("button_close")
        self.horizontalLayout_5.addWidget(self.button_close)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem3)
        self.verticalLayout_4.addLayout(self.horizontalLayout_5)
        self.verticalLayout.addWidget(self.widget_list)

        self.retranslateUi(List)
        QtCore.QMetaObject.connectSlotsByName(List)

    def retranslateUi(self, List):
        _translate = QtCore.QCoreApplication.translate
        self.button_new.setToolTip(_translate("List", "Ctrl+N"))
        self.button_new.setShortcut(_translate("List", "Ctrl+N"))
        self.input_search.setToolTip(_translate("List", "Axtarış üçün daxil edin"))
        self.input_search.setPlaceholderText(_translate("List", "axtar..."))
        self.button_close.setToolTip(_translate("List", "Esc"))
        self.button_close.setText(_translate("List", "Bağla"))
        self.button_close.setShortcut(_translate("List", "Esc"))
import resources_rc