# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'payment.ui'
#
# Created by: PyQt5 UI code generator 5.15.11
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Payment(object):
    def setupUi(self, Payment):
        Payment.setObjectName("Payment")
        Payment.resize(300, 450)
        Payment.setMaximumSize(QtCore.QSize(300, 450))
        Payment.setWindowTitle("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/favicon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Payment.setWindowIcon(icon)
        Payment.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(Payment)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.widget_payment = QtWidgets.QWidget(Payment)
        font = QtGui.QFont()
        font.setFamily("Sans Serif")
        font.setBold(False)
        font.setWeight(50)
        self.widget_payment.setFont(font)
        self.widget_payment.setFocusPolicy(QtCore.Qt.NoFocus)
        self.widget_payment.setStyleSheet("QDateEdit {\n"
"    border:1px solid #006EFF;\n"
"    border-radius:6px;\n"
"    height:25px;\n"
"}\n"
"\n"
"QDateEdit::drop-down {\n"
"        border:1px solid #006EFF;\n"
"    border-top-right-radius:4px;\n"
"    border-bottom-right-radius:4px;\n"
"    background-color:#006EFF;\n"
"    width: 20px;\n"
"}\n"
"\n"
"\n"
"QDateEdit::calendar-popup QCalendarWidget QAbstractItemView {\n"
"        border:1px solid #006EFF;\n"
"    padding-left:2px;\n"
"    padding-right:2px;\n"
"}\n"
"")
        self.widget_payment.setObjectName("widget_payment")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.widget_payment)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout()
        self.verticalLayout_6.setSpacing(5)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.label_username = QtWidgets.QLabel(self.widget_payment)
        font = QtGui.QFont()
        font.setFamily("Sans Serif")
        font.setPointSize(14)
        font.setBold(False)
        font.setWeight(50)
        self.label_username.setFont(font)
        self.label_username.setFocusPolicy(QtCore.Qt.NoFocus)
        self.label_username.setStyleSheet("background-color:transparent;")
        self.label_username.setText("")
        self.label_username.setWordWrap(True)
        self.label_username.setObjectName("label_username")
        self.verticalLayout_6.addWidget(self.label_username)
        self.label_type = QtWidgets.QLabel(self.widget_payment)
        font = QtGui.QFont()
        font.setFamily("Sans Serif")
        font.setPointSize(9)
        font.setBold(False)
        font.setWeight(50)
        self.label_type.setFont(font)
        self.label_type.setFocusPolicy(QtCore.Qt.NoFocus)
        self.label_type.setStyleSheet("background-color:transparent;\n"
"color:rgb(99, 99, 99);")
        self.label_type.setText("")
        self.label_type.setWordWrap(True)
        self.label_type.setObjectName("label_type")
        self.verticalLayout_6.addWidget(self.label_type)
        self.label_id = QtWidgets.QLabel(self.widget_payment)
        self.label_id.setMaximumSize(QtCore.QSize(16777215, 10))
        font = QtGui.QFont()
        font.setFamily("Sans Serif")
        font.setPointSize(3)
        font.setBold(False)
        font.setWeight(50)
        self.label_id.setFont(font)
        self.label_id.setFocusPolicy(QtCore.Qt.NoFocus)
        self.label_id.setStyleSheet("color:transparent;")
        self.label_id.setText("")
        self.label_id.setObjectName("label_id")
        self.verticalLayout_6.addWidget(self.label_id)
        self.verticalLayout_7.addLayout(self.verticalLayout_6)
        self.line = QtWidgets.QFrame(self.widget_payment)
        font = QtGui.QFont()
        font.setFamily("Sans Serif")
        font.setBold(False)
        font.setWeight(50)
        self.line.setFont(font)
        self.line.setFocusPolicy(QtCore.Qt.NoFocus)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout_7.addWidget(self.line)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_total = QtWidgets.QLabel(self.widget_payment)
        font = QtGui.QFont()
        font.setFamily("Sans Serif")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.label_total.setFont(font)
        self.label_total.setFocusPolicy(QtCore.Qt.NoFocus)
        self.label_total.setStyleSheet("background-color:transparent;")
        self.label_total.setObjectName("label_total")
        self.verticalLayout.addWidget(self.label_total)
        self.input_total = QtWidgets.QLineEdit(self.widget_payment)
        self.input_total.setMinimumSize(QtCore.QSize(0, 0))
        self.input_total.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setFamily("Sans Serif")
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.input_total.setFont(font)
        self.input_total.setFocusPolicy(QtCore.Qt.NoFocus)
        self.input_total.setStyleSheet("border:1px solid #006EFF;\n"
"background-color: rgb(255, 255, 255);\n"
"border-radius:6px;\n"
"height:25px;\n"
"color:rgb(79, 79, 79);\n"
"")
        self.input_total.setInputMethodHints(QtCore.Qt.ImhDigitsOnly|QtCore.Qt.ImhPreferNumbers)
        self.input_total.setReadOnly(True)
        self.input_total.setObjectName("input_total")
        self.verticalLayout.addWidget(self.input_total)
        self.verticalLayout_7.addLayout(self.verticalLayout)
        spacerItem = QtWidgets.QSpacerItem(20, 10, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout_7.addItem(spacerItem)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label_paid = QtWidgets.QLabel(self.widget_payment)
        font = QtGui.QFont()
        font.setFamily("Sans Serif")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.label_paid.setFont(font)
        self.label_paid.setFocusPolicy(QtCore.Qt.NoFocus)
        self.label_paid.setStyleSheet("background-color:transparent;")
        self.label_paid.setObjectName("label_paid")
        self.verticalLayout_2.addWidget(self.label_paid)
        self.input_paid = QtWidgets.QLineEdit(self.widget_payment)
        self.input_paid.setMinimumSize(QtCore.QSize(200, 0))
        self.input_paid.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setFamily("Sans Serif")
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.input_paid.setFont(font)
        self.input_paid.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.input_paid.setStyleSheet("border:1px solid #006EFF;\n"
"background-color: rgb(255, 255, 255);\n"
"border-radius:6px;\n"
"height:25px\n"
"")
        self.input_paid.setInputMethodHints(QtCore.Qt.ImhDigitsOnly)
        self.input_paid.setInputMask("")
        self.input_paid.setClearButtonEnabled(True)
        self.input_paid.setObjectName("input_paid")
        self.verticalLayout_2.addWidget(self.input_paid)
        self.verticalLayout_7.addLayout(self.verticalLayout_2)
        spacerItem1 = QtWidgets.QSpacerItem(20, 10, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout_7.addItem(spacerItem1)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.label_debt = QtWidgets.QLabel(self.widget_payment)
        font = QtGui.QFont()
        font.setFamily("Sans Serif")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.label_debt.setFont(font)
        self.label_debt.setFocusPolicy(QtCore.Qt.NoFocus)
        self.label_debt.setStyleSheet("background-color:transparent;")
        self.label_debt.setObjectName("label_debt")
        self.verticalLayout_3.addWidget(self.label_debt)
        self.input_debt = QtWidgets.QLineEdit(self.widget_payment)
        self.input_debt.setMinimumSize(QtCore.QSize(200, 0))
        self.input_debt.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setFamily("Sans Serif")
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.input_debt.setFont(font)
        self.input_debt.setFocusPolicy(QtCore.Qt.NoFocus)
        self.input_debt.setStyleSheet("border:1px solid #006EFF;\n"
"background-color: rgb(255, 255, 255);\n"
"border-radius:6px;\n"
"height:25px;\n"
"color:rgb(79, 79, 79);\n"
"")
        self.input_debt.setInputMethodHints(QtCore.Qt.ImhDigitsOnly)
        self.input_debt.setReadOnly(True)
        self.input_debt.setObjectName("input_debt")
        self.verticalLayout_3.addWidget(self.input_debt)
        self.verticalLayout_7.addLayout(self.verticalLayout_3)
        spacerItem2 = QtWidgets.QSpacerItem(20, 10, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout_7.addItem(spacerItem2)
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.label_debt_2 = QtWidgets.QLabel(self.widget_payment)
        font = QtGui.QFont()
        font.setFamily("Sans Serif")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.label_debt_2.setFont(font)
        self.label_debt_2.setFocusPolicy(QtCore.Qt.NoFocus)
        self.label_debt_2.setStyleSheet("background-color:transparent;")
        self.label_debt_2.setObjectName("label_debt_2")
        self.verticalLayout_4.addWidget(self.label_debt_2)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.payment_calendar = QtWidgets.QDateEdit(self.widget_payment)
        self.payment_calendar.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.payment_calendar.setFocusPolicy(QtCore.Qt.NoFocus)
        self.payment_calendar.setStyleSheet("color:black;\n"
"")
        self.payment_calendar.setCalendarPopup(True)
        self.payment_calendar.setTimeSpec(QtCore.Qt.LocalTime)
        self.payment_calendar.setDate(QtCore.QDate(2024, 2, 8))
        self.payment_calendar.setObjectName("payment_calendar")
        self.horizontalLayout_2.addWidget(self.payment_calendar)
        self.verticalLayout_4.addLayout(self.horizontalLayout_2)
        self.verticalLayout_7.addLayout(self.verticalLayout_4)
        spacerItem3 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout_7.addItem(spacerItem3)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.button_add = QtWidgets.QPushButton(self.widget_payment)
        self.button_add.setMaximumSize(QtCore.QSize(125, 16777215))
        font = QtGui.QFont()
        font.setFamily("Sans Serif")
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.button_add.setFont(font)
        self.button_add.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.button_add.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.button_add.setStyleSheet("QPushButton{\n"
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
        self.button_add.setIconSize(QtCore.QSize(20, 20))
        self.button_add.setCheckable(False)
        self.button_add.setChecked(False)
        self.button_add.setAutoExclusive(False)
        self.button_add.setObjectName("button_add")
        self.horizontalLayout.addWidget(self.button_add)
        spacerItem4 = QtWidgets.QSpacerItem(10, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem4)
        self.button_cancel = QtWidgets.QPushButton(self.widget_payment)
        self.button_cancel.setMaximumSize(QtCore.QSize(125, 16777215))
        font = QtGui.QFont()
        font.setFamily("Sans Serif")
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.button_cancel.setFont(font)
        self.button_cancel.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.button_cancel.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.button_cancel.setStyleSheet("QPushButton{\n"
"    color:rgb(255, 53, 53);\n"
"    height:30px;\n"
"    padding:0 5px 0 5px;\n"
"    border:1px solid rgb(255, 53, 53);\n"
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
        self.button_cancel.setIconSize(QtCore.QSize(20, 20))
        self.button_cancel.setCheckable(False)
        self.button_cancel.setAutoExclusive(False)
        self.button_cancel.setObjectName("button_cancel")
        self.horizontalLayout.addWidget(self.button_cancel)
        self.verticalLayout_7.addLayout(self.horizontalLayout)
        self.verticalLayout_5.addWidget(self.widget_payment)

        self.retranslateUi(Payment)
        QtCore.QMetaObject.connectSlotsByName(Payment)

    def retranslateUi(self, Payment):
        _translate = QtCore.QCoreApplication.translate
        self.label_total.setText(_translate("Payment", "Ümumi"))
        self.input_total.setToolTip(_translate("Payment", "Ümumi qiymət"))
        self.input_total.setPlaceholderText(_translate("Payment", "0"))
        self.label_paid.setText(_translate("Payment", "Ödəniş"))
        self.input_paid.setToolTip(_translate("Payment", "Ödəniş miqdarı"))
        self.input_paid.setText(_translate("Payment", "0"))
        self.input_paid.setPlaceholderText(_translate("Payment", "0"))
        self.label_debt.setText(_translate("Payment", "Qalıq Borc"))
        self.input_debt.setToolTip(_translate("Payment", "Qalıq borc"))
        self.input_debt.setPlaceholderText(_translate("Payment", "0"))
        self.label_debt_2.setText(_translate("Payment", "Tarix"))
        self.payment_calendar.setToolTip(_translate("Payment", "Borcun ödəniş tarixi"))
        self.payment_calendar.setDisplayFormat(_translate("Payment", "dd.MM.yyyy"))
        self.button_add.setToolTip(_translate("Payment", "Enter"))
        self.button_add.setText(_translate("Payment", "Təsdiqlə"))
        self.button_add.setShortcut(_translate("Payment", "Return"))
        self.button_cancel.setToolTip(_translate("Payment", "Esc"))
        self.button_cancel.setText(_translate("Payment", "Ləğv et"))
        self.button_cancel.setShortcut(_translate("Payment", "Esc"))
import resources_rc
