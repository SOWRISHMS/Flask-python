# Inventory-Management-System Web Application

This is a **Flask-based Inventory Management System** built as part of the Flask Hiring Test.  
It helps manage **Products**, **Locations**, and **Product Movements** in a warehouse or shop environment.

---

## 🚀 Tech Stack

- **Backend:** Flask (Python)
- **Database:** SQLite
- **Frontend:** HTML, CSS, JavaScript

---

## 🧱 Features

### 🧩 1. Product Management
- Add, edit, and view product details.
- Each product has a unique `product_id` and related information.

### 🧾 Product Adding List
![Product Adding List](Images/Products.png)
*Displays all available products with options to add or edit.*

---

### 📍 2. Location Management
- Add, edit, and view locations.
- Each warehouse or storage point is identified by a `location_id`.

### 📦 Location Adding List
![Location Adding List](Images/Location.png)
*Shows all locations (warehouses/stores) where products are stored.*

---

### 🔄 3. Product Movements
- Record product transfers between locations.
- Supports both **incoming** (to a location) and **outgoing** (from a location) movements.
- Tracks `timestamp`, `product_id`, and `quantity`.

- ### 🔁 Product Movements
![Product Movements](Images/Movements.png)
*Tracks every movement of products between locations with date, time, and quantity.*

---

### 📊 4. Reports
- Displays current product balance across all locations.
- Report includes columns: **Product**, **Warehouse**, and **Quantity**.

---

## 🧠 Use Case Examples

1. Move Product A to Location X  
2. Move Product B to Location X  
3. Move Product A from Location X to Location Y  
4. Generate a balance report to view total quantities at each location  

---

## ⚙️ Installation and Setup

Follow these steps to run the application locally:

```bash
# 1️⃣ Clone the repository
git clone https://github.com/yourusername/inventory-management-flask.git
cd inventory-management-flask

# 2️⃣ Create a virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate

# 3️⃣ Install dependencies
pip install -r requirements.txt

# 4️⃣ Run the application
python app.py
