# Bar Inventory and Sales Management

This is a desktop application for managing the inventory and sales of a bar, developed using Python with Tkinter and SQLite.

## Features

- **Login:** Secure access with username and password, using salted hashes for security.
- **User Roles:**
    - **Admin:** Full access to all modules (Inventory, Sales, Closing).
    - **Cashier:** Access restricted to the Sales module only.
- **Inventory Management:** Add, edit, and delete products with details like name, quantity, price, and a unique shortcut.
- **Sales Registration:** Quickly register sales using product shortcuts, with automatic calculation of totals and change.
- **Daily Closing:** Generate a daily sales report with details of products sold, total revenue, and remaining stock.

## Installation

1.  **Clone the repository:**
    ```bash
    git clone <repository_url>
    cd <repository_folder>
    ```

2.  **Create a virtual environment (recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3.  **Install dependencies:**
    This project has no external dependencies beyond Python's standard library for its core functionality. If you want to build the executable, you will need `pyinstaller`.
    ```bash
    pip install -r requirements.txt
    ```

## How to Run the Application

To run the application, execute the `main.py` file:
```bash
python -m bar_app.main
```

The application will start, and you will be prompted with the login screen. The default credentials are:
- **Admin:**
    - **Username:** `admin`
    - **Password:** `admin`
- **Cashier:**
    - **Username:** `cajero`
    - **Password:** `cajero`

## How to Build the Executable

This project uses **PyInstaller** to create a standalone executable file for Windows, macOS, or Linux.

1.  **Install PyInstaller** by following the installation steps above.

2.  **Run the PyInstaller command:**
    From the root of the project, run the following command:
    ```bash
    pyinstaller --onefile --windowed --name BarApp bar_app/main.py
    ```
    - `--onefile`: Bundles everything into a single executable file.
    - `--windowed`: Prevents the command-line console from appearing when you run the application.
    - `--name BarApp`: Specifies the name of the output executable.

3.  **Find the executable:**
    The generated executable will be located in the `dist` folder. You can distribute this file to other users.

## Future Improvements

- **Export to PDF/Excel:** Add functionality to the closing panel to export the daily report to PDF or Excel for better record-keeping.
- **Sales History:** Implement a separate panel to view sales history from previous days, with filters by date range.
- **Logo Customization:** Allow the bar logo on the login screen to be customized from the application settings.
- **More Detailed Reports:** Add more advanced reports, such as best-selling products or sales trends over time.
