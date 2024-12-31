import hashlib
import subprocess
from db_connect import Products, Session
from secret_key import SecretKey


class ProductFormValidator:
    def __init__(self, product_name, product_quantity, product_buy_price, product_sale_price, product_barcode,product_id):
        self.product_name = product_name
        self.product_quantity = product_quantity
        self.product_buy_price = product_buy_price
        self.product_sale_price = product_sale_price
        self.product_barcode = product_barcode
        self.product_id = product_id

    def validate(self):
        # Validate product name
        if not self.product_name:
            return "Məhsul adı boş ola bilməz."
        if len(self.product_name) > 100:
            return "Məhsul adı 100 simvoldan çox ola bilməz."

        # Validate product quantity
        try:
            if float(self.product_quantity) <= 0:
                    "Məhsulun miqdarı düzgün deyil."
        except ValueError:
            return "Məhsulun miqdarı düzgün deyil."

        # Validate product buy price
        try:
            buy_price = float(self.product_buy_price)
            if buy_price <= 0:
                return "Məhsulun alış qiyməti düzgün deyil."
        except ValueError:
            return "Məhsulun alış qiyməti düzgün deyil."

        # Validate product sale price
        try:
            sale_price = float(self.product_sale_price)
            if sale_price <= 0:
                return "Məhsulun satış qiyməti düzgün deyil."
        except ValueError:
            return "Məhsulun satış qiyməti düzgün deyil."

        # Validate product barcode
        if self.product_barcode.isdigit() == False:
            return 'Məhsul barkodu düzgün deyil!'

        if not self.product_barcode or len(self.product_barcode) > 13:
            return "Məhsulun barkodu boş ola bilməz və 13 simvoldan çox olmamalıdır."

        # Check if barcode is unique
        if not self.is_barcode_unique():
            return "Barkod unikal deyil."

        return True

    def is_barcode_unique(self):
        if self.product_barcode == 'pass':
            return True
        
        session = Session()
        try:
            existing_product = session.query(Products).filter(Products.barcode == self.product_barcode).first()
            if existing_product:
                if self.product_id:
                    if existing_product.id == int(self.product_id):
                        return True
                    return False
                else:
                    return False
            return True
        finally:
            session.close()


class CustomerFormValidator:
    def __init__(self, name, phone, address):
        self.name = name
        self.phone = phone
        self.address = address

    def validate(self):
        # Validate first name
        if not self.name:
            return "Ad boş ola bilməz."
        if len(self.name) > 100:
            return "Ad 100 simvoldan çox ola bilməz."

        # Validate primary phone number
        if not self.phone:
            return "Telefon nömrəsi boş ola bilməz."

        # Validate address (optional)
        if not self.address:
            return 'Ünvan boş ola bilməz.'
        if len(self.address) > 100:
            return "Ünvan 100 simvoldan çox ola bilməz."

        return True


class CheckOutFormValidator:
    def __init__(self, product_quantity, product_price):
        self.product_quantity = product_quantity
        self.product_price = product_price

    def validate(self):
        # Validate product quantity
        try:
            quantity = float(self.product_quantity)
            if quantity <= 0:
                return "Məhsulun miqdarı düzgün deyil."
        except ValueError:
            return "Məhsulun miqdarı düzgün deyil."

        # Validate product buy price
        try:
            price = float(self.product_price)
            if price <= 0:
                return "Məhsulun qiyməti düzgün deyil."
        except ValueError:
            return "Məhsulun qiyməti düzgün deyil."

        return True


class PaymentFormValidator:
    def __init__(self, debt, paid):
        self.payment_debt = debt
        self.payment_paid = paid

    def validate(self):
        try:
            debt = float(self.payment_paid)
            if debt <= 0:
                return "Ödəniş məbləği düzgün deyil."
        except ValueError:
            return "Ödəniş məbləği düzgün deyil."

        try:
            debt = float(self.payment_debt)
            if debt < 0:
                return "Ödəniş məbləği düzgün deyil."
        except ValueError:
            return "Ödəniş məbləği düzgün deyil."

        return True


class LicenseManager:
    def __init__(self):
        self.secret_key = SecretKey

    def get_processor_id(self):
        try:
            output = subprocess.check_output("wmic cpu get ProcessorId", shell=True)
            processor_id = output.decode().strip().split('\n')[1].strip()
            return processor_id
        except:
            return None

    def generate_license_key(self):
        processor_id = self.get_processor_id()
        if processor_id:
            modified_id = f"{processor_id}{self.secret_key}"
            hash_object = hashlib.sha256(modified_id.encode())
            license_key = hash_object.hexdigest()[:20]
            return license_key
        return None

    def validate_license_key(self, license_key):
        processor_id = self.get_processor_id()
        if processor_id:
            expected_license_key = self.generate_license_key()
            return license_key == expected_license_key
        return None
