# POSCredit <img src="https://github.com/user-attachments/assets/e1d7a617-8be0-4fa6-94f4-2a515ba273ec" alt="favicon" width="30"/>

POSCredit is a user-friendly Point of Sale (POS) desktop application designed for small to medium-sized businesses that need an efficient way to manage sales transactions, customer information, and credit management. Built using Python and PyQt5, POSCredit offers a modern graphical user interface that simplifies the sales process and enhances the overall customer experience.

## Features

- **User-Friendly Interface**  
  A clean and intuitive design for easy navigation without extensive training.

- **Customer Management**  
  Effortlessly create and manage customer profiles for personalized service.

- **Product Management**  
  Add and update product details, ensuring inventory is always current.

- **Sales Processing**  
  Quickly process cash and credit transactions, with automatic balance calculations for partial payments.

- **Credit Management**  
  Track customer debts, view outstanding balances, and access payment history.

- **Document Generation**  
  Generate sales receipts and other documents for accurate record-keeping.

## Demo
 <img src="https://github.com/user-attachments/assets/1428a2b7-d462-4fae-9dd7-4ec3e10271e6" alt="favicon" width="700"/>


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
