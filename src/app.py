import json
import pandas as pd
import random
import sys
from functools import partial

from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QIcon, QPixmap, QBrush, QColor, QFont, QTextDocument
from PyQt5.QtPrintSupport import QPrinter, QPrintDialog
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QFileDialog, QDialog, \
    QPushButton, QTableWidgetItem, QWidget, QHBoxLayout
from db_connect import *
from forms import ProductFormValidator, CustomerFormValidator, CheckOutFormValidator, PaymentFormValidator, \
    LicenseManager
from info import AppName, AppVersion, LastUpdate, LegalCopyright, Website
from ui_pycode.customer import Ui_Customer
from ui_pycode.document import Ui_Document
from ui_pycode.main import Ui_Main
from ui_pycode.payment import Ui_Payment
from ui_pycode.price import Ui_Price
from ui_pycode.product import Ui_Product


class Main(QMainWindow, Ui_Main):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.setup_window()
        self.setup_buttons()
        self.setup_customers_dialog()
        self.setup_products_dialog()
        self.setup_payments_dialog()
        self.setup_documents_dialog()
        self.setup_license()
        self.setup_timers()

    def setup_window(self):
        self.setWindowFlags(QtCore.Qt.Window | QtCore.Qt.FramelessWindowHint)
        self.setWindowTitle(AppName)
        self.showFullScreen()
        self.icon_name_widget.setHidden(True)
        self.button_clear_customer.hide()
        self.reset_checkout_table()
        self.switch_to_sale_page()

    # Connect buttons
    def setup_buttons(self):
        button_page_map = {
            self.button_sale_1: 'sale',
            self.button_sale_2: 'sale',
            self.button_customer_1: 'customers',
            self.button_customer_2: 'customers',
            self.button_choose_customer: 'customers',
            self.button_product_1: 'products',
            self.button_product_2: 'products',
            self.button_document_1: 'documents',
            self.button_document_2: 'documents',
            self.button_payment_1: 'payment',
            self.button_payment_2: 'payment',
        }

        for button, page in button_page_map.items():
            button.clicked.connect(lambda _, p=page: self.switch_to_page(p))

        self.button_info_1.clicked.connect(self.about_app)
        self.button_info_2.clicked.connect(self.about_app)
        self.button_exit_1.clicked.connect(self.confirm_exit)
        self.button_exit_2.clicked.connect(self.confirm_exit)

    # CUSTOMERS WINDOW
    def setup_customers_dialog(self):
        self.Customer, self.Customer_GUI = self.create_dialog(Ui_Customer)
        self.button_filtr_customer.clicked.connect(
            lambda: self.open_payment_window(self.input_filtr_customer.text(), 'search'))
        self.button_export_excel_customers.clicked.connect(lambda: self.export_to_excel('customers'))
        self.button_clear_customer.clicked.connect(self.clear_customer)
        self.button_new_customer.clicked.connect(lambda: self.open_customer_window(None))
        self.table_customers.cellDoubleClicked.connect(self.on_customer_click)
        self.Customer_GUI.button_delete.clicked.connect(self.delete_customer)
        self.Customer_GUI.button_add.clicked.connect(lambda: self.create_or_update_customer(False))
        self.Customer_GUI.button_add_and_create.clicked.connect(self.create_and_add_customer)
        self.Customer_GUI.button_cancel.clicked.connect(self.Customer.close)

    # PRODUCTS WINDOW
    def setup_products_dialog(self):
        self.Product, self.Product_GUI = self.create_dialog(Ui_Product)
        self.button_export_excel_products.clicked.connect(lambda: self.export_to_excel('products'))
        self.button_filtr_product.clicked.connect(lambda: self.filtr_product(self.input_filtr_product.text()))
        self.button_search_product.clicked.connect(lambda: self.search_product(self.input_search_product.text()))
        self.button_new_product.clicked.connect(lambda: self.open_product_window(None))
        self.Product_GUI.button_generate_barcode.clicked.connect(self.generate_barcode)
        self.Product_GUI.button_delete.clicked.connect(self.delete_product)
        self.Product_GUI.button_add.clicked.connect(self.create_or_update_product)
        self.Product_GUI.button_cancel.clicked.connect(self.Product.close)

        # Product Price Window
        self.Price, self.Price_GUI = self.create_dialog(Ui_Price)
        self.Price_GUI.button_add.clicked.connect(self.choose_product)
        self.Price_GUI.button_cancel.clicked.connect(self.Price.close)
        self.table_products.cellDoubleClicked.connect(self.on_product_click)

    # PAYMENTS WINDOW
    def setup_payments_dialog(self):
        self.Payment, self.Payment_GUI = self.create_dialog(Ui_Payment)
        self.button_sale.clicked.connect(self.calculate_sale)
        self.Payment_GUI.button_add.clicked.connect(self.make_payment)
        self.Payment_GUI.button_cancel.clicked.connect(self.Payment.close)

    # DOCUMENTS WINDOW 
    def setup_documents_dialog(self):
        self.Document, self.Document_GUI = self.create_dialog(Ui_Document)
        self.Document_GUI.button_print_document.clicked.connect(self.print_sale_document)
        self.Document_GUI.button_close.clicked.connect(self.Document.close)
        self.table_documents.cellDoubleClicked.connect(self.on_document_click)

    # LICENSE
    def setup_license(self):
        self.button_add_license.clicked.connect(self.add_license)
        self.button_copy.clicked.connect(self.copy_processor_id)

    def create_dialog(self, ui_class):
        dialog = QDialog(self)
        dialog.setWindowTitle(AppName)
        ui_instance = ui_class()
        ui_instance.setupUi(dialog)
        return dialog, ui_instance

    # Timers
    def setup_timers(self):
        timer_configs = {
            'customer_combobox': (self.load_customers_data, self.combobox_level_customer.currentIndexChanged),
            'customer_search': (self.load_customers_data, self.input_filtr_customer.textChanged),
            'product_search': (self.load_products_data, self.input_filtr_product.textChanged),
            'document_search': (self.load_documents_data, self.input_filtr_documents.textChanged),
            'payment_search': (self.load_payments_data, self.input_filtr_payment.textChanged),
        }

        # Create and connect timers based on the configurations
        for name, (callback, signal) in timer_configs.items():
            timer = QTimer(self)
            timer.setSingleShot(True)
            timer.timeout.connect(callback)

            signal.connect(lambda _, t=timer: t.start(300))

        # Special case for the combo box timer
        self.customer_combobox_timer = QTimer(self)
        self.customer_combobox_timer.setSingleShot(True)
        self.customer_combobox_timer.timeout.connect(self.load_customers_data)
        self.combobox_level_customer.currentIndexChanged.connect(lambda: self.customer_combobox_timer.start(300))

    ############## SWITCH PAGES ###########################
    #######################################################
    def switch_to_page(self, page):
        if page == 'sale':
            self.switch_to_sale_page()
        elif page == 'customers':
            self.switch_to_customers_page()
        elif page == 'products':
            self.switch_to_product_page()
        elif page == 'documents':
            self.switch_to_document_page()
        elif page == 'payment':
            self.switch_to_payment_page()

    def switch_to_sale_page(self):
        if self.switch_to_license_page():
            self.button_sale_1.setChecked(not self.button_sale_1.isChecked())
            self.stackedWidget.setCurrentIndex(0)
            self.input_search_product.clear()
            self.input_search_product.setFocus()
            self.load_checkout_products()

    def switch_to_customers_page(self):
        if self.switch_to_license_page():
            self.stackedWidget.setCurrentIndex(1)
            self.combobox_level_customer.setCurrentText('Müştərilər')
            self.input_filtr_customer.clear()
            self.input_filtr_customer.setFocus()
            self.load_customers_data()

    def switch_to_product_page(self):
        if self.switch_to_license_page():
            self.stackedWidget.setCurrentIndex(2)
            self.input_filtr_product.clear()
            self.input_filtr_product.setFocus()
            self.load_products_data()

    def switch_to_document_page(self):
        if self.switch_to_license_page():
            self.stackedWidget.setCurrentIndex(3)
            self.input_filtr_documents.clear()
            self.load_documents_data()

    def switch_to_payment_page(self):
        if self.switch_to_license_page():
            self.stackedWidget.setCurrentIndex(4)
            self.input_filtr_payment.clear()
            self.load_payments_data()

    def switch_to_license_page(self):
        is_license_valid = self.check_license()

        if not is_license_valid:
            self.stackedWidget.setCurrentIndex(5)
            license_manager = LicenseManager()
            self.label_processor_id.setText(license_manager.get_processor_id())
            is_license_valid = False

        self.toggle_buttons(is_license_valid)

        return is_license_valid

    def toggle_buttons(self, is_enabled):
        """Enable or disable buttons based on the provided status."""
        buttons = [
            self.button_sale_1, self.button_sale_2,
            self.button_customer_1, self.button_customer_2,
            self.button_product_1, self.button_product_2,
            self.button_document_1, self.button_document_2,
            self.button_payment_1, self.button_payment_2,
            self.button_settings_1, self.button_settings_2,
            self.button_users_1, self.button_users_2
        ]

        for button in buttons:
            button.setEnabled(is_enabled)

    ############ LICENSE ###################################
    ########################################################
    def check_license(self):
        license_manager = LicenseManager()
        with Session() as session:
            current_license = session.query(License).first()

            if current_license:
                is_valid = license_manager.validate_license_key(current_license.app_license)
                return is_valid  # Activate License
                # return True  # Bypass License
            else:
                return None

    def add_license(self):
        current_license = self.input_license.text().strip()
        license_manager = LicenseManager()
        if current_license:
            with Session() as session:
                is_valid = license_manager.validate_license_key(current_license)
                if is_valid:
                    new_license = session.query(License).first()
                    if not new_license:
                        new_license = License()

                    new_license.app_license = current_license
                    session.add(new_license)
                    session.commit()
                    self.switch_to_sale_page()
                else:
                    QMessageBox.critical(self, AppName, 'Lisenziya Kodu düzgün deyil!')
        else:
            QMessageBox.critical(self, AppName, 'Lisenziya Kodunu daxil edin!')

    def copy_processor_id(self):
        processor_id = self.label_processor_id.text()
        if processor_id:
            clipboard = QApplication.clipboard()
            clipboard.setText(processor_id)
            QMessageBox.information(self, AppName, "ID kopyalandı.")
        else:
            pass

    ############ DOCUMENTS ###################################
    ##########################################################
    def clear_tables(self):
        self.table_customers.setRowCount(0)
        self.table_documents.setRowCount(0)
        self.table_payments.setRowCount(0)
        self.table_products.setRowCount(0)
        self.table_sale.setRowCount(0)

    def load_documents_data(self):
        search_index = str(self.input_filtr_documents.text())
        with Session() as session:

            if search_index:
                documents = session.query(Documents).filter(Documents.customer.like(f"%{search_index}%")).order_by(
                    Documents.id.desc()).all()
            else:
                documents = session.query(Documents).order_by(Documents.id.desc()).all()

            self.clear_tables()
            self.table_documents.setRowCount(len(documents))

            for row_index, document in enumerate(documents):
                self.table_documents.setItem(row_index, 0, QTableWidgetItem(str(document.id)))

                customer = QTableWidgetItem(document.customer)
                customer.setForeground(QBrush(QColor('#006EFF')))

                self.table_documents.setItem(row_index, 1, customer)
                self.table_documents.setItem(row_index, 2, QTableWidgetItem(str(document.total)))
                self.table_documents.setItem(row_index, 3, QTableWidgetItem(str(document.paid)))
                self.table_documents.setItem(row_index, 4, QTableWidgetItem(str(document.debt)))
                date_string = document.date.strftime('%d.%m.%Y - %H:%M')
                self.table_documents.setItem(row_index, 5, QTableWidgetItem(date_string))

            self.table_documents.setColumnHidden(0, True)
            self.table_documents.setColumnWidth(1, 150)

    def on_document_click(self, row, column):
        document_id = self.table_documents.item(row, 0).text()
        if column == 1:
            document = self.get_document_by_id(document_id)
            self.show_sale_document(document)

    def get_document_by_id(self, document_id):
        with Session() as session:
            return session.query(Documents).filter(Documents.id == document_id).first()

    def show_sale_document(self, document):
        self.Document_GUI.label_document.setText(f'Satış Sənədi - {document.id}')
        self.Document_GUI.label_about_customer.setText(f"Alıcı: {document.customer}")

        products = json.loads(document.products)
        total_price = 0

        self.Document_GUI.table_sale.setRowCount(len(products))

        for row_index, product in enumerate(products):
            product_total_price = float(product['price']) * float(product['quantity'])
            total_price = float(total_price) + float(product_total_price)

            self.Document_GUI.table_sale.setItem(row_index, 0, QTableWidgetItem(product['name']))
            self.Document_GUI.table_sale.setItem(row_index, 1, QTableWidgetItem(str(product['quantity'])))
            self.Document_GUI.table_sale.setItem(row_index, 2, QTableWidgetItem(str(product['price'])))
            self.Document_GUI.table_sale.setItem(row_index, 3, QTableWidgetItem(str(product_total_price)))
            self.Document_GUI.table_sale.setItem(row_index, 4, QTableWidgetItem(product['barcode']))

        self.Document_GUI.label_total_price.setText(f"{total_price:.2f}")
        self.Document_GUI.table_sale.setColumnWidth(1, 150)

        self.Document.exec_()

    def print_sale_document(self):
        customer_name = self.Document_GUI.label_about_customer.text()
        total_price = float(self.Document_GUI.label_total_price.text())

        print_content = f"{customer_name}\n\nMəbləğ: {total_price:.2f}\n\n"
        print_content += "-" * 70 + "\n"
        print_content += "Məhsul\t  Qiymət\t  Miqdar\t  Ümumi\n"
        print_content += "-" * 70 + "\n"

        row_count = self.Document_GUI.table_sale.rowCount()
        for row in range(row_count):
            product_name = self.Document_GUI.table_sale.item(row, 0).text()
            price = float(self.Document_GUI.table_sale.item(row, 1).text())
            quantity = float(self.Document_GUI.table_sale.item(row, 2).text())

            product_total_price = price * quantity
            total_price += product_total_price

            words = product_name.split()

            wrapped_product_name = ""
            current_line = ""

            for word in words:
                if len(current_line) + len(word) + 1 > 10:
                    wrapped_product_name += current_line.strip() + "\n"
                    current_line = word
                else:
                    if current_line:
                        current_line += " "
                    current_line += word

            if current_line:
                wrapped_product_name += current_line.strip()

            price = "   " + str(price)
            print_content += f"{wrapped_product_name}\t  {price}\t  {quantity}\t  {product_total_price:.2f}\t\n\n"

        printer = QPrinter(QPrinter.HighResolution)
        print_dialog = QPrintDialog(printer, self.Document)

        if print_dialog.exec_() == QPrintDialog.Accepted:
            text_document = QTextDocument()
            text_document.setPlainText(print_content)

            text_document.setTextWidth(printer.pageRect().width())

            font = QFont()
            font.setPointSize(12)
            text_document.setDefaultFont(font)

            text_document.print_(printer)

    ############ SALE #####################################
    #######################################################
    def calculate_sale(self):
        id = self.label_customer_id.text()
        label_name = 'Ümumi'
        button_name = 'Təsdiqlə'
        total = 0

        if not id:
            QMessageBox.critical(self, AppName, 'Alıcı seçilməyib!')
            self.input_search_product.setFocus()
            return

        with Session() as session:
            sale_products = session.query(CheckOut).all()

            if not sale_products:
                QMessageBox.critical(self, AppName, 'Satış üçün məhsul daxil edin!')
                return

            for product in sale_products:
                total = float(total) + float(product.product_total_price)

            customer = session.query(Customers).filter(Customers.id == id).first()

            self.Payment_GUI.label_username.setText(customer.customer_name)
            self.Payment_GUI.label_customer_id.setText(str(customer.id))
            self.Payment_GUI.label_total.setText(label_name)
            self.Payment_GUI.button_add.setText(button_name)

            self.Payment_GUI.input_total.setText(str(total))
            self.Payment_GUI.input_paid.clear()
            self.Payment_GUI.input_debt.setText(str(total))
            self.Payment_GUI.payment_calendar.setDate(customer.customer_payment_date)

            self.Payment_GUI.input_total.textChanged.connect(self.update_debt)
            self.Payment_GUI.input_paid.textChanged.connect(self.update_debt)

            self.Payment.exec_()

    def load_checkout_products(self):
        with Session() as session:
            sale_products = session.query(CheckOut).all()

            self.clear_tables()
            self.table_sale.setRowCount(len(sale_products))

            for row_index, product in enumerate(sale_products):
                self.table_sale.setItem(row_index, 0, QTableWidgetItem(product.product_name))
                self.table_sale.setItem(row_index, 1, QTableWidgetItem(str(product.product_quantity)))
                self.table_sale.setItem(row_index, 2, QTableWidgetItem(str(product.product_price)))
                self.table_sale.setItem(row_index, 3, QTableWidgetItem(str(product.product_total_price)))
                self.table_sale.setItem(row_index, 4, QTableWidgetItem(product.product_barcode))

                right_buttons = QWidget()
                layout_button = QHBoxLayout(right_buttons)

                button_edit = self.create_buttons(':/icons/edit.png')
                button_edit.clicked.connect(partial(self.search_product, product.product_name))
                layout_button.addWidget(button_edit)

                button_delete = self.create_buttons(':/icons/delete.png')
                button_delete.clicked.connect(partial(self.delete_checkout_product, product))
                layout_button.addWidget(button_delete)

                layout_button.setContentsMargins(0, 0, 0, 0)
                right_buttons.setLayout(layout_button)

                self.table_sale.setCellWidget(row_index, 5, right_buttons)

    def create_buttons(self, icon_path):
        button = QPushButton()
        button.setIcon(QIcon(icon_path))
        button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        button.setFixedWidth(20)
        button.setIconSize(QtCore.QSize(19, 19))
        button.setStyleSheet(
            "QPushButton{\n"
            "padding:5px;\n"
            "border:none;\n"
            "border-radius:8px;\n"
            "}\n")

        return button

    def delete_checkout_product(self, product):
        with Session() as session:
            session.delete(product)
            session.commit()
            self.load_checkout_products()

    def search_product(self, product):
        search_index = product
        if not search_index:
            QMessageBox.critical(self, AppName, 'Məhsul adını vəya barkodunu daxil edin!')
            self.input_search_product.setFocus()
            return

        with Session() as session:

            product = session.query(Products).filter((Products.product_name.like(f"%{search_index}%")) | (
                Products.product_barcode.like(f"%{search_index}%"))).first()

            if product:
                sales_product = session.query(CheckOut).filter(CheckOut.product_id == product.id).first()

                if sales_product:
                    price = sales_product.product_price
                    quantity = sales_product.product_quantity
                else:
                    price = product.product_sale_price
                    quantity = 1

                self.Price_GUI.label_stock_quantity.setText(f'Anbar Qalığı: {product.product_quantity}')
                self.Price_GUI.label_product.setText(product.product_name)
                self.Price_GUI.label_id.setText(str(product.id))
                self.Price_GUI.input_price.setText(str(price))
                self.Price_GUI.input_quantity.setText(str(quantity))
                self.Price.exec_()
            else:
                QMessageBox.critical(self, AppName, 'Məhsul tapılmadı!')

            self.input_search_product.clear()
            self.input_search_product.setFocus()

    def choose_product(self):
        id = self.Price_GUI.label_id.text()
        price = self.Price_GUI.input_price.text().strip()
        quantity = self.Price_GUI.input_quantity.text().strip()

        validator = CheckOutFormValidator(quantity, price)
        result = validator.validate()
        if result is True:
            with Session() as session:
                product = session.query(Products).filter(Products.id == id).first()

                sales_product = session.query(CheckOut).filter(CheckOut.product_id == id).first()

                if sales_product:
                    pass
                else:
                    sales_product = CheckOut()

                sales_product.product_id = product.id
                sales_product.product_name = product.product_name
                sales_product.product_quantity = float(quantity)
                sales_product.product_price = float(price)
                sales_product.product_total_price = float(quantity) * float(price)
                sales_product.product_barcode = product.product_barcode

                session.add(sales_product)
                session.commit()
                self.Price.close()

                self.switch_to_sale_page()
        else:
            QMessageBox.critical(self.Price, AppName, result)
            self.input_filtr_product.clear()
            self.input_filtr_product.setFocus()

    def choose_customer(self, customer):
        about_customer = f"{customer.customer_name}, {customer.customer_address}"
        self.label_about_customer.setText(about_customer)
        self.label_customer_id.setText(str(customer.id))
        self.button_clear_customer.show()

        self.switch_to_sale_page()

    def clear_customer(self):
        self.label_about_customer.clear()
        self.label_customer_id.clear()
        self.button_clear_customer.hide()

    def reset_checkout_table(self):
        with Session() as session:
            session.query(CheckOut).delete()
            session.commit()
        self.load_checkout_products()

    ############ PRODUCTS ######################################
    ############################################################
    def create_or_update_product(self):
        id = self.Product_GUI.label_product_id.text()
        product_name = self.Product_GUI.input_product_name.text().strip()
        product_quantity = self.Product_GUI.input_product_quantity.text().strip()
        product_buy_price = self.Product_GUI.input_product_buy_price.text().strip()
        product_sale_price = self.Product_GUI.input_product_sale_price.text().strip()
        product_barcode = self.Product_GUI.input_product_barcode.text().strip()

        validator = ProductFormValidator(product_name, product_quantity, product_buy_price, product_sale_price,
                                         product_barcode, product_id=id)
        result = validator.validate()

        if result:
            with Session() as session:
                if id:
                    product = session.query(Products).filter(Products.id == id).first()
                    message = 'Məhsul məlumatları uğurla yeniləndi.'
                else:
                    product = Products()
                    message = 'Məhsul uğurla əlavə edildi.'

                product.product_name = product_name
                product.product_quantity = float(product_quantity)
                product.product_buy_price = float(product_buy_price)
                product.product_sale_price = float(product_sale_price)
                product.product_barcode = product_barcode

                session.add(product)
                session.commit()

                self.Product.close()
                self.load_products_data()
                QMessageBox.information(self.Product, AppName, message)

        else:
            QMessageBox.critical(self.Product, AppName, result)

    def open_product_window(self, product):
        if not product:
            self.Product_GUI.label_product_id.clear()
            self.Product_GUI.input_product_name.clear()
            self.Product_GUI.input_product_quantity.setText('0')
            self.Product_GUI.input_product_buy_price.setText('0')
            self.Product_GUI.input_product_sale_price.setText('0')
            self.Product_GUI.input_product_barcode.clear()
            self.Product_GUI.button_add.setText('Təsdiqlə')
            self.Product_GUI.label_add_product.setText('Məhsul əlavə et')
            self.Product_GUI.button_delete.hide()
        else:
            self.Product_GUI.label_product_id.setText(str(product.id))
            self.Product_GUI.input_product_name.setText(product.product_name)
            self.Product_GUI.input_product_quantity.setText(str(product.product_quantity))
            self.Product_GUI.input_product_buy_price.setText(str(product.product_buy_price))
            self.Product_GUI.input_product_sale_price.setText(str(product.product_sale_price))
            self.Product_GUI.input_product_barcode.setText(product.product_barcode)
            self.Product_GUI.button_add.setText('Yenilə')
            self.Product_GUI.label_add_product.setText('Məlumatları yenilə')
            self.Product_GUI.button_delete.show()

        self.Product.exec_()
        self.input_filtr_product.clear()
        self.input_filtr_product.setFocus()

    def delete_product(self):
        id = self.Product_GUI.label_product_id.text()
        with Session() as session:
            product = session.query(Products).filter(Products.id == id).first()
            reply = QMessageBox.question(self, AppName,
                                         f'{product.product_name} adlı məhsul silinsin?',
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

            if reply == QMessageBox.Yes:
                session.delete(product)
                session.commit()

                self.Product.close()
                QMessageBox.information(self, AppName, 'Məhsul uğurla silindi')
                self.load_products_data()
            else:
                pass

    def load_products_data(self):
        search_index = str(self.input_filtr_product.text())

        with Session() as session:
            if search_index:
                all_products = session.query(Products).filter(
                    (Products.product_name.like(f"%{search_index}%")) |
                    (Products.product_barcode.like(f"%{search_index}%"))).order_by(Products.product_name.desc()).all()
            else:
                all_products = session.query(Products).order_by(Products.product_name.desc()).all()

            self.clear_tables()
            self.table_products.setRowCount(len(all_products))

            for row_index, product in enumerate(all_products):
                self.table_products.setItem(row_index, 0, QTableWidgetItem(str(product.id)))

                product_name = QTableWidgetItem(str(product.product_name))
                product_name.setForeground(QBrush(QColor('#006EFF')))
                self.table_products.setItem(row_index, 1, product_name)

                self.table_products.setItem(row_index, 2, QTableWidgetItem(str(product.product_quantity)))
                self.table_products.setItem(row_index, 3, QTableWidgetItem(str(product.product_buy_price)))
                self.table_products.setItem(row_index, 4, QTableWidgetItem(str(product.product_sale_price)))
                self.table_products.setItem(row_index, 5, QTableWidgetItem(str(product.product_barcode)))

                edit = QTableWidgetItem()
                icon_pixmap = QPixmap(f':/icons/edit.png')
                edit.setIcon(QIcon(icon_pixmap))
                self.table_products.setItem(row_index, 6, edit)

            self.table_products.setColumnHidden(0, True)
            self.table_products.setColumnWidth(1, 150)
            self.table_products.setColumnWidth(6, 20)

    def on_product_click(self, row, column):
        product_id = self.table_products.item(row, 0).text()
        if column == 1:
            product = self.get_product_by_id(product_id)
            self.search_product(product.product_name)
        elif column == 6:
            product = self.get_product_by_id(product_id)
            self.open_product_window(product)

    def get_product_by_id(self, product_id):
        with Session() as session:
            return session.query(Products).filter(Products.id == product_id).first()

    def filtr_product(self, search_index):
        if not search_index:
            QMessageBox.critical(self, AppName, 'Məhsul adını vəya barkodunu daxil edin!')
            self.input_filtr_product.clear()
            self.input_filtr_product.setFocus()
            return

        with Session() as session:
            product = session.query(Products).filter((Products.product_name.like(f"%{search_index}%")) | (
                Products.product_barcode.like(f"%{search_index}%"))).first()

            if product:
                self.open_product_window(product)
            else:
                QMessageBox.critical(self, AppName, 'Məhsul tapılmadı!')
                self.input_filtr_product.clear()
                self.input_filtr_product.setFocus()

    def generate_barcode(self):
        random_number = str(random.randint(100000000000, 999999999999))
        self.Product_GUI.input_product_barcode.clear()
        self.Product_GUI.input_product_barcode.setText(random_number)

    ############## PAYMENTS ########################################
    ################################################################
    def load_payments_data(self):
        search_index = str(self.input_filtr_payment.text())
        with Session() as session:

            if search_index:
                payments = session.query(Payments).filter(Payments.customer.like(f"%{search_index}%")).order_by(
                    Payments.id.desc()).all()
            else:
                payments = session.query(Payments).order_by(Payments.id.desc()).all()

            self.clear_tables()
            self.table_payments.setRowCount(len(payments))

            for row_index, payment in enumerate(payments):
                process_item = QTableWidgetItem(str(payment.process))
                icon_pixmap = QPixmap(f':/icons/caret-{payment.status}.png')
                process_item.setIcon(QIcon(icon_pixmap))

                self.table_payments.setItem(row_index, 0, QTableWidgetItem(payment.customer))
                self.table_payments.setItem(row_index, 1, QTableWidgetItem(str(payment.total)))
                self.table_payments.setItem(row_index, 2, process_item)
                self.table_payments.setItem(row_index, 3, QTableWidgetItem(str(payment.debt)))
                date_string = payment.date.strftime('%d.%m.%Y - %H:%M')
                self.table_payments.setItem(row_index, 4, QTableWidgetItem(date_string))

            self.table_payments.setColumnWidth(0, 150)

    def create_payment(self, old_debt, new_debt, session, status):

        payment = Payments()

        payment.customer = self.Payment_GUI.label_username.text().strip()

        if status == 'down':
            payment.total = float(self.Payment_GUI.input_total.text().strip())
            payment.process = float(self.Payment_GUI.input_paid.text().strip())
        else:
            payment.total = float(old_debt)
            payment.process = float(self.Payment_GUI.input_debt.text().strip())

        payment.debt = new_debt
        payment.status = status

        session.add(payment)

    def create_sale_document(self, session, customer):
        sale_products = session.query(CheckOut).all()

        product_list = []
        for i in sale_products:
            product_details = {
                'id': i.product_id,
                'name': i.product_name,
                'quantity': i.product_quantity,
                'price': i.product_price,
                'barcode': i.product_barcode
            }
            product_list.append(product_details)

            product = session.query(Products).filter(Products.id == i.product_id).first()
            product.product_quantity = product.product_quantity - i.product_quantity

        products_json = json.dumps(product_list)

        document = Documents()

        document.customer_id = customer.id
        document.customer = f"{customer.customer_name}"
        document.products = products_json
        document.total = self.Payment_GUI.input_total.text()
        document.paid = self.Payment_GUI.input_paid.text()
        document.debt = self.Payment_GUI.input_debt.text()

        session.add(document)

    def make_payment(self):
        customer_id = self.Payment_GUI.label_customer_id.text()
        button_name = self.Payment_GUI.button_add.text()
        current_debt = self.Payment_GUI.input_debt.text().strip()
        payment_paid = self.Payment_GUI.input_paid.text().strip()
        payment_date = self.Payment_GUI.payment_calendar.date().toPyDate()

        validator = PaymentFormValidator(current_debt, payment_paid)
        result = validator.validate()

        if result is True:
            current_debt = float(current_debt)
            with Session() as session:
                customer = session.query(Customers).filter(Customers.id == customer_id).first()
                customer.customer_payment_date = payment_date

                old_debt = customer.customer_debt
                if button_name == 'Yenilə':
                    customer.customer_debt = current_debt
                    self.create_payment(None, current_debt, session, 'down')

                    session.commit()

                    self.input_filtr_customer.clear()
                    self.load_customers_data()
                else:
                    current_debt = float(old_debt) + current_debt
                    customer.customer_debt = current_debt

                    self.create_sale_document(session, customer)
                    self.create_payment(old_debt, current_debt, session, 'up')

                    session.commit()

                    self.reset_checkout_table()
                    self.clear_customer()

                    document = session.query(Documents).order_by(Documents.id.desc()).first()

            self.Payment.close()

            if button_name == 'Təsdiqlə':
                self.show_sale_document(document)
            else:
                QMessageBox.information(self, AppName, 'Müştəri borcu yeniləndi')
        else:
            QMessageBox.critical(self.Payment, AppName, result)

    def open_payment_window(self, search_index, info):
        label_name = 'Ümumi Borc'
        button_name = 'Yenilə'

        if not search_index:
            QMessageBox.critical(self, AppName, 'Müştəri təyin olumayıb!')
            self.input_filtr_customer.setFocus()
            return

        with Session() as session:
            if info == 'id':
                customer = session.query(Customers).filter(Customers.id == search_index).first()
            else:
                customer = session.query(Customers).filter((Customers.customer_name.like(f"%{search_index}%")) | (
                    Customers.customer_phone_1.like(f"%{search_index}%"))).first()

            if customer is None:
                QMessageBox.critical(self, AppName, 'Müştəri tapılmadı!')
                self.input_filtr_customer.clear()
                self.input_filtr_customer.setFocus()
                return

            self.Payment_GUI.label_username.setText(customer.customer_name)
            self.Payment_GUI.label_customer_id.setText(str(customer.id))
            self.Payment_GUI.label_total.setText(label_name)
            self.Payment_GUI.button_add.setText(button_name)

            self.Payment_GUI.input_total.setText(str(customer.customer_debt))
            self.Payment_GUI.input_paid.setText('0')
            self.Payment_GUI.input_debt.setReadOnly(False)
            self.Payment_GUI.input_debt.setText(str(customer.customer_debt))
            self.Payment_GUI.payment_calendar.setDate(customer.customer_payment_date)

            self.Payment_GUI.input_paid.textChanged.connect(self.update_debt)

            self.Payment.exec_()
            self.input_filtr_customer.setFocus()

    def update_debt(self):
        total_text = self.Payment_GUI.input_total.text()
        paid_text = self.Payment_GUI.input_paid.text()

        try:
            total = float(total_text) if total_text else 0.0
            paid = float(paid_text) if paid_text else 0.0

            if total < 0 or paid < 0 or total < paid:
                self.Payment_GUI.input_debt.setText("Hesab xətası!")
                return

            debt = total - paid

            self.Payment_GUI.input_debt.setText(f"{debt:.2f}")
        except ValueError:
            self.Payment_GUI.input_debt.setText("Hesab xətası!")

    ############# CUSTOMERS ###########################################
    ###################################################################
    def create_and_add_customer(self):
        if self.create_or_update_customer(True) is True:
            with Session() as session:
                customer = session.query(Customers).order_by(Customers.id.desc()).first()

            self.choose_customer(customer)

    def create_or_update_customer(self, info):
        customer_id = self.Customer_GUI.label_customer_id.text()
        customer_name = self.Customer_GUI.input_name.text().strip()
        customer_phone_1 = self.Customer_GUI.input_phone_1.text().strip()
        customer_phone_2 = self.Customer_GUI.input_phone_2.text().strip()
        customer_address = self.Customer_GUI.input_address.text().strip()
        customer_level = 'loyal' if self.Customer_GUI.checkBox_level_customer.isChecked() else 'standart'

        validator = CustomerFormValidator(customer_name, customer_phone_1, customer_address)
        result = validator.validate()

        if result is True:
            with Session() as session:

                if not customer_phone_2:
                    customer_phone_2 = "yoxdur"

                existing_customer = session.query(Customers).filter(
                    Customers.customer_name == customer_name,
                    Customers.customer_address == customer_address
                ).first()

                if customer_id:
                    if existing_customer:
                        if existing_customer.id == int(customer_id):
                            pass
                        else:
                            QMessageBox.critical(self.Customer, AppName, "Bu məlumat artıq istifadə olunub.")
                            if info is True:
                                return False
                            else:
                                return
                    message = 'Müştəri məlumatları uğurla yeniləndi.'
                    customer = session.query(Customers).filter(Customers.id == customer_id).first()
                else:
                    if existing_customer:
                        QMessageBox.critical(self.Customer, AppName, "Bu məlumat artıq istifadə olunub.")
                        if info is True:
                            return False
                        else:
                            return

                    customer = Customers()
                    message = 'Müştəri uğurla əlavə edildi.'
                    customer.customer_payment_date = datetime.now().date()

                customer.customer_name = customer_name
                customer.customer_phone_1 = customer_phone_1
                customer.customer_phone_2 = customer_phone_2
                customer.customer_address = customer_address
                customer.customer_level = customer_level

                session.add(customer)
                session.commit()

                self.Customer.close()
                self.load_customers_data()

                if info is True:
                    return True
                else:
                    QMessageBox.information(self.Customer, AppName, message)
        else:
            QMessageBox.critical(self.Customer, AppName, result)
            if info is True:
                return False

    def open_customer_window(self, customer):
        if not customer:
            self.Customer_GUI.label_customer_id.clear()
            self.Customer_GUI.input_name.clear()
            self.Customer_GUI.input_phone_1.clear()
            self.Customer_GUI.input_phone_2.clear()
            self.Customer_GUI.input_address.clear()
            self.Customer_GUI.checkBox_level_customer.setChecked(False)
            self.Customer_GUI.button_add.setText('Təsdiqlə')
            self.Customer_GUI.button_add_and_create.show()
            self.Customer_GUI.label_add_customer.setText('Müştəri əlavə et')
            self.Customer_GUI.button_delete.hide()
        else:

            self.Customer_GUI.label_customer_id.setText(str(customer.id))
            self.Customer_GUI.input_name.setText(customer.customer_name)
            self.Customer_GUI.input_phone_1.setText(customer.customer_phone_1)
            self.Customer_GUI.input_phone_2.setText(customer.customer_phone_2)
            self.Customer_GUI.input_address.setText(customer.customer_address)
            self.Customer_GUI.button_add.setText('Yenilə')
            self.Customer_GUI.button_add_and_create.hide()
            self.Customer_GUI.button_delete.show()
            self.Customer_GUI.label_add_customer.setText('Məlumatları yenilə')

            if customer.customer_level == 'loyal':
                level = True
            else:
                level = False

            self.Customer_GUI.checkBox_level_customer.setChecked(level)

        self.Customer.exec_()

    def delete_customer(self):
        id = self.Customer_GUI.label_customer_id.text()
        with Session() as session:
            customer = session.query(Customers).filter(Customers.id == id).first()
            reply = QMessageBox.question(self, AppName,
                                         f'{customer.customer_name} adlı müştəri silinsin?',
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

            if reply == QMessageBox.Yes:
                session.delete(customer)
                session.commit()

                self.Customer.close()
                QMessageBox.information(self, AppName, 'Müştəri uğurla silindi')
                self.load_customers_data()
            else:
                pass

    def load_customers_data(self):

        filter_level = str(self.combobox_level_customer.currentText()).lower()

        search_index = str(self.input_filtr_customer.text())

        with Session() as session:
            if search_index:
                if filter_level == 'müştərilər':
                    all_customers = session.query(Customers).filter(
                        (Customers.customer_name.like(f"%{search_index}%")) |
                        (Customers.customer_phone_1.like(f"%{search_index}%"))).order_by(
                        Customers.customer_payment_date).all()
                else:
                    all_customers = session.query(Customers).filter(
                        (Customers.customer_name.like(f"%{search_index}%")) |
                        (Customers.customer_phone_1.like(f"%{search_index}%")),
                        Customers.customer_level == filter_level).order_by(Customers.customer_payment_date).all()
            else:
                if filter_level == 'müştərilər':
                    all_customers = session.query(Customers).order_by(Customers.customer_payment_date).all()
                else:
                    all_customers = session.query(Customers).filter(Customers.customer_level == filter_level).order_by(
                        Customers.customer_payment_date).all()

            self.clear_tables()
            self.table_customers.setRowCount(len(all_customers))

            for row_index, customer in enumerate(all_customers):

                self.table_customers.setItem(row_index, 0, QTableWidgetItem(str(customer.id)))

                name = QTableWidgetItem(customer.customer_name)
                name.setForeground(QBrush(QColor('#006EFF')))

                self.table_customers.setItem(row_index, 1, name)
                self.table_customers.setItem(row_index, 2, QTableWidgetItem(customer.customer_address))
                self.table_customers.setItem(row_index, 3, QTableWidgetItem(customer.customer_phone_1))
                self.table_customers.setItem(row_index, 4, QTableWidgetItem(customer.customer_phone_2))
                self.table_customers.setItem(row_index, 5, QTableWidgetItem(customer.customer_level))

                debt = float(customer.customer_debt)

                customer_debt = QTableWidgetItem(str(debt))
                customer_debt.setForeground(QBrush(QColor('#006EFF')))
                self.table_customers.setItem(row_index, 6, customer_debt)

                date_string = customer.customer_payment_date.strftime('%d.%m.%Y')
                date_item = QTableWidgetItem(date_string)
                difference = (customer.customer_payment_date - datetime.now().date()).days

                if 5 < difference <= 10 and debt != 0:
                    date_item.setForeground(QBrush(QColor("#6d0000")))
                elif 0 < difference <= 5 and debt != 0:
                    date_item.setForeground(QBrush(QColor("#b80000")))
                elif difference <= 0 and debt != 0:
                    date_item.setForeground(QBrush(QColor("#ff0000")))
                else:
                    date_item.setForeground(QBrush(QColor("black")))

                self.table_customers.setItem(row_index, 7, date_item)

                edit = QTableWidgetItem()
                icon_pixmap = QPixmap(f':/icons/edit.png')
                edit.setIcon(QIcon(icon_pixmap))
                self.table_customers.setItem(row_index, 8, edit)

            self.table_customers.setColumnHidden(0, True)
            self.table_customers.setColumnWidth(1, 150)
            self.table_customers.setColumnWidth(2, 200)
            self.table_customers.setColumnWidth(8, 20)

    def on_customer_click(self, row, column):
        customer_id = self.table_customers.item(row, 0).text()
        if column == 1:
            customer = self.get_customer_by_id(customer_id)
            self.choose_customer(customer)

        elif column == 6:
            self.open_payment_window(customer_id, 'id')

        elif column == 8:
            customer = self.get_customer_by_id(customer_id)
            self.open_customer_window(customer)

    def get_customer_by_id(self, customer_id):
        with Session() as session:
            return session.query(Customers).filter(Customers.id == customer_id).first()

    ############################################################
    ############################################################
    def export_to_excel(self, table):
        with Session() as session:
            if table == 'customers':
                data = session.query(Customers).order_by(Customers.customer_name.desc()).all()

                data_list = [{
                    'Müştəri': customer.customer_name,
                    'Telefon 1': customer.customer_phone_1,
                    'Telefon 2': customer.customer_phone_2,
                    'Ünvan': customer.customer_address,
                    'Kateqoriya': customer.customer_level,
                    'Borc': customer.customer_debt,
                    'Ödəniş Tarixi': customer.customer_payment_date
                } for customer in data]

                df = pd.DataFrame(data_list)

            elif table == 'products':
                data = session.query(Products).order_by(Products.product_name.desc()).all()

                data_list = [{
                    'Məhsul': product.product_name,
                    'Miqdar': product.product_quantity,
                    'Alış Qiyməti': product.product_buy_price,
                    'Satış Qiyməti': product.product_sale_price,
                    'Barkod': product.product_barcode,
                    'Tarix': product.date
                } for product in data]

                df = pd.DataFrame(data_list)

            options = QFileDialog.Options()
            file_name, _ = QFileDialog.getSaveFileName(self, "Faylı saxla", "", "Excel Faylı (*.xlsx);",
                                                       options=options)

            if file_name:
                if not file_name.endswith('.xlsx'):
                    file_name += '.xlsx'
                try:
                    df.to_excel(file_name, index=False)
                    QMessageBox.information(self, AppName, f'Məlumat uğurla qeyd edildi!')
                except Exception as e:
                    QMessageBox.critical(self, AppName, f"Məlumatı Excel'ə köçürərkən xəta baş verdi!: {e}")

    def closeEvent(self, event):
        reply = self.confirm_exit()
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def confirm_exit(self):
        reply = QMessageBox.question(self, AppName,
                                     'Çıxış etmək istədiyinizdən əminsiniz?',
                                     QMessageBox.Yes | QMessageBox.No,
                                     QMessageBox.No)

        if reply == QMessageBox.Yes:
            QApplication.quit()
        else:
            pass

    def about_app(self):
        about = f"""\n
        Proqram: {AppName}.
        Açıqlama: Kassa-Satış proqramı.
        Versiya: {AppVersion}.
        Son Yenilənmə Tarixi: {LastUpdate}.
        Əməliyyat Sistemi: Windows.
        -----------------------------------------------
        {LegalCopyright}\n
        {Website}\n

        """
        QMessageBox.information(self, AppName, about)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = Main()
    main_window.show()
    sys.exit(app.exec_())
