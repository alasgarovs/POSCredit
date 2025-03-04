# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'product.ui'
#
# Created by: PyQt5 UI code generator 5.15.11
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Product(object):
    def setupUi(self, Product):
        Product.setObjectName("Product")
        Product.resize(400, 570)
        Product.setMinimumSize(QtCore.QSize(350, 550))
        Product.setMaximumSize(QtCore.QSize(400, 570))
        Product.setWindowTitle("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/favicon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Product.setWindowIcon(icon)
        Product.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(Product)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.widget_product = QtWidgets.QWidget(Product)
        font = QtGui.QFont()
        font.setFamily("Sans Serif")
        font.setBold(False)
        font.setWeight(50)
        self.widget_product.setFont(font)
        self.widget_product.setFocusPolicy(QtCore.Qt.NoFocus)
        self.widget_product.setObjectName("widget_product")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.widget_product)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.label_add_product = QtWidgets.QLabel(self.widget_product)
        font = QtGui.QFont()
        font.setFamily("Sans Serif")
        font.setPointSize(16)
        font.setBold(False)
        font.setWeight(50)
        self.label_add_product.setFont(font)
        self.label_add_product.setFocusPolicy(QtCore.Qt.NoFocus)
        self.label_add_product.setStyleSheet("background-color:transparent;")
        self.label_add_product.setObjectName("label_add_product")
        self.verticalLayout_7.addWidget(self.label_add_product)
        self.label_product_id = QtWidgets.QLabel(self.widget_product)
        self.label_product_id.setMaximumSize(QtCore.QSize(16777215, 10))
        font = QtGui.QFont()
        font.setFamily("Sans Serif")
        font.setPointSize(3)
        font.setBold(False)
        font.setWeight(50)
        self.label_product_id.setFont(font)
        self.label_product_id.setFocusPolicy(QtCore.Qt.NoFocus)
        self.label_product_id.setStyleSheet("color:transparent;")
        self.label_product_id.setText("")
        self.label_product_id.setObjectName("label_product_id")
        self.verticalLayout_7.addWidget(self.label_product_id)
        self.line = QtWidgets.QFrame(self.widget_product)
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
        self.label_product_name = QtWidgets.QLabel(self.widget_product)
        font = QtGui.QFont()
        font.setFamily("Sans Serif")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.label_product_name.setFont(font)
        self.label_product_name.setFocusPolicy(QtCore.Qt.NoFocus)
        self.label_product_name.setStyleSheet("background-color:transparent;")
        self.label_product_name.setObjectName("label_product_name")
        self.verticalLayout.addWidget(self.label_product_name)
        self.input_product_name = QtWidgets.QLineEdit(self.widget_product)
        self.input_product_name.setMinimumSize(QtCore.QSize(0, 0))
        self.input_product_name.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setFamily("Sans Serif")
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.input_product_name.setFont(font)
        self.input_product_name.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.input_product_name.setAutoFillBackground(False)
        self.input_product_name.setStyleSheet("border:1px solid #006EFF;\n"
"background-color: rgb(255, 255, 255);\n"
"border-radius:6px;\n"
"height:25px\n"
"")
        self.input_product_name.setInputMethodHints(QtCore.Qt.ImhNone)
        self.input_product_name.setInputMask("")
        self.input_product_name.setText("")
        self.input_product_name.setMaxLength(100)
        self.input_product_name.setPlaceholderText("")
        self.input_product_name.setClearButtonEnabled(True)
        self.input_product_name.setObjectName("input_product_name")
        self.verticalLayout.addWidget(self.input_product_name)
        self.verticalLayout_7.addLayout(self.verticalLayout)
        spacerItem = QtWidgets.QSpacerItem(20, 10, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout_7.addItem(spacerItem)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setSpacing(20)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label_produt_unit = QtWidgets.QLabel(self.widget_product)
        font = QtGui.QFont()
        font.setFamily("Sans Serif")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.label_produt_unit.setFont(font)
        self.label_produt_unit.setFocusPolicy(QtCore.Qt.NoFocus)
        self.label_produt_unit.setStyleSheet("background-color:transparent;")
        self.label_produt_unit.setObjectName("label_produt_unit")
        self.verticalLayout_2.addWidget(self.label_produt_unit)
        self.combobox_product_unit = QtWidgets.QComboBox(self.widget_product)
        self.combobox_product_unit.setMinimumSize(QtCore.QSize(70, 0))
        self.combobox_product_unit.setMaximumSize(QtCore.QSize(16777215, 33))
        font = QtGui.QFont()
        font.setFamily("Sans Serif")
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.combobox_product_unit.setFont(font)
        self.combobox_product_unit.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.combobox_product_unit.setFocusPolicy(QtCore.Qt.NoFocus)
        self.combobox_product_unit.setStyleSheet("QComboBox {\n"
"    border:1px solid #006EFF;\n"
"    border-radius:2px;\n"
"    background-color: rgb(255, 255, 255);\n"
"    height:25px;\n"
"    color:black;\n"
"}\n"
"\n"
"")
        self.combobox_product_unit.setFrame(True)
        self.combobox_product_unit.setObjectName("combobox_product_unit")
        self.combobox_product_unit.addItem("")
        self.combobox_product_unit.addItem("")
        self.combobox_product_unit.addItem("")
        self.combobox_product_unit.addItem("")
        self.verticalLayout_2.addWidget(self.combobox_product_unit)
        self.horizontalLayout_3.addLayout(self.verticalLayout_2)
        self.verticalLayout_6 = QtWidgets.QVBoxLayout()
        self.verticalLayout_6.setSpacing(0)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.label_product_barcode = QtWidgets.QLabel(self.widget_product)
        font = QtGui.QFont()
        font.setFamily("Sans Serif")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.label_product_barcode.setFont(font)
        self.label_product_barcode.setFocusPolicy(QtCore.Qt.NoFocus)
        self.label_product_barcode.setStyleSheet("background-color:transparent;")
        self.label_product_barcode.setObjectName("label_product_barcode")
        self.verticalLayout_6.addWidget(self.label_product_barcode)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setSpacing(3)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.input_product_barcode = QtWidgets.QLineEdit(self.widget_product)
        self.input_product_barcode.setMinimumSize(QtCore.QSize(180, 0))
        self.input_product_barcode.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setFamily("Sans Serif")
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.input_product_barcode.setFont(font)
        self.input_product_barcode.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.input_product_barcode.setStyleSheet("border:1px solid #006EFF;\n"
"background-color: rgb(255, 255, 255);\n"
"border-radius:6px;\n"
"height:25px;\n"
"")
        self.input_product_barcode.setMaxLength(15)
        self.input_product_barcode.setReadOnly(False)
        self.input_product_barcode.setClearButtonEnabled(True)
        self.input_product_barcode.setObjectName("input_product_barcode")
        self.horizontalLayout_2.addWidget(self.input_product_barcode)
        self.button_empty = QtWidgets.QPushButton(self.widget_product)
        self.button_empty.setMinimumSize(QtCore.QSize(0, 0))
        self.button_empty.setMaximumSize(QtCore.QSize(1, 30))
        font = QtGui.QFont()
        font.setFamily("Sans Serif")
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.button_empty.setFont(font)
        self.button_empty.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.button_empty.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.button_empty.setToolTip("")
        self.button_empty.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.button_empty.setAutoFillBackground(False)
        self.button_empty.setStyleSheet("QPushButton{\n"
"    color:transparent;\n"
"    border:none;\n"
"}")
        self.button_empty.setText("")
        self.button_empty.setIconSize(QtCore.QSize(18, 18))
        self.button_empty.setCheckable(False)
        self.button_empty.setAutoExclusive(False)
        self.button_empty.setObjectName("button_empty")
        self.horizontalLayout_2.addWidget(self.button_empty)
        self.button_generate_barcode = QtWidgets.QPushButton(self.widget_product)
        self.button_generate_barcode.setMinimumSize(QtCore.QSize(40, 20))
        self.button_generate_barcode.setMaximumSize(QtCore.QSize(50, 27))
        font = QtGui.QFont()
        font.setFamily("Sans Serif")
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.button_generate_barcode.setFont(font)
        self.button_generate_barcode.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.button_generate_barcode.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.button_generate_barcode.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.button_generate_barcode.setAutoFillBackground(False)
        self.button_generate_barcode.setStyleSheet("QPushButton{\n"
"    color:#006EFF;\n"
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
        self.button_generate_barcode.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/icons/refresh.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.button_generate_barcode.setIcon(icon1)
        self.button_generate_barcode.setIconSize(QtCore.QSize(18, 18))
        self.button_generate_barcode.setCheckable(False)
        self.button_generate_barcode.setAutoExclusive(False)
        self.button_generate_barcode.setObjectName("button_generate_barcode")
        self.horizontalLayout_2.addWidget(self.button_generate_barcode)
        self.verticalLayout_6.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3.addLayout(self.verticalLayout_6)
        self.verticalLayout_7.addLayout(self.horizontalLayout_3)
        spacerItem1 = QtWidgets.QSpacerItem(20, 10, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout_7.addItem(spacerItem1)
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.verticalLayout_14 = QtWidgets.QVBoxLayout()
        self.verticalLayout_14.setObjectName("verticalLayout_14")
        self.label_produt_quantity_3 = QtWidgets.QLabel(self.widget_product)
        font = QtGui.QFont()
        font.setFamily("Sans Serif")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.label_produt_quantity_3.setFont(font)
        self.label_produt_quantity_3.setFocusPolicy(QtCore.Qt.NoFocus)
        self.label_produt_quantity_3.setStyleSheet("background-color:transparent;")
        self.label_produt_quantity_3.setObjectName("label_produt_quantity_3")
        self.verticalLayout_14.addWidget(self.label_produt_quantity_3)
        self.input_product_quantity = QtWidgets.QLineEdit(self.widget_product)
        self.input_product_quantity.setMinimumSize(QtCore.QSize(0, 0))
        self.input_product_quantity.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setFamily("Sans Serif")
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.input_product_quantity.setFont(font)
        self.input_product_quantity.setCursor(QtGui.QCursor(QtCore.Qt.ForbiddenCursor))
        self.input_product_quantity.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.input_product_quantity.setStyleSheet("border:1px solid #006EFF;\n"
"background-color: rgb(255, 255, 255);\n"
"border-radius:6px;\n"
"height:25px;\n"
"")
        self.input_product_quantity.setMaxLength(10)
        self.input_product_quantity.setReadOnly(True)
        self.input_product_quantity.setClearButtonEnabled(True)
        self.input_product_quantity.setObjectName("input_product_quantity")
        self.verticalLayout_14.addWidget(self.input_product_quantity)
        self.horizontalLayout_7.addLayout(self.verticalLayout_14)
        self.verticalLayout_7.addLayout(self.horizontalLayout_7)
        spacerItem2 = QtWidgets.QSpacerItem(20, 10, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout_7.addItem(spacerItem2)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.label_product_buy_price = QtWidgets.QLabel(self.widget_product)
        font = QtGui.QFont()
        font.setFamily("Sans Serif")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.label_product_buy_price.setFont(font)
        self.label_product_buy_price.setFocusPolicy(QtCore.Qt.NoFocus)
        self.label_product_buy_price.setStyleSheet("background-color:transparent;")
        self.label_product_buy_price.setObjectName("label_product_buy_price")
        self.verticalLayout_3.addWidget(self.label_product_buy_price)
        self.input_product_buy_price = QtWidgets.QLineEdit(self.widget_product)
        self.input_product_buy_price.setMinimumSize(QtCore.QSize(0, 0))
        self.input_product_buy_price.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setFamily("Sans Serif")
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.input_product_buy_price.setFont(font)
        self.input_product_buy_price.setCursor(QtGui.QCursor(QtCore.Qt.ForbiddenCursor))
        self.input_product_buy_price.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.input_product_buy_price.setStyleSheet("border:1px solid #006EFF;\n"
"background-color: rgb(255, 255, 255);\n"
"border-radius:6px;\n"
"height:25px;\n"
"")
        self.input_product_buy_price.setMaxLength(10)
        self.input_product_buy_price.setReadOnly(True)
        self.input_product_buy_price.setClearButtonEnabled(True)
        self.input_product_buy_price.setObjectName("input_product_buy_price")
        self.verticalLayout_3.addWidget(self.input_product_buy_price)
        self.verticalLayout_7.addLayout(self.verticalLayout_3)
        spacerItem3 = QtWidgets.QSpacerItem(20, 10, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout_7.addItem(spacerItem3)
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.label_product_sale_price = QtWidgets.QLabel(self.widget_product)
        font = QtGui.QFont()
        font.setFamily("Sans Serif")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.label_product_sale_price.setFont(font)
        self.label_product_sale_price.setFocusPolicy(QtCore.Qt.NoFocus)
        self.label_product_sale_price.setStyleSheet("background-color:transparent;")
        self.label_product_sale_price.setObjectName("label_product_sale_price")
        self.verticalLayout_4.addWidget(self.label_product_sale_price)
        self.input_product_sale_price = QtWidgets.QLineEdit(self.widget_product)
        self.input_product_sale_price.setMinimumSize(QtCore.QSize(0, 0))
        self.input_product_sale_price.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setFamily("Sans Serif")
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.input_product_sale_price.setFont(font)
        self.input_product_sale_price.setCursor(QtGui.QCursor(QtCore.Qt.ForbiddenCursor))
        self.input_product_sale_price.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.input_product_sale_price.setStyleSheet("border:1px solid #006EFF;\n"
"background-color: rgb(255, 255, 255);\n"
"border-radius:6px;\n"
"height:25px;\n"
"")
        self.input_product_sale_price.setMaxLength(10)
        self.input_product_sale_price.setEchoMode(QtWidgets.QLineEdit.Normal)
        self.input_product_sale_price.setReadOnly(True)
        self.input_product_sale_price.setClearButtonEnabled(True)
        self.input_product_sale_price.setObjectName("input_product_sale_price")
        self.verticalLayout_4.addWidget(self.input_product_sale_price)
        self.verticalLayout_7.addLayout(self.verticalLayout_4)
        spacerItem4 = QtWidgets.QSpacerItem(20, 30, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout_7.addItem(spacerItem4)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.button_add = QtWidgets.QPushButton(self.widget_product)
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
        self.button_add.setAutoExclusive(False)
        self.button_add.setObjectName("button_add")
        self.horizontalLayout.addWidget(self.button_add)
        spacerItem5 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem5)
        self.button_cancel = QtWidgets.QPushButton(self.widget_product)
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
        spacerItem6 = QtWidgets.QSpacerItem(60, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem6)
        self.button_delete = QtWidgets.QPushButton(self.widget_product)
        self.button_delete.setMaximumSize(QtCore.QSize(40, 16777215))
        font = QtGui.QFont()
        font.setFamily("Sans Serif")
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.button_delete.setFont(font)
        self.button_delete.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.button_delete.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.button_delete.setStyleSheet("QPushButton{\n"
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
        self.button_delete.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/icons/delete.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.button_delete.setIcon(icon2)
        self.button_delete.setIconSize(QtCore.QSize(20, 20))
        self.button_delete.setCheckable(False)
        self.button_delete.setAutoExclusive(False)
        self.button_delete.setObjectName("button_delete")
        self.horizontalLayout.addWidget(self.button_delete)
        self.verticalLayout_7.addLayout(self.horizontalLayout)
        self.verticalLayout_5.addWidget(self.widget_product)

        self.retranslateUi(Product)
        QtCore.QMetaObject.connectSlotsByName(Product)

    def retranslateUi(self, Product):
        _translate = QtCore.QCoreApplication.translate
        self.label_add_product.setText(_translate("Product", "Məhsul Əlavə et"))
        self.label_product_name.setText(_translate("Product", "Məhsul adı*"))
        self.input_product_name.setToolTip(_translate("Product", "Məhsul adı"))
        self.label_produt_unit.setText(_translate("Product", "Vahid"))
        self.combobox_product_unit.setCurrentText(_translate("Product", "ədəd"))
        self.combobox_product_unit.setItemText(0, _translate("Product", "ədəd", "dsffsd"))
        self.combobox_product_unit.setItemText(1, _translate("Product", "blok"))
        self.combobox_product_unit.setItemText(2, _translate("Product", "kq"))
        self.combobox_product_unit.setItemText(3, _translate("Product", "metr"))
        self.label_product_barcode.setText(_translate("Product", "Barkod*"))
        self.input_product_barcode.setToolTip(_translate("Product", "Məhsul barkodu"))
        self.input_product_barcode.setPlaceholderText(_translate("Product", "000000000000"))
        self.button_generate_barcode.setToolTip(_translate("Product", "Barkod yarat - Ctrl+B"))
        self.button_generate_barcode.setShortcut(_translate("Product", "Ctrl+B"))
        self.label_produt_quantity_3.setText(_translate("Product", "Miqdar"))
        self.input_product_quantity.setToolTip(_translate("Product", "Məhsulun anbar miqdarı"))
        self.input_product_quantity.setText(_translate("Product", "0.0"))
        self.input_product_quantity.setPlaceholderText(_translate("Product", "0"))
        self.label_product_buy_price.setText(_translate("Product", "Alış Qiyməti"))
        self.input_product_buy_price.setToolTip(_translate("Product", "Məhsulun alış qiyməti"))
        self.input_product_buy_price.setText(_translate("Product", "0.0"))
        self.input_product_buy_price.setPlaceholderText(_translate("Product", "0"))
        self.label_product_sale_price.setText(_translate("Product", "Satış Qiyməti"))
        self.input_product_sale_price.setToolTip(_translate("Product", "Məhsulun satış qiyməti"))
        self.input_product_sale_price.setText(_translate("Product", "0.0"))
        self.input_product_sale_price.setPlaceholderText(_translate("Product", "0"))
        self.button_add.setToolTip(_translate("Product", "Enter"))
        self.button_add.setText(_translate("Product", "Təsdiqlə"))
        self.button_add.setShortcut(_translate("Product", "Return"))
        self.button_cancel.setToolTip(_translate("Product", "Esc"))
        self.button_cancel.setText(_translate("Product", "Ləğv et"))
        self.button_cancel.setShortcut(_translate("Product", "Esc"))
        self.button_delete.setToolTip(_translate("Product", "Məhsulu sil - Ctrl+Del"))
        self.button_delete.setShortcut(_translate("Product", "Ctrl+Del"))
import resources_rc
