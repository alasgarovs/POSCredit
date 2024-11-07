# POSCredit

POSCredit is a user-friendly Point of Sale (POS) application designed for small to medium-sized businesses that need an efficient way to manage sales transactions, customer information, and credit management. Built using Python and PyQt5, POSCredit offers a modern graphical user interface that simplifies the sales process and enhances the overall customer experience.

## Features

- **Intuitive User Interface**: The application features a clean and straightforward interface, making it easy for users to navigate and perform tasks without extensive training.
- **Customer Management**: Users can easily add, edit, and manage customer profiles, allowing for personalized service and better customer relationship management.
- **Product Management**: The program allows users to add and manage products, including details such as product name, price, and stock levels, ensuring that inventory is always up to date.
- **Sales Processing**: POSCredit enables users to process sales transactions quickly, including handling cash and credit payments. The system automatically calculates the remaining balance for customers who make partial payments.
- **Credit Management**: The application tracks customer debts, allowing businesses to manage credit sales effectively. Users can view outstanding balances and payment history for each customer.
- **Document Generation**: POSCredit can generate sales receipts and other documents, providing customers with proof of purchase and helping businesses maintain accurate records.

## Demo
![screenshot](https://github.com/user-attachments/assets/1428a2b7-d462-4fae-9dd7-4ec3e10271e6)


## Requirements

- Python 3.12
- PyQt5

## Installation and Usage

1. Clone the repository:
   ```console
   git clone https://github.com/alasgarovs/POSCredit.git
   cd POSCredit
   ```
   
2. Create virtualenv.
   ```console
   python -m venv .venv
   source .venv/bin/activate
   ```
   
3. Install requirements:
   ```console
   pip install -r requirements.txt
   ```
   
4. Create `secret_key.py` in `src` folder and enter the following:
   ```console
    SecretKey = 'your_secret_key'
   ```
   
5. Create `info.py` in `src` folder and enter the following:
   ```console
   AppName = 'app_name'
   AppVersion = 'app_version'
   LastUpdate = 'last_update_date'
   OriginalFilename = 'file_name'
   FileDescription = 'description'
   CompanyName = 'company_name'
   Website = 'website'
   LegalCopyright = 'copyright'
   ```
      
   
## Future Improvements

We have several exciting enhancements planned for future releases, including:

- **Multi-Language Support**: Implement support for multiple languages to make the application accessible to a broader audience.
- **Multiple SQL Database Connections**: Add support for various SQL databases, including MS SQL Server, PostgreSQL, MySQL, and others, allowing users to interact with their preferred database systems.
- **User Interface Enhancements**: Improve the user interface to enhance usability and provide a more intuitive experience for users.


## Contributing

Contributions are welcome! If you have suggestions for improvements or new features, please open an issue or submit a pull request.
