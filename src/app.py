import pandas as pd
import sys
from db_connect import *

from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QIcon, QPixmap, QBrush, QColor, QFont, QTextDocument
from PyQt5.QtPrintSupport import QPrinter, QPrintDialog
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QFileDialog, QDialog,QTableWidgetItem
from fpdf import FPDF

from forms import ProductFormValidator, CustomerFormValidator, CheckOutFormValidator, PaymentFormValidator, LicenseManager
from info import AppName, AppVersion, LastUpdate, LegalCopyright, Website

from ui_pycode.stakeholder import Ui_Stakeholder
from ui_pycode.main import Ui_Main
from ui_pycode.payment import Ui_Payment
from ui_pycode.price import Ui_Price
from ui_pycode.product import Ui_Product
from ui_pycode.document import Ui_Document
from ui_pycode.list import Ui_List


class Main(QMainWindow, Ui_Main):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self._customer = 'Müştəri'
        self._supplier = 'Tədarükçü'
        self.setup_stakeholders_dialog()
        self.setup_products_dialog()
        self.setup_payments_dialog()
        self.setup_documents_dialog()
        self.setup_list_dialog()
        self.setup_sale_page_dialog()
        self.setup_license()
        self.setup_timers()
        self.setup_buttons()
        self.setup_window()

    def setup_window(self):
        self.setWindowFlags(QtCore.Qt.Window | QtCore.Qt.FramelessWindowHint)
        self.setWindowTitle(AppName)
        self.showFullScreen()
        self.icon_name_widget.setHidden(True)
        self.reset_documents_table()
        self.switch_to_sale_page()

    # Connect buttons
    def setup_buttons(self):
        button_page_map = {
            self.button_sale_1: 'sale',
            self.button_sale_2: 'sale',
            self.button_product_1: 'products',
            self.button_product_2: 'products',
            self.button_document_1: 'documents',
            self.button_document_2: 'documents',
            self.button_movement_1: 'movements',
            self.button_movement_2: 'movements',
            self.button_stakeholder_1: 'stakeholder',
            self.button_stakeholder_2: 'stakeholder',
        }

        for button, page in button_page_map.items():
            button.clicked.connect(lambda _, p=page: self.switch_to_page(p))

        self.button_info_1.clicked.connect(self.about_app)
        self.button_info_2.clicked.connect(self.about_app)
        self.button_exit_1.clicked.connect(self.confirm_exit) 
        self.button_exit_2.clicked.connect(self.confirm_exit)


    # SALE PAGE WINDOW
    def setup_sale_page_dialog(self):
        self.button_sale.clicked.connect(self.calculate_sale)
        self.button_search_product.clicked.connect(self.search_sale_product)
        self.button_choose_customer.clicked.connect(lambda: self.open_list_window('customer'))
        self.button_choose_product.clicked.connect(lambda: self.open_list_window('product_for_sale'))
        self.button_clear_customer.clicked.connect(self.clear_customer)
        self.label_total_sale_price.setText('0.0')
        self.table_sale.cellDoubleClicked.connect(self.on_checkout_click)
        self.clear_customer()
        

    # STAKEHOLDERS WINDOW
    def setup_stakeholders_dialog(self):
        self.Stakeholder, self.Stakeholder_GUI = self.create_dialog(Ui_Stakeholder)
        self.button_filtr_stakeholder.clicked.connect(lambda: self.open_payment_window(search_index=self.input_filtr_stakeholder.text(), info='search'))
        self.button_export_excel_stakeholder.clicked.connect(lambda: self.export_to_excel('stakeholders'))
        self.button_new_stakeholder.clicked.connect(lambda: self.open_stakeholders_window('normal', None))
        self.table_stakeholders.cellDoubleClicked.connect(self.on_stakeholder_click)
    
        self.Stakeholder_GUI.button_delete.clicked.connect(self.delete_stakeholder)
        self.Stakeholder_GUI.button_add.clicked.connect(self.create_or_update_stakeholder)
        self.Stakeholder_GUI.button_cancel.clicked.connect(self.Stakeholder.close)


    # PRODUCTS WINDOW
    def setup_products_dialog(self):
        self.Product, self.Product_GUI = self.create_dialog(Ui_Product)
        self.button_export_excel_products.clicked.connect(lambda: self.export_to_excel('products'))
        self.button_filtr_product.clicked.connect(lambda: self.filtr_product(self.input_filtr_product.text()))
        self.button_new_product.clicked.connect(lambda: self.open_product_window(product=None, info='create'))
        self.Product_GUI.button_generate_barcode.clicked.connect(self.generate_ean13_barcode)
        self.Product_GUI.button_delete.clicked.connect(self.delete_product)
        self.Product_GUI.button_add.clicked.connect(self.create_or_update_product)
        self.Product_GUI.button_cancel.clicked.connect(self.Product.close)

        # Product Price Window
        self.Price, self.Price_GUI = self.create_dialog(Ui_Price)
        self.Price_GUI.button_add.clicked.connect(self.edit_checkout_product)
        self.Price_GUI.button_cancel.clicked.connect(self.Price.close)
        self.table_products.cellDoubleClicked.connect(self.on_product_click)


    # DOCUMENTS WINDOW
    def setup_documents_dialog(self):
        self.Document, self.Document_GUI = self.create_dialog(Ui_Document)
        self.Document_GUI.button_search_product.clicked.connect(lambda: self.open_product_window(product=self.Document_GUI.input_search_product.text(), info='add'))
        self.Document_GUI.button_choose_stakeholder.clicked.connect(lambda: self.open_list_window('document_type'))
        self.Document_GUI.button_choose_product.clicked.connect(lambda: self.open_list_window('product'))
        self.Document_GUI.button_export_excel_document.clicked.connect(lambda: self.export_to_excel('documents'))
        self.Document_GUI.button_delete.clicked.connect(self.delete_document)
        self.Document_GUI.button_add.clicked.connect(self.make_manual_document)
        self.Document_GUI.button_cancel.clicked.connect(self.Document.close)
        self.Document_GUI.table_products.cellDoubleClicked.connect(self.on_checkin_click)
        self.button_new_document.clicked.connect(lambda: self.open_document_window(info='new', document=None))
        self.button_choose_stakeholder.clicked.connect(lambda: self.open_list_window('stakeholders'))
        self.button_clear_stakeholder.clicked.connect(lambda: self.clear_stakeholder_filter('documents'))
        self.table_documents.cellDoubleClicked.connect(self.on_document_click)

    # LIST WINDOW
    def setup_list_dialog(self):
        self.List, self.List_GUI = self.create_dialog(Ui_List)
        self.List_GUI.button_new.clicked.connect(self.create_new_product_or_stakeholder)
        self.List_GUI.button_close.clicked.connect(self.List.close)
        self.List_GUI.table_list.cellDoubleClicked.connect(self.on_list_click)

    # PAYMENTS WINDOW
    def setup_payments_dialog(self):
        self.Payment, self.Payment_GUI = self.create_dialog(Ui_Payment)
        self.Payment_GUI.button_add.clicked.connect(self.make_process)
        self.Payment_GUI.button_cancel.clicked.connect(self.Payment.close)
        self.button_movement_choose_stakeholder.clicked.connect(lambda: self.open_list_window('stakeholders_movements'))
        self.button_movement_clear_stakeholder.clicked.connect(lambda: self.clear_stakeholder_filter('movements'))
        self.table_movements.cellDoubleClicked.connect(self.delete_movement)

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
            'supplier_search': (self.load_stakeholders_data, self.input_filtr_stakeholder.textChanged),
            'list_search': (self.load_list_data, self.List_GUI.input_search.textChanged),
            'product_search': (self.load_products_data, self.input_filtr_product.textChanged),
        }

        # Create and connect timers based on the configurations
        for name, (callback, signal) in timer_configs.items():
            timer = QTimer(self)
            timer.setSingleShot(True)
            timer.timeout.connect(callback)
        
            signal.connect(lambda _, t=timer: t.start(300))

        # Special case for the combo box timer
        self.document_combobox_timer = QTimer(self)
        self.document_combobox_timer.setSingleShot(True)
        self.document_combobox_timer.timeout.connect(self.load_documents_data)
        self.combobox_type_documents.currentIndexChanged.connect(lambda: self.document_combobox_timer.start(300))

        self.stakeholder_combobox_timer = QTimer(self)
        self.stakeholder_combobox_timer.setSingleShot(True)
        self.stakeholder_combobox_timer.timeout.connect(self.load_stakeholders_data)
        self.combobox_type_stakeholders.currentIndexChanged.connect(lambda: self.stakeholder_combobox_timer.start(300))


    ############## SWITCH PAGES ###########################
    #######################################################
    def switch_to_page(self, page):
        if page == 'sale':
            self.switch_to_sale_page()
        elif page == 'stakeholder':
            self.switch_to_stakeholders_page()
        elif page == 'products':
            self.switch_to_product_page()
        elif page == 'documents':
            self.switch_to_document_page()
        elif page == 'movements':
            self.switch_to_movement_page()
            

    def switch_to_sale_page(self):
        if self.switch_to_license_page():
            self.button_sale_1.setChecked(not self.button_sale_1.isChecked())
            self.stackedWidget.setCurrentIndex(0)
            self.load_checkout_products()
            self.input_search_product.clear()
            self.input_search_product.setFocus()

    def switch_to_stakeholders_page(self):
        if self.switch_to_license_page():
            self.stackedWidget.setCurrentIndex(1)
            self.input_filtr_stakeholder.clear()
            self.input_filtr_stakeholder.setFocus()
            self.load_stakeholders_data()

    def switch_to_product_page(self):
        if self.switch_to_license_page():
            self.stackedWidget.setCurrentIndex(2)
            self.input_filtr_product.clear()
            self.input_filtr_product.setFocus()
            self.load_products_data()

    def switch_to_document_page(self):
        if self.switch_to_license_page():
            self.stackedWidget.setCurrentIndex(3)
            self.label_document_stakeholder.clear()
            self.label_document_stakeholder_id.clear()
            self.button_clear_stakeholder.hide()
            self.load_documents_data()


    def switch_to_movement_page(self):
        if self.switch_to_license_page():
            self.stackedWidget.setCurrentIndex(4)
            self.label_movement_stakeholder.clear()
            self.label_movement_stakeholder_id.clear()
            self.button_movement_clear_stakeholder.hide()
            self.load_movements_data()

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
            self.button_product_1, self.button_product_2,
            self.button_stakeholder_1, self.button_stakeholder_2,
            self.button_document_1, self.button_document_2,
            self.button_movement_1, self.button_movement_2,
            self.button_settings_1, self.button_settings_2,
            self.button_cash_register_1, self.button_cash_register_2,
            self.button_users_1, self.button_users_2
        ]

        for button in buttons:
            button.setEnabled(is_enabled)

    ############ LICENSE #################################################################################
    ######################################################################################################
    def check_license(self):
        license_manager = LicenseManager()
        with Session() as session:
            current_license = session.query(License).first()

            if current_license:
                is_valid = license_manager.validate_license_key(current_license.app_license)
                # return is_valid  # Activate License
                return True  # Bypass License
            else:
                # return None
                return True  # Bypass License

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
        else:
            pass


    ############ LIST WINDOW ####################################################################################################
    #############################################################################################################################
    def open_list_window(self, list_type):
        self.List_GUI.label_list_type.clear()
        if list_type == 'document_type':
            list_type = 'supplier' if self.Document_GUI.combobox_document_type.currentText() == 'Alış'  else 'customer'

        self.List_GUI.label_list_type.setText(list_type)
        self.load_list_data()
        self.List.exec_()


    def load_list_data(self):
        list_type = self.List_GUI.label_list_type.text()
        if list_type == 'stakeholders' or list_type == 'stakeholders_movements':
            header = 'Kontragentlər'
            DB_Table = Stakeholders
        elif list_type == 'supplier':
            header = 'Tədarükçülər'
        elif list_type == 'customer':
            header = 'Müştərilər'
        elif list_type == 'customers':
            header = 'Müştərilər'
            list_type = 'customer'
        else:
            header = 'Məhsullar'
            DB_Table = Products

        search_index = str(self.List_GUI.input_search.text())

        with Session() as session:
            if search_index:
                if list_type == 'supplier' or list_type == 'customer':
                    all = session.query(Stakeholders).filter((Stakeholders.name.like(f"%{search_index}%")), (Stakeholders.type == list_type)).order_by(Stakeholders.name.desc()).limit(500).all()
                else:
                    all = session.query(DB_Table).filter(DB_Table.name.like(f"%{search_index}%")).order_by(DB_Table.name.desc()).limit(500).all()
            else:
                if list_type == 'supplier' or list_type == 'customer':
                    all = session.query(Stakeholders).filter(Stakeholders.type == list_type).order_by(Stakeholders.name.desc()).limit(500).all()
                else:
                    all = session.query(DB_Table).order_by(DB_Table.name.desc()).limit(500).all()

            self.List_GUI.table_list.setRowCount(len(all))

            for row_index, item in enumerate(all):
                self.List_GUI.table_list.setItem(row_index, 0, QTableWidgetItem(str(item.id)))
                self.List_GUI.table_list.setItem(row_index, 1, QTableWidgetItem(str(item.name)))

            self.List_GUI.table_list.setHorizontalHeaderItem(1, QTableWidgetItem(header))
            self.List_GUI.table_list.setColumnHidden(0, True)
    

    def on_list_click(self, row, column):
        element_id = self.List_GUI.table_list.item(row, 0).text()
        list_type = self.List_GUI.label_list_type.text()
        if list_type == 'product' or list_type == 'product_for_sale':
            element=self.get_element_by_id(element_id, Products)
            if list_type == 'product':
                if self.Document_GUI.combobox_document_type.currentText() == 'Alış':
                    self.List.close()
                    self.open_product_window(product=element.name, info='add')
                else:
                    with Session() as session:
                        product_price = session.query(ProductMovements).filter(
                            ProductMovements.product_id == element.id, 
                            ProductMovements.movement_type == 0).order_by(ProductMovements.created_date.desc()).first() 
                        if product_price:
                            self.List.close()
                            self.open_product_window(product=element.name, info='add')
                        else:
                            QMessageBox.critical(self.Document, AppName, 'Məhsul satış qiyməti təyin edilməyib!')
                            return
                
            else:
                self.input_search_product.setText(element.barcode)
                self.search_sale_product()
                self.List.close()
        else:
            element=self.get_element_by_id(element_id, Stakeholders)
            if list_type == 'supplier':
                self.Document_GUI.label_stakeholder.setText(element.name)
                self.Document_GUI.label_stakeholder_id.setText(str(element.id))
                self.List.close()
            elif list_type == 'customer':
                if self.Document_GUI.combobox_document_type.currentText() == 'Alış':
                    self.label_customer.setText(element.name)
                    self.label_customer_id.setText(str(element_id))
                    self.button_clear_customer.show()
                else:
                    self.Document_GUI.label_stakeholder.setText(element.name)
                    self.Document_GUI.label_stakeholder_id.setText(str(element.id))
                self.List.close()
            elif list_type == 'stakeholders':
                self.label_document_stakeholder.setText(element.name)
                self.label_document_stakeholder_id.setText(str(element_id))
                self.button_clear_stakeholder.show()
                self.load_documents_data()
                self.List.close()
            elif list_type == 'stakeholders_movements':
                self.label_movement_stakeholder.setText(element.name)
                self.label_movement_stakeholder_id.setText(str(element_id))
                self.button_movement_clear_stakeholder.show()
                self.load_movements_data()
                self.List.close()
            else:
                pass


    def create_new_product_or_stakeholder(self):
        list_type = self.List_GUI.label_list_type.text()
        if list_type == 'product' or list_type == 'product_for_sale':
            self.open_product_window(product=None, info='create')
        else:
            self.open_stakeholders_window('list', None)


    ############ DOCUMENTS #############################################################################################################
    ####################################################################################################################################
    def open_document_window(self, info, document):
        with Session() as session:
            session.query(CheckIn).delete()
            session.commit()
            if info == 'update':
                document_date = document.created_date.strftime(r'%d.%m.%Y - %H:%M:%S')
                self.Document_GUI.label_date.setText(document_date)
                self.Document_GUI.label_document_number.setText(str(document.id))
                self.Document_GUI.label_warhouse.setText(document.warhouse)
                self.Document_GUI.button_add.setText('Yenilə')
                document_type = 'Alış' if document.document_type == 0 else 'Satış'
                self.Document_GUI.combobox_document_type.setCurrentText(document_type)
                self.Document_GUI.combobox_document_type.setEnabled(False)
                self.Document_GUI.button_delete.show()
                self.Document_GUI.button_export_excel_document.show()

                # Get Stakeholder from Stakeholders
                stakeholder = session.query(Stakeholders).filter(Stakeholders.id == document.stakeholder_id).first()

                # Write Stakeholder info
                self.Document_GUI.label_stakeholder.setText(str(stakeholder.name))
                self.Document_GUI.label_stakeholder_id.setText(str(document.stakeholder_id))

                # Write Document note
                self.Document_GUI.input_note.setText(str(document.note))

                # Get document products from ProductsMovements
                document_products = session.query(ProductMovements).filter(ProductMovements.document_id == document.id).limit(500).all()

                # Write Products in Document table
                for product in document_products:
                    product_info = session.query(Products).filter(Products.id == product.product_id).first()
                    product_in_table = CheckIn(
                        product_id = product.product_id,
                        product_movement_id = product.id,
                        name = product_info.name,
                        quantity = product.quantity,
                        price = product.purchase_price,
                        sale_price = product.sale_price,
                        barcode = product_info.barcode,
                        unit = product_info.unit
                    )
                    session.add(product_in_table)

                session.commit()

            else:
                document = session.query(Documents).order_by(Documents.id.desc()).first()
                if document:
                    document_id = document.id+1
                    document_warhouse = document.warhouse
                else:
                    document_id = 1
                    document_warhouse = 'Əsas'
                current_date = datetime.now().strftime(r'%d.%m.%Y - %H:%M:%S')
                self.Document_GUI.label_date.setText(str(current_date))
                self.Document_GUI.label_document_number.setText(str(document_id))
                self.Document_GUI.label_warhouse.setText(document_warhouse)
                self.Document_GUI.button_add.setText('Təsdiqlə')
                self.Document_GUI.combobox_document_type.setCurrentText('Alış')
                self.Document_GUI.combobox_document_type.setEnabled(True)
                self.Document_GUI.button_delete.hide()
                self.Document_GUI.button_export_excel_document.hide()

                self.Document_GUI.label_stakeholder.clear()
                self.Document_GUI.label_stakeholder_id.clear()
                self.Document_GUI.label_total_price.clear()
                self.Document_GUI.label_total_sale_price.clear()

        self.load_checkin_products()
        self.Document.exec_()
        self.Document_GUI.combobox_document_type.setCurrentText('Alış')


    def make_process(self):
        button_name = self.Payment_GUI.button_add.text()
        if button_name == 'Yenilə':
            self.make_payment()
        else:
            self.make_sale_document()

            # GENERATE SALE CHECK
            # with Session() as session:
            #     sales_products = session.query(CheckOut).limit(500).all()
            #     customer_id = self.Payment_GUI.label_id.text()
            #     customer = session.query(Stakeholders).filter(Stakeholders.id == customer_id).first()


    def make_manual_document(self):

        if not self.Document_GUI.label_stakeholder_id.text().strip():
            QMessageBox.critical(self.Document, AppName, 'Kontragent seçilməyib!')
            return
        
        if round(float(self.Document_GUI.label_total_price.text()), 2) <= 0.0:
            QMessageBox.critical(self.Document, AppName, 'Məhsul daxil edilməyib!')
            return
        
        with Session() as session:
            document_id = self.Document_GUI.label_document_number.text()
            document_type = self.Document_GUI.combobox_document_type.currentText()

            # Write Documents
            if self.Document_GUI.button_add.text() == 'Yenilə':
                document =  session.query(Documents).filter(Documents.id == document_id).first()
                stakeholder_movement = session.query(StakeholderMovements).filter(StakeholderMovements.document_id == document_id).first()
                paid = stakeholder_movement.paid
                warhouse = self.Document_GUI.label_warhouse.text()
            else:
                document = Documents()
                stakeholder_movement = StakeholderMovements()
                paid = 0.0
                warhouse = 'Əsas'


            if document_type == 'Alış':
                document_type = 0
                product_movement_type = 0
                total = self.Document_GUI.label_total_price.text()
            elif document_type == 'Satış':
                document_type = 1
                product_movement_type = 1
                total = self.Document_GUI.label_total_sale_price.text()
            else:
                QMessageBox.critical(self.Document, AppName, 'Sənəd tipi düzgün deyil!')
                return

            debt = round(float(total)) - float(paid)
            
            self.create_or_update_document(
                session, 
                document, 
                self.Document_GUI.label_stakeholder_id.text(), 
                total,
                warhouse, 
                self.Document_GUI.input_note.text(), 
                document_type
                )

            # Write Product Movements
            sales_products = session.query(CheckIn).limit(500).all()
            for product in sales_products:
                if product.delete_status == 1:
                    movement = session.query(ProductMovements).filter(ProductMovements.id  == product.product_movement_id).first()
                    if movement:
                        session.delete(movement)
                        session.commit()
                        self.calculate_product_quantity(product.id)
                else:
                    if product.product_movement_id == 0:
                        movement = ProductMovements()
                        movement.created_date = document.created_date
                    else:
                        movement = session.query(ProductMovements).filter(
                            ProductMovements.id == product.product_movement_id,
                            ProductMovements.document_id == document_id ).first()
                        
                    self.create_or_update_product_movement(
                        session, 
                        movement, 
                        product.product_id, 
                        self.Document_GUI.label_stakeholder_id.text(), 
                        document_id, 
                        product_movement_type, 
                        product.quantity, 
                        product.sale_price, 
                        product.price
                        )

            # Write Stakeholder Movements
            self.create_or_update_stakeholder_movement(  
                session,              
                stakeholder_movement, 
                self.Document_GUI.label_stakeholder_id.text(), 
                document_id, 
                0, 
                total,
                paid,
                debt
                )

        self.Document.close()
        self.load_documents_data()


    def make_sale_document(self):
        customer_id = self.Payment_GUI.label_id.text()

        validator = PaymentFormValidator(self.Payment_GUI.input_debt.text().strip(), self.Payment_GUI.input_paid.text().strip())
        result = validator.validate()

        if result is True:
            with Session() as session:
                customer = session.query(Stakeholders).filter(Stakeholders.id == customer_id).first()
                customer.payment_date = self.Payment_GUI.payment_calendar.date().toPyDate()
                document = session.query(Documents).order_by(Documents.id.desc()).first()
                document_id = document.id+1
                # Write Documents
                document = Documents()
                warhouse = 'Əsas'


                self.create_or_update_document(
                    session, 
                    document, 
                    customer_id,
                    self.Payment_GUI.input_total.text().strip(),
                    warhouse, 
                    '', 
                    1
                    )
                
                # Write Product Movements
                sales_products = session.query(CheckOut).limit(500).all()
                for product in sales_products:
                    if product.delete_status == 1:
                        movement = session.query(ProductMovements).filter(ProductMovements.id  == product.product_movement_id).first()
                        if movement:
                            session.delete(movement)
                            session.commit()
                            self.calculate_product_quantity(product.id)
                    else:
                        movement = ProductMovements()
                        movement.created_date = document.created_date
                            
                        self.create_or_update_product_movement(
                            session, 
                            movement, 
                            product.product_id, 
                            customer_id, 
                            document_id, 
                            1, 
                            product.quantity, 
                            product.sale_price, 
                            product.price
                            )
                

                # Write Stakeholder Movements
                stakeholder_movement = StakeholderMovements()

                self.create_or_update_stakeholder_movement(  
                    session,              
                    stakeholder_movement, 
                    customer_id, 
                    document_id, 
                    0, 
                    self.Payment_GUI.input_total.text().strip(),
                    self.Payment_GUI.input_paid.text().strip(),
                    self.Payment_GUI.input_debt.text().strip()
                    )
            

                session.query(CheckOut).delete()
                session.commit()

            self.Payment.close()
            self.clear_customer()
            self.load_checkout_products()
        else:
            QMessageBox.critical(self.Payment, AppName, result)


    def create_or_update_document(self, session, document, stakeholder_id, total, warhouse, note, document_type):
        document.stakeholder_id = stakeholder_id
        document.total = round(float(total), 2)
        document.warhouse = warhouse
        document.note = note
        document.document_type = document_type

        session.add(document)
        session.commit()


    def create_or_update_product_movement(self, session, movement, product_id, stakeholder_id, document_id, movement_type, quantity, sale_price, price):
        movement.product_id = product_id
        movement.stakeholder_id = stakeholder_id
        movement.document_id = document_id
        movement.movement_type = movement_type
        movement.quantity = quantity
        movement.sale_price = sale_price
        movement.purchase_price = price

        session.add(movement)
        session.commit()

        self.calculate_product_quantity(product_id)


    def create_or_update_stakeholder_movement(self, session, movement, stakeholder_id, document_id, movement_type, total, paid, debt):
        movement.stakeholder_id = stakeholder_id
        movement.document_id = document_id
        movement.movement_type = movement_type
        movement.total = round(float(total), 2)
        movement.paid = round(float(paid), 2)
        movement.debt = round(float(debt), 2)
        
        session.add(movement)
        session.commit()

        self.calculate_stakeholder_debt(stakeholder_id)


    def load_documents_data(self):
        document_type = self.combobox_type_documents.currentText()
        search_index = self.label_document_stakeholder_id.text()
        
        if document_type == 'Ümumi':
            pass
        elif document_type == 'Alış':
            document_type = 0
        else:
            document_type = 1   

        with Session() as session:
            if search_index:
                if document_type == 'Ümumi':
                    documents = session.query(Documents).filter(Documents.stakeholder_id == search_index).order_by(Documents.id.desc()).limit(500).all()
                else:                     
                    documents = session.query(Documents).filter(
                        (Documents.stakeholder_id == search_index),
                        (Documents.document_type == document_type)).order_by(Documents.id.desc()).limit(500).all()
            else:
                if document_type == 'Ümumi':
                    documents = session.query(Documents).order_by(Documents.id.desc()).limit(500).all()
                else:
                    documents = session.query(Documents).filter(Documents.document_type == document_type).order_by(Documents.id.desc()).limit(500).all()

            
            self.table_documents.setRowCount(len(documents))

            for row_index, document in enumerate(documents):
                stakeholder = session.query(Stakeholders).filter(Stakeholders.id == document.stakeholder_id).first()

                self.table_documents.setItem(row_index, 0, QTableWidgetItem(str(document.id)))

                document_type = 'Alış' if document.document_type == 0 else 'Satış'
                self.table_documents.setItem(row_index, 1, QTableWidgetItem(document_type))
                date_string = document.updated_date.strftime('%d.%m.%Y - %H:%M')
                self.table_documents.setItem(row_index, 2, QTableWidgetItem(date_string))
                self.table_documents.setItem(row_index, 3, QTableWidgetItem(stakeholder.name))
                self.table_documents.setItem(row_index, 4, QTableWidgetItem(str(document.total)))
                self.table_documents.setItem(row_index, 5, QTableWidgetItem(str(document.note)))

            self.table_documents.setColumnHidden(0, True)
            self.table_documents.setColumnWidth(1, 80)


    def on_document_click(self, row, column):
        document_id = self.table_documents.item(row, 0).text()
        document_type = self.table_documents.item(row,1).text()
        document = self.get_element_by_id(document_id, Documents)
        if document_type == 'Alış':
            self.open_document_window(info='update', document=document)
        else:
            self.open_document_window(info='update', document=document)


    def delete_document(self):
        id = self.Document_GUI.label_document_number.text()
        with Session() as session:
            element = session.query(Documents).filter(Documents.id == id).first()
            reply = QMessageBox.question(self, AppName,
                                         f'{id} nömrəli sənəd silinsin?',
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

            if reply == QMessageBox.Yes:
                products_document = session.query(ProductMovements).filter(ProductMovements.document_id == id).limit(500).all()
                for product in products_document:
                    session.delete(product)
                    session.commit()
                
                    self.calculate_product_quantity(product.product_id)
                
                stakeholders_document = session.query(StakeholderMovements).filter(StakeholderMovements.document_id == id).limit(500).all()
                for stakeholder in stakeholders_document:
                    session.delete(stakeholder)
                    session.commit()

                    self.calculate_stakeholder_debt(stakeholder.stakeholder_id)

                session.delete(element)
                session.commit()

                self.Document.close()
                self.load_documents_data()
            else:
                pass


    def clear_stakeholder_filter(self, info):
        if info == 'documents':
            self.label_document_stakeholder.clear()
            self.label_document_stakeholder_id.clear()
            self.button_clear_stakeholder.hide()
            self.load_documents_data()
        else:
            self.label_movement_stakeholder.clear()
            self.label_movement_stakeholder_id.clear()
            self.button_movement_clear_stakeholder.hide()
            self.load_movements_data()
            

    def reset_documents_table(self):
        with Session() as session:
            session.query(CheckOut).delete()
            session.query(CheckIn).delete()
            session.commit()


    ############ SALE AND PURCHASE #################################################################################
    ################################################################################################################
    def calculate_sale(self):
        self.Payment_GUI.button_add.show()
        id = self.label_customer_id.text()

        if not id:
            id = 1

        with Session() as session:
            sale_products = session.query(CheckOut).limit(500).all()
            if not sale_products:
                QMessageBox.critical(self, AppName, 'Satış üçün məhsul daxil edin!')
                return
            
            total = 0
            for product in sale_products:
                product_total_price = round(float(product.sale_price) * float(product.quantity), 2)
                total += + product_total_price

            customer = session.query(Stakeholders).filter(Stakeholders.id == id).first()

            self.Payment_GUI.label_type.setText(self._customer)
            self.Payment_GUI.label_username.setText(customer.name)
            self.Payment_GUI.label_id.setText(str(customer.id))
            self.Payment_GUI.button_add.setText('Təsdiqlə')

            self.Payment_GUI.input_total.setText(str(total))
            self.Payment_GUI.payment_calendar.setDate(customer.payment_date)

            if customer.id == 1:
                self.Payment_GUI.input_paid.setReadOnly(True)
                self.Payment_GUI.payment_calendar.setReadOnly(True)
                self.Payment_GUI.input_paid.setText(str(total))
                self.Payment_GUI.input_debt.setText(str(0.0))
            else:
                self.Payment_GUI.input_paid.setReadOnly(False)
                self.Payment_GUI.payment_calendar.setReadOnly(False)
                self.Payment_GUI.input_debt.setText(str(total))
                self.Payment_GUI.input_paid.setText(str(0))


            self.Payment_GUI.input_total.textChanged.connect(self.update_debt)
            self.Payment_GUI.input_paid.textChanged.connect(self.update_debt)

            self.Payment.exec_()
            

    def load_checkout_products(self):
        with Session() as session:
            products = session.query(CheckOut).limit(500).all()
            self.table_sale.setRowCount(len(products))

            product_count = 1
            total_sale_price = 0.0

            for row_index, product in enumerate(products):
                self.table_sale.setItem(row_index, 0, QTableWidgetItem(str(product.id)))
                self.table_sale.setItem(row_index, 1, QTableWidgetItem(str(product_count)))
                self.table_sale.setItem(row_index, 3, QTableWidgetItem(product.name))
                self.table_sale.setItem(row_index, 4, QTableWidgetItem(product.unit))
                self.table_sale.setItem(row_index, 5, QTableWidgetItem(str(product.quantity)))
                self.table_sale.setItem(row_index, 6, QTableWidgetItem(str(product.sale_price)))
                product_total_sale_price = round(float(product.quantity) * float(product.sale_price), 2)
                self.table_sale.setItem(row_index, 7, QTableWidgetItem(str(product_total_sale_price)))

                product_count += 1
                total_sale_price += product_total_sale_price

                delete = QTableWidgetItem()
                icon_pixmap = QPixmap(f':/icons/cross.png')
                delete.setIcon(QIcon(icon_pixmap))
                self.table_sale.setItem(row_index, 2, delete)

            self.label_total_sale_price.setText(f'{total_sale_price}')
            self.table_sale.setColumnHidden(0, True)
            self.table_sale.setColumnWidth(1, 20)
            self.table_sale.setColumnWidth(2, 30)


    def on_checkout_click(self, row, column):
        product_id = self.table_sale.item(row, 0).text()
        product = self.get_element_by_id(product_id, CheckOut)
        if column == 1:
            pass
        elif column == 2:
            self.remove_product_from_document(info='sale', product=product)
        else:
            self.Price_GUI.label_product.setText(product.name)
            self.Price_GUI.label_id.setText(str(product.product_id))
            self.Price_GUI.input_quantity.setText(str(self.table_sale.item(row, 5).text()))
            self.Price_GUI.input_price.setText(str(self.table_sale.item(row, 6).text()))
            self.Price.exec_()
            
            self.input_search_product.clear()
            self.input_search_product.setFocus()


    def search_sale_product(self):
        original_barcode = self.input_search_product.text()
        if not original_barcode:
            QMessageBox.critical(self, AppName, 'Məhsul barkodunu daxil edin!')
            self.input_search_product.setFocus()
            return
        
        if original_barcode.isdigit() == False:
            QMessageBox.critical(self, AppName, 'Məhsul barkodu düzgün deyil!')
            self.input_search_product.clear()
            self.input_search_product.setFocus()
            return

        converted_barcode = original_barcode[:-6] + "00000"
        check_digit = self.calculate_check_digit(converted_barcode)
        full_barcode = converted_barcode + str(check_digit)

        with Session() as session:
            product = session.query(Products).filter(Products.barcode == full_barcode).first()

            if product:
                if product.unit == 'kq':
                    weight_str = original_barcode[-6:-1] 
                    weight_kg = int(weight_str) / 1000
                    quantity = f"{weight_kg:.2f}"
                    if quantity == '0.00':
                        quantity = 1
                else:
                    quantity = 1
            else:
                product = session.query(Products).filter(Products.barcode == original_barcode).first()
                if product:
                    quantity = 1
                else:
                    QMessageBox.critical(self, AppName, 'Məhsul tapılmadı!')
                    self.input_search_product.clear()
                    self.input_search_product.setFocus()
                    return
                    
            if product.quantity <= 0:
                QMessageBox.information(self, AppName, f'Məhsulun anbar qalığı: {product.quantity}')
            else:
                pass
            product_in_checkout = session.query(CheckOut).filter(CheckOut.product_id == product.id).first()
            
            if product_in_checkout:
                new_checkout_product = product_in_checkout
                new_checkout_product.quantity += round(float(quantity), 2)
            else:
                product_price = session.query(ProductMovements).filter(
                    ProductMovements.product_id == product.id,
                    ProductMovements.movement_type == 0).order_by(ProductMovements.created_date.desc()).first() 
                if product_price:
                    new_checkout_product = CheckOut()
                    new_checkout_product.product_id = product.id
                    new_checkout_product.name = product.name
                    new_checkout_product.barcode = product.barcode
                    new_checkout_product.quantity = quantity
                    new_checkout_product.price = product_price.purchase_price
                    new_checkout_product.sale_price = product_price.sale_price
                    new_checkout_product.unit = product.unit
    
                else:
                    QMessageBox.critical(self, AppName, 'Məhsul qiyməti təyin olunmayıb!')
                    return
                
            session.add(new_checkout_product)
            session.commit()
            self.load_checkout_products()

        self.input_search_product.clear()
        self.input_search_product.setFocus()


    def edit_checkout_product(self):
        product_id = self.Price_GUI.label_id.text()
        price = self.Price_GUI.input_price.text().strip()
        quantity = self.Price_GUI.input_quantity.text().strip()

        validator = CheckOutFormValidator(quantity, price)
        result = validator.validate()
        if result is True:
            with Session() as session:
                product = session.query(CheckOut).filter(CheckOut.product_id == product_id).first()

                product.quantity = round(float(quantity), 2)
                product.sale_price= round(float(price), 2)

                session.add(product)
                session.commit()
                self.Price.close()
                self.load_checkout_products()
        else:
            QMessageBox.critical(self.Price, AppName, result)

        self.input_search_product.clear()
        self.input_search_product.setFocus()


    def load_checkin_products(self):
        with Session() as session:
            products = session.query(CheckIn).filter(CheckIn.delete_status == 0).limit(500).all()
            self.Document_GUI.table_products.setRowCount(len(products))
            
            total_price = 0.0
            total_sale_price = 0.0

            for row_index, product in enumerate(products):
                self.Document_GUI.table_products.setItem(row_index, 0, QTableWidgetItem(str(product.id)))
                self.Document_GUI.table_products.setItem(row_index, 2, QTableWidgetItem(product.name))
                self.Document_GUI.table_products.setItem(row_index, 3, QTableWidgetItem(str(product.barcode)))
                self.Document_GUI.table_products.setItem(row_index, 4, QTableWidgetItem(str(product.quantity)))
                self.Document_GUI.table_products.setItem(row_index, 5, QTableWidgetItem(str(product.unit)))
                self.Document_GUI.table_products.setItem(row_index, 6, QTableWidgetItem(str(product.price)))
                product_total_price = round(float(product.quantity) * float(product.price), 2)
                self.Document_GUI.table_products.setItem(row_index, 7, QTableWidgetItem(str(product_total_price)))
                product_total_sale_price = round(float(product.quantity) * float(product.sale_price), 2)
                self.Document_GUI.table_products.setItem(row_index, 8, QTableWidgetItem(str(product.sale_price)))
                self.Document_GUI.table_products.setItem(row_index, 9, QTableWidgetItem(str(product_total_sale_price)))

                total_price += product_total_price
                total_sale_price += product_total_sale_price

                delete = QTableWidgetItem()
                icon_pixmap = QPixmap(f':/icons/cross.png')
                delete.setIcon(QIcon(icon_pixmap))
                self.Document_GUI.table_products.setItem(row_index, 1, delete)

            self.Document_GUI.label_total_price.setText(f'{total_price}')
            self.Document_GUI.label_total_sale_price.setText(f'{total_sale_price}')
            self.Document_GUI.table_products.setColumnHidden(0, True)
            self.Document_GUI.table_products.setColumnWidth(1, 20)


    def on_checkin_click(self, row, column):
        product_id = self.Document_GUI.table_products.item(row, 0).text()
        product = self.get_element_by_id(product_id, CheckIn)
        if column == 1:
            self.remove_product_from_document(info='buy', product=product)
        else:
            self.open_product_window(product=product, info='update')


    def remove_product_from_document(self, info, product):
        with Session() as session:
            if info == 'sale':
                session.delete(product)
                session.commit()
                self.load_checkout_products()
            else:
                product.delete_status = 1
                session.add(product)
                session.commit()
                self.load_checkin_products()


    ############ PRODUCTS #######################################################################################
    #############################################################################################################
    def create_or_update_product(self):
        button = self.Product_GUI.button_add.text()

        id = self.Product_GUI.label_product_id.text()
        product_name = self.Product_GUI.input_product_name.text().strip()
        product_quantity = self.Product_GUI.input_product_quantity.text().strip()
        product_price = self.Product_GUI.input_product_buy_price.text().strip()
        product_sale_price = self.Product_GUI.input_product_sale_price.text().strip()
        product_unit = self.Product_GUI.combobox_product_unit.currentText()
        product_barcode = self.Product_GUI.input_product_barcode.text().strip()

        if button == 'Əlavə et':
            DB_Table = CheckIn
            product_barcode
            T_id = DB_Table.product_id
            validator = ProductFormValidator(product_name, product_quantity, product_price, product_sale_price, product_barcode, id)
            result = validator.validate()
        else:
            DB_Table = Products
            T_id = DB_Table.id
            validator = ProductFormValidator(product_name, 1, 1, 1, product_barcode, id)
            result = validator.validate()
        
        if result is True:
            product_barcode = self.Product_GUI.input_product_barcode.text().strip()
            with Session() as session:
                if id:
                    new_product = session.query(DB_Table).filter(T_id == id).first()

                    if new_product:
                        pass
                    else:
                        new_product = DB_Table()

                else:
                    new_product = DB_Table()

                if button == 'Əlavə et':
                    new_product.product_id = id
                    new_product.delete_status = 0
                else:
                    pass
                
                new_product.name = product_name
                new_product.quantity = round(float(product_quantity), 2)
                new_product.price = round(float(product_price), 2)
                new_product.sale_price = round(float(product_sale_price), 2)
                new_product.barcode = product_barcode
                new_product.unit = product_unit

                session.add(new_product)
                session.commit()

                self.Product.close()
                if button == 'Əlavə et':
                    self.load_checkin_products()
                else:
                    self.load_products_data()
                    self.load_list_data()

        else:
            QMessageBox.critical(self.Product, AppName, result)


    def open_product_window(self, product, info):
        if info == 'create':
            self.Product_GUI.label_product_id.clear()
            self.Product_GUI.input_product_name.clear()
            self.Product_GUI.input_product_quantity.setText(str(0.0))
            self.Product_GUI.input_product_buy_price.setText(str(0.0))
            self.Product_GUI.input_product_sale_price.setText(str(0.0))
            self.Product_GUI.input_product_barcode.clear()
            self.Product_GUI.combobox_product_unit.setCurrentText('ədəd')
            self.Product_GUI.button_add.setText('Təsdiqlə')
            self.Product_GUI.label_add_product.setText('Məhsul əlavə et')
            self.Product_GUI.button_delete.hide()
        elif info == 'update':
            if hasattr(product, 'product_id'):
                info = 'add'
                label = 'Əlavə et'
                button_delete = self.Product_GUI.button_delete.hide()
                product_id = str(product.product_id)
                purchase_price = str(product.price)
                sale_price = str(product.sale_price)
            else:
                with Session() as session:
                    product_price = session.query(ProductMovements).filter(
                        ProductMovements.product_id == product.id,
                        ProductMovements.movement_type == 0).order_by(ProductMovements.created_date.desc()).first() 
                if product_price:
                    purchase_price = str(product_price.purchase_price)
                    sale_price = str(product_price.sale_price)
                else:
                    purchase_price = str(0.0)
                    sale_price = str(0.0)

                info = 'update'
                label = 'Yenilə'
                button_delete = self.Product_GUI.button_delete.show()
                product_id = str(product.id)

            self.Product_GUI.label_product_id.setText(product_id)
            self.Product_GUI.input_product_name.setText(product.name)
            self.Product_GUI.input_product_quantity.setText(str(product.quantity))
            self.Product_GUI.input_product_buy_price.setText(purchase_price)
            self.Product_GUI.input_product_sale_price.setText(sale_price)
            self.Product_GUI.input_product_barcode.setText(product.barcode)
            self.Product_GUI.combobox_product_unit.setCurrentText(product.unit)
            self.Product_GUI.button_add.setText(label)
            self.Product_GUI.label_add_product.setText('Məlumatları yenilə')
            button_delete
        else:
            if not product:
                QMessageBox.critical(self.Document, AppName, 'Məhsul adını vəya barkodunu daxil edin!')
                self.Document_GUI.input_search_product.clear()
                self.Document_GUI.input_search_product.setFocus()
                return
        
            with Session() as session:
                product = session.query(Products).filter(Products.name.like(f"%{product}%")).first()
                if product:
                    product_for_price = session.query(ProductMovements).filter(
                        ProductMovements.product_id == product.id,
                        ProductMovements.movement_type == 0).order_by(ProductMovements.created_date.desc()).first() 
                    if product_for_price:
                        purchase_price = str(product_for_price.purchase_price)
                        sale_price = str(product_for_price.sale_price)
                    else:
                        purchase_price = str(0.0)
                        sale_price = str(0.0)

                    self.Product_GUI.label_product_id.setText(str(product.id))
                    self.Product_GUI.input_product_name.setText(product.name)
                    self.Product_GUI.input_product_quantity.setText(str(1))
                    self.Product_GUI.input_product_buy_price.setText(str(purchase_price))
                    self.Product_GUI.input_product_sale_price.setText(str(sale_price))
                    self.Product_GUI.input_product_barcode.setText(product.barcode)
                    self.Product_GUI.combobox_product_unit.setCurrentText(product.unit)
                    self.Product_GUI.button_add.setText('Əlavə et')
                    self.Product_GUI.label_add_product.setText('Məhsul əlavə et')
                    self.Product_GUI.button_delete.hide()
                else:
                    QMessageBox.critical(self.List, AppName, 'Məhsul tapılmadı!')
                    self.List_GUI.input_search.clear()
                    self.List_GUI.input_search.setFocus()
                    return
        
        if info == 'add':
            self.Product_GUI.input_product_name.setReadOnly(True)
            self.Product_GUI.input_product_barcode.setReadOnly(True)
            self.Product_GUI.button_generate_barcode.setEnabled(False)
            self.Product_GUI.combobox_product_unit.setEnabled(False)
            self.Product_GUI.input_product_quantity.setReadOnly(False)
            if self.Document_GUI.combobox_document_type.currentText() == 'Alış':
                self.Product_GUI.input_product_buy_price.setReadOnly(False)
            else:
                self.Product_GUI.input_product_buy_price.setReadOnly(True)
            self.Product_GUI.input_product_sale_price.setReadOnly(False)
            self.Product_GUI.input_product_quantity.setFocus()
        else:
            self.Product_GUI.input_product_name.setReadOnly(False)
            self.Product_GUI.input_product_barcode.setReadOnly(False)
            self.Product_GUI.button_generate_barcode.setEnabled(True)
            self.Product_GUI.combobox_product_unit.setEnabled(True)
            self.Product_GUI.input_product_quantity.setReadOnly(True)
            self.Product_GUI.input_product_buy_price.setReadOnly(True)
            self.Product_GUI.input_product_sale_price.setReadOnly(True)
            self.Product_GUI.input_product_name.setFocus()

        self.Product.exec_()
        self.Document_GUI.input_search_product.clear()
        self.Document_GUI.input_search_product.setFocus()
        self.input_filtr_product.clear()
        self.input_filtr_product.setFocus()


    def load_products_data(self):
        search_index = str(self.input_filtr_product.text())

        with Session() as session:
            if search_index:
                all_products = session.query(Products).filter(
                    (Products.name.like(f"%{search_index}%")) |
                    (Products.barcode.like(f"%{search_index}%"))).order_by(Products.name.desc()).limit(500).all()
            else:
                all_products = session.query(Products).order_by(Products.name.desc()).limit(500).all()
            
            self.table_products.setRowCount(len(all_products))

            for row_index, product in enumerate(all_products):
                product_price = session.query(ProductMovements).filter(
                    ProductMovements.product_id == product.id, 
                    ProductMovements.movement_type == 0).order_by(ProductMovements.created_date.desc()).first() 
                
                if product_price:
                    purchase_price = str(product_price.purchase_price)
                    sale_price = str(product_price.sale_price)
                else:
                    purchase_price = str(0.0)
                    sale_price = str(0.0)

                self.table_products.setItem(row_index, 0, QTableWidgetItem(str(product.id)))
                self.table_products.setItem(row_index, 1, QTableWidgetItem(str(product.name)))
                self.table_products.setItem(row_index, 2, QTableWidgetItem(str(product.quantity)))
                self.table_products.setItem(row_index, 3, QTableWidgetItem(str(product.unit)))
                self.table_products.setItem(row_index, 4, QTableWidgetItem(purchase_price))
                self.table_products.setItem(row_index, 5, QTableWidgetItem(sale_price))
                self.table_products.setItem(row_index, 6, QTableWidgetItem(str(product.barcode)))

            self.table_products.setColumnHidden(0, True)
            self.table_products.setColumnWidth(1, 150)


    def calculate_product_quantity(self, product_id):
        with Session() as session:
            product = session.query(Products).filter(Products.id == product_id).first()
            total_purchase_quantity = session.query(
                func.coalesce(func.sum(ProductMovements.quantity), 0)).filter(ProductMovements.product_id == product_id, ProductMovements.movement_type == 0).scalar()

            total_sale_quantity = session.query(
                func.coalesce(func.sum(ProductMovements.quantity), 0)).filter(ProductMovements.product_id == product_id, ProductMovements.movement_type == 1).scalar()

            total_quantity = total_purchase_quantity - total_sale_quantity

            product.quantity = total_quantity
            session.add(product)
            session.commit()


    def delete_product(self):
        id = self.Product_GUI.label_product_id.text()
        with Session() as session:
            product = session.query(Products).filter(Products.id == id).first()
            reply = QMessageBox.question(self, AppName,
                                         f'{product.name} adlı məhsul silinsin?',
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

            if reply == QMessageBox.Yes:
                products = session.query(ProductMovements).filter(ProductMovements.product_id == id).limit(500).all()
                if products:
                    QMessageBox.critical(self, AppName, 'Məhsul sənədlərdə istifadə olunduğu üçün silinə bilməz!')
                else:
                    session.delete(product)
                    session.commit()
                    self.Product.close()
                    self.load_products_data()
            else:
                pass
    

    def on_product_click(self, row, column):
        product_id = self.table_products.item(row, 0).text()
        product = self.get_element_by_id(product_id, Products)
        self.open_product_window(product=product, info='update')


    def filtr_product(self, search_index):
        if not search_index:
            QMessageBox.critical(self, AppName, 'Məhsul adını vəya barkodunu daxil edin!')
            self.input_filtr_product.clear()
            self.input_filtr_product.setFocus()
            return

        with Session() as session:
            product = session.query(Products).filter((Products.name.like(f"%{search_index}%")) | (
                Products.barcode.like(f"%{search_index}%"))).first()

            if product:
                self.open_product_window(product=product, info='update')
            else:
                QMessageBox.critical(self, AppName, 'Məhsul tapılmadı!')
                self.input_filtr_product.clear()
                self.input_filtr_product.setFocus()


    def generate_ean13_barcode(self):
        product_id = self.Product_GUI.label_product_id.text().strip()
        unit = self.Product_GUI.combobox_product_unit.currentText()

        if product_id:
            pass
        else:
            with Session() as session:
                product = session.query(Products).order_by(Products.id.desc()).first()
                if product:
                    product_id = str(product.id + 1)
                else:
                    product_id = '1'

        if unit == 'kq':
            header = 27
        else:
            header = 20
        
        barcode = f"{header}{product_id.zfill(5)}00000"
        
        check_digit = self.calculate_check_digit(barcode)
        full_barcode = barcode + str(check_digit)
        
        self.Product_GUI.input_product_barcode.clear()
        self.Product_GUI.input_product_barcode.setText(full_barcode)


    def calculate_check_digit(self, barcode):        
        odd_sum = 0
        even_sum = 0
        
        for i in range(12):
            digit = int(barcode[i])
            if (i + 1) % 2 == 1:
                odd_sum += digit
            else:
                even_sum += digit * 3
        
        total_sum = odd_sum + even_sum
        
        mod = total_sum % 10
        
        check_digit = (10 - mod) % 10
        
        return check_digit


    ############## MOVEMENTS ########################################################################################################
    #################################################################################################################################
    def load_movements_data(self):
        search_index = self.label_movement_stakeholder_id.text()

        with Session() as session:
            if search_index:
                movements = session.query(StakeholderMovements).filter(
                    StakeholderMovements.stakeholder_id == search_index).order_by(StakeholderMovements.id.desc()).limit(500).all()
            else:
                movements = session.query(StakeholderMovements).order_by(StakeholderMovements.id.desc()).limit(500).all()

            
            self.table_movements.setRowCount(len(movements))

            for row_index, movement in enumerate(movements):
                stakeholder =session.query(Stakeholders).filter(Stakeholders.id == movement.stakeholder_id).first()
                stakeholder_type = 'Tədarükçü' if stakeholder.type == 'supplier' else 'Müştəri'
                movement_type = 'Sənəd' if movement.movement_type == 0 else 'Ödəniş'
                date_string = movement.created_date.strftime('%d.%m.%Y - %H:%M')

                self.table_movements.setItem(row_index, 0, QTableWidgetItem(str(movement.id)))
                self.table_movements.setItem(row_index, 1, QTableWidgetItem(stakeholder_type))
                self.table_movements.setItem(row_index, 2, QTableWidgetItem(stakeholder.name))
                self.table_movements.setItem(row_index, 3, QTableWidgetItem(movement_type))
                self.table_movements.setItem(row_index, 4, QTableWidgetItem(str(movement.total)))
                self.table_movements.setItem(row_index, 5, QTableWidgetItem(str(movement.paid)))
                self.table_movements.setItem(row_index, 6, QTableWidgetItem(str(movement.debt)))
                self.table_movements.setItem(row_index, 7, QTableWidgetItem(date_string))
                
                delete = QTableWidgetItem()
                icon_pixmap = QPixmap(f':/icons/cross.png')
                delete.setIcon(QIcon(icon_pixmap))
                self.table_movements.setItem(row_index, 8, delete)

            self.table_movements.setColumnHidden(0, True)
            self.table_movements.setColumnWidth(8, 20)
            

    def delete_movement(self, row, column):
        movement_id = self.table_movements.item(row, 0).text()
        movement = self.get_element_by_id(movement_id, StakeholderMovements)
        stakeholder_id = movement.stakeholder_id

        if column == 8:
            with Session() as session:
                if movement.movement_type == 1:
                    reply = QMessageBox.question(self, AppName,
                                                f'{movement.id} nömrəli ödəniş sənədi silinsin?',
                                                QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

                    if reply == QMessageBox.Yes:
                        session.delete(movement)
                        session.commit()

                        self.calculate_stakeholder_debt(stakeholder_id)
                        self.load_movements_data()
                    else:
                        pass
                else:
                    QMessageBox.critical(self, AppName, f'Əməliyyat sənədə bağlı olduğu üçün silinə bilməz!')


    def open_payment_window(self, search_index, info):
        self.Payment_GUI.input_paid.setReadOnly(False)
        self.Payment_GUI.payment_calendar.setReadOnly(False)
        button_name = 'Yenilə'

        if not search_index:
            QMessageBox.critical(self, AppName, f'Kontragent təyin olumayıb!')
            self.input_filtr_stakeholder.setFocus()
            return

        with Session() as session:
            if info == 'id':
                stakeholder = session.query(Stakeholders).filter(Stakeholders.id == search_index).first()
            else:
                stakeholder = session.query(Stakeholders).filter((Stakeholders.name.like(f"%{search_index}%")) | (
                    Stakeholders.phone.like(f"%{search_index}%"))).first()

            if stakeholder is None:
                QMessageBox.critical(self, AppName, f'Kontragent tapılmadı!')
                self.input_filtr_stakeholder.clear()
                self.input_filtr_stakeholder.setFocus()
                return


            if stakeholder.debt <= 0:
                self.Payment_GUI.button_add.hide()
            else:
                self.Payment_GUI.button_add.show()

            self.Payment_GUI.label_username.setText(stakeholder.name)
            self.Payment_GUI.label_id.setText(str(stakeholder.id))
            self.Payment_GUI.button_add.setText(button_name)
            stakeholder_type = 'Tədarükçü' if stakeholder.type == 'supplier' else 'Müştəri'
            self.Payment_GUI.label_type.setText(stakeholder_type)

            self.Payment_GUI.input_total.setText(str(stakeholder.debt))
            self.Payment_GUI.input_paid.setText('0')
            self.Payment_GUI.input_debt.setReadOnly(False)
            self.Payment_GUI.input_debt.setText(str(stakeholder.debt))
            self.Payment_GUI.payment_calendar.setDate(stakeholder.payment_date)

            self.Payment_GUI.input_paid.textChanged.connect(self.update_debt)

            self.Payment.exec_()
            self.input_filtr_stakeholder.clear()
            self.input_filtr_stakeholder.setFocus()


    def make_payment(self):
        stakeholder_id = self.Payment_GUI.label_id.text()
        debt = self.Payment_GUI.input_debt.text().strip()
        paid = self.Payment_GUI.input_paid.text().strip()
        total = self.Payment_GUI.input_total.text().strip()
        date = self.Payment_GUI.payment_calendar.date().toPyDate()

        validator = PaymentFormValidator(debt, paid)
        result = validator.validate()

        if result is True:
            with Session() as session:
                stakeholder = session.query(Stakeholders).filter(Stakeholders.id == stakeholder_id).first()
                stakeholder.payment_date = date
                session.commit()

                stakeholder_movement = StakeholderMovements()
                self.create_or_update_stakeholder_movement(
                    session,
                    stakeholder_movement, 
                    stakeholder_id, 
                    0, 
                    1, 
                    total, 
                    paid, 
                    debt)

                self.input_filtr_stakeholder.clear()
                self.load_stakeholders_data()

            self.Payment.close()
        else:
            QMessageBox.critical(self.Payment, AppName, result)


    def update_debt(self):
        total_text = self.Payment_GUI.input_total.text()
        paid_text = self.Payment_GUI.input_paid.text()

        try:
            total = round(float(total_text), 2) if total_text else 0.0
            paid = round(float(paid_text), 2) if paid_text else 0.0

            if total < 0 or paid < 0 or total < paid:
                self.Payment_GUI.input_debt.setText("Hesab xətası!")
                return

            debt = total - paid

            self.Payment_GUI.input_debt.setText(f"{debt:.2f}")
        except ValueError:
            self.Payment_GUI.input_debt.setText("Hesab xətası!")


    def clear_customer(self):
        self.button_clear_customer.hide()
        self.label_customer.clear()
        self.label_customer_id.clear()

    ############# STAKEHOLDERS ######################################################################################################
    #################################################################################################################################
    def create_or_update_stakeholder(self):
        stakeholder_id = self.Stakeholder_GUI.label_stakeholder_id.text()
        stakeholder_name = self.Stakeholder_GUI.input_name.text().strip()
        stakeholder_phone = self.Stakeholder_GUI.input_phone.text().strip()
        stakeholder_type = 'supplier' if self.Stakeholder_GUI.combobox_type_stakeholder.currentText() == 'Tədarükçü' else 'customer'
        stakeholder_note = self.Stakeholder_GUI.input_note.text().strip()
        stakeholder_address = self.Stakeholder_GUI.input_address.text().strip()

        validator = CustomerFormValidator(stakeholder_name, stakeholder_phone, stakeholder_address)
        result = validator.validate()

        if result is True:
            with Session() as session:
                existing_stakeholder = session.query(Stakeholders).filter(Stakeholders.name == stakeholder_name, Stakeholders.address == stakeholder_address).first()

                if stakeholder_id:
                    if existing_stakeholder:
                        if existing_stakeholder.id == int(stakeholder_id):
                            pass
                        else:
                            QMessageBox.critical(self.Stakeholder, AppName, "Bu məlumat artıq istifadə olunub.")
                            return
                    stakeholder = session.query(Stakeholders).filter(Stakeholders.id == stakeholder_id).first()
                else:
                    if existing_stakeholder:
                        QMessageBox.critical(self.Stakeholder, AppName, "Bu məlumat artıq istifadə olunub.")
                        return

                    stakeholder = Stakeholders()
                    stakeholder.payment_date = datetime.now().date()

                stakeholder.name = stakeholder_name
                stakeholder.phone = stakeholder_phone
                stakeholder.note = stakeholder_note
                stakeholder.type = stakeholder_type
                stakeholder.address = stakeholder_address

                session.add(stakeholder)
                session.commit()

                self.Stakeholder.close()
                if self.Stakeholder_GUI.button_add.text() == 'Əlavə et':
                    self.load_list_data()
                else:
                    self.load_stakeholders_data()

        else:
            QMessageBox.critical(self.Stakeholder, AppName, result)


    def open_stakeholders_window(self, info, stakeholder):
        if info == 'normal':
            button_name = 'Təsdiqlə'
        else:
            button_name = 'Əlavə et'

        if not stakeholder:
            self.Stakeholder_GUI.label_stakeholder_id.clear()
            self.Stakeholder_GUI.input_name.clear()
            self.Stakeholder_GUI.input_phone.clear()
            self.Stakeholder_GUI.input_note.clear()
            self.Stakeholder_GUI.input_address.clear()
            self.Stakeholder_GUI.combobox_type_stakeholder.setEnabled(True)
            self.Stakeholder_GUI.combobox_type_stakeholder.setCurrentText('Tədarükçü')
            self.Stakeholder_GUI.button_add.setText(button_name)
            self.Stakeholder_GUI.label_add_stakeholder.setText(f'Kontragent əlavə et')
            self.Stakeholder_GUI.button_delete.hide()
        else:
            with Session() as session:
                stakeholder_check = session.query(StakeholderMovements).filter(StakeholderMovements.stakeholder_id == stakeholder.id).first()
                if stakeholder_check:
                    self.Stakeholder_GUI.combobox_type_stakeholder.setEnabled(False)
                else:
                    self.Stakeholder_GUI.combobox_type_stakeholder.setEnabled(True)

            self.Stakeholder_GUI.label_stakeholder_id.setText(str(stakeholder.id))
            self.Stakeholder_GUI.input_name.setText(stakeholder.name)
            self.Stakeholder_GUI.input_phone.setText(stakeholder.phone)
            self.Stakeholder_GUI.input_note.setText(stakeholder.note)
            stakeholder_type = 'Tədarükçü' if stakeholder.type == 'supplier' else 'Müştəri'
            self.Stakeholder_GUI.combobox_type_stakeholder.setCurrentText(stakeholder_type)
            self.Stakeholder_GUI.input_address.setText(stakeholder.address)
            self.Stakeholder_GUI.button_add.setText('Yenilə')
            self.Stakeholder_GUI.button_delete.show()
            self.Stakeholder_GUI.label_add_stakeholder.setText(f'Kontragent məlumatını yenilə')

        self.Stakeholder.exec_()


    def load_stakeholders_data(self):
        stakeholder_type = self.combobox_type_stakeholders.currentText()
        search_index = str(self.input_filtr_stakeholder.text())

        if stakeholder_type == 'Ümumi':
            pass
        elif stakeholder_type == 'Tədarükçü':
            stakeholder_type = 'supplier'
        else:
            stakeholder_type = 'customer'   

        with Session() as session:
            if search_index:
                if stakeholder_type == 'Ümumi':
                    all_stakeholders = session.query(Stakeholders).filter(
                        (Stakeholders.name.like(f"%{search_index}%")) |
                        (Stakeholders.phone.like(f"%{search_index}%"))).order_by(Stakeholders.payment_date).limit(500).all()
                else:    
                    all_stakeholders = session.query(Stakeholders).filter(
                    (Stakeholders.name.like(f"%{search_index}%")) |
                    (Stakeholders.phone.like(f"%{search_index}%")), Stakeholders.type == stakeholder_type).order_by(Stakeholders.payment_date).limit(500).all() 
            else:
                if stakeholder_type == 'Ümumi':
                    all_stakeholders = session.query(Stakeholders).order_by(Stakeholders.payment_date).limit(500).all()
                else:
                    all_stakeholders = session.query(Stakeholders).filter(Stakeholders.type == stakeholder_type).order_by(Stakeholders.payment_date).limit(500).all() 
            
            self.table_stakeholders.setRowCount(len(all_stakeholders))

            for row_index, stakeholder in enumerate(all_stakeholders):
                self.table_stakeholders.setItem(row_index, 0, QTableWidgetItem(str(stakeholder.id)))
                stakeholder_type = 'Tədarükçü' if stakeholder.type == 'supplier' else 'Müştəri'
                self.table_stakeholders.setItem(row_index, 1, QTableWidgetItem(stakeholder_type))
                self.table_stakeholders.setItem(row_index, 2, QTableWidgetItem(stakeholder.name))
                self.table_stakeholders.setItem(row_index, 3, QTableWidgetItem(stakeholder.address))
                self.table_stakeholders.setItem(row_index, 4, QTableWidgetItem(stakeholder.phone))
                self.table_stakeholders.setItem(row_index, 5, QTableWidgetItem(stakeholder.note))
                debt = round(float(stakeholder.debt), 2)
                self.table_stakeholders.setItem(row_index, 6, QTableWidgetItem(str(debt)))

                date_string = stakeholder.payment_date.strftime('%d.%m.%Y')
                date_item = QTableWidgetItem(date_string)
                difference = (stakeholder.payment_date - datetime.now().date()).days

                if 5 < difference <= 10 and debt != 0:
                    date_item.setForeground(QBrush(QColor("#6d0000")))
                elif 0 < difference <= 5 and debt != 0:
                    date_item.setForeground(QBrush(QColor("#b80000")))
                elif difference <= 0 and debt != 0:
                    date_item.setForeground(QBrush(QColor("#ff0000")))
                else:
                    date_item.setForeground(QBrush(QColor("black")))

                self.table_stakeholders.setItem(row_index, 7, date_item)

            self.table_stakeholders.setColumnHidden(0, True)
            self.table_stakeholders.setColumnWidth(1, 100)
            self.table_stakeholders.setColumnWidth(2, 150)
            self.table_stakeholders.setColumnWidth(3, 200)


    def on_stakeholder_click(self, row, column):
        stakeholder_id = self.table_stakeholders.item(row, 0).text()
        if column == 6:
            self.open_payment_window(search_index=stakeholder_id, info='id')

        else:
            stakeholder = self.get_element_by_id(stakeholder_id, Stakeholders)
            self.open_stakeholders_window('normal', stakeholder)


    def calculate_stakeholder_debt(self, id):
        with Session() as session:
            stakeholder = session.query(Stakeholders).filter(Stakeholders.id == id).first()
            debt = session.query(
                func.coalesce(func.sum(StakeholderMovements.debt), 0)).filter(StakeholderMovements.stakeholder_id == id, StakeholderMovements.movement_type == 0).scalar()

            paid = session.query(
                func.coalesce(func.sum(StakeholderMovements.paid), 0)).filter(StakeholderMovements.stakeholder_id == id, StakeholderMovements.movement_type == 1).scalar()

            total_debt = debt - paid

            stakeholder.debt = total_debt
            session.add(stakeholder)
            session.commit()


    def delete_stakeholder(self):
        id = self.Stakeholder_GUI.label_stakeholder_id.text()
        with Session() as session:
            stakeholder = session.query(Stakeholders).filter(Stakeholders.id == id).first()
            stakeholder_type = 'Tədarükçü' if stakeholder.type == 'supplier' else 'Müştəri'
            reply = QMessageBox.question(self, AppName,
                                         f'{stakeholder.name} adlı {stakeholder_type.lower()} silinsin?',
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

            if reply == QMessageBox.Yes:
                stakeholder_in_documents = session.query(Documents).filter(Documents.stakeholder_id == id).limit(500).all()
                if stakeholder_in_documents:
                    QMessageBox.critical(self, AppName, f'{stakeholder_type} sənədlərdə istifadə olunduğu üçün silinə bilməz!')
                else:
                    stakeholder_in_movements = session.query(StakeholderMovements).filter(StakeholderMovements.stakeholder_id == id).limit(500).all()
                    if stakeholder_in_movements:
                        for process in stakeholder_in_movements:
                            session.delete(process)

                    session.delete(stakeholder)
                    session.commit()
                    self.Stakeholder.close()
                    self.load_stakeholders_data()
            else:
                pass


    #############################################################################################################
    #############################################################################################################
    def get_element_by_id(self, element_id, DB_Table):
        with Session() as session:
            return session.query(DB_Table).filter(DB_Table.id == element_id).first()


    def export_to_excel(self, info):
        with Session() as session:
            if info == 'stakeholders':
                stakeholder_type = self.combobox_type_stakeholders.currentText()
                search_index = str(self.input_filtr_stakeholder.text())

                if stakeholder_type == 'Ümumi':
                    pass
                elif stakeholder_type == 'Tədarükçü':
                    stakeholder_type = 'supplier'
                else:
                    stakeholder_type = 'customer'   

                if search_index:
                    if stakeholder_type == 'Ümumi':
                        data = session.query(Stakeholders).filter(
                            (Stakeholders.name.like(f"%{search_index}%"))|(Stakeholders.phone.like(f"%{search_index}%"))).order_by(Stakeholders.payment_date).all()
                    else:    
                        data = session.query(Stakeholders).filter(
                        (Stakeholders.name.like(f"%{search_index}%")) |
                        (Stakeholders.phone.like(f"%{search_index}%")), Stakeholders.type == stakeholder_type).order_by(Stakeholders.payment_date).all()
                else:
                    if stakeholder_type == 'Ümumi':
                        data = session.query(Stakeholders).order_by(Stakeholders.payment_date)
                    else:
                        data = session.query(Stakeholders).filter(Stakeholders.type == stakeholder_type).order_by(Stakeholders.payment_date).all()
                
                data_list = [{
                    'Ad Soyad': stakeholder.name,
                    'Növ': stakeholder.type,
                    'Ünvan': stakeholder.address,
                    'Telefon': stakeholder.phone,
                    'Qeyd': stakeholder.note,
                    'Borc': stakeholder.debt,
                    'Ödəniş Tarixi': stakeholder.payment_date
                } for stakeholder in data]

                df = pd.DataFrame(data_list)

            elif info == 'products':
                search_index = str(self.input_filtr_product.text())

                if search_index:
                    data = session.query(Products).filter(
                        (Products.name.like(f"%{search_index}%"))|(Products.barcode.like(f"%{search_index}%"))).order_by(Products.name.desc()).all()
                else:
                    data = session.query(Products).order_by(Products.name.desc()).all()
                                
                data_list = []

                for product in data:
                    product_price = session.query(ProductMovements).filter(
                    ProductMovements.product_id == product.id, ProductMovements.movement_type == 0).order_by(ProductMovements.created_date.desc()).first() 
                
                    if product_price:
                        purchase_price = str(product_price.purchase_price)
                        sale_price = str(product_price.sale_price)
                    else:
                        purchase_price = str(0.0)
                        sale_price = str(0.0)

                    product_dict = {
                        'Məhsul': product.name,
                        'Barkod': product.barcode,
                        'Miqdar': product.quantity,
                        'Ölçü vahidi': product.unit,
                        'Alış qiyməti': purchase_price,
                        'Satış qiyməti': sale_price,
                    }
                    
                    data_list.append(product_dict)

                df = pd.DataFrame(data_list)

            elif info == 'documents':
                document_id = self.Document_GUI.label_document_number.text()
                data = session.query(ProductMovements).filter(ProductMovements.document_id == document_id).order_by(ProductMovements.id.desc()).all()

                data_list = []

                for element in data:
                    product = session.query(Products).filter(Products.id == element.product_id).first() 
                
                    product_dict = {
                        'Məhsul': product.name,
                        'Barkod': product.barcode,
                        'Miqdar': element.quantity,
                        'Ölçü vahidi': product.unit,
                        'Qiyməti': element.purchase_price,
                        'Məbləğ': element.purchase_price * element.quantity,
                        'Satış qiyməti': element.sale_price,
                        'Satış məbləği' : element.sale_price * element.quantity
                    }
                    
                    data_list.append(product_dict)

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

    def test(self):
        QMessageBox.information(self.Document, AppName, "Test")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = Main()
    main_window.show()
    sys.exit(app.exec_())
