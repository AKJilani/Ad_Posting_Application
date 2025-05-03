import sqlite3

conn = sqlite3.connect('db/flat.db')
cursor = conn.cursor()

# Create users table
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    Apartment_Type TEXT NOT NULL UNIQUE,
    Apartment_Number TEXT NOT NULL UNIQUE,
    Parking_Number TEXT NOT NULL UNIQUE,
    username TEXT NOT NULL UNIQUE,
    email TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL
)
''')

# Create ads table
cursor.execute('''
CREATE TABLE IF NOT EXISTS ads (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    price REAL,
    user_id INTEGER,
    date_posted TEXT DEFAULT CURRENT_TIMESTAMP
)
''')

# create ad_aparement table
cursor.execute('''
CREATE TABLE IF NOT EXISTS ad_apartment (
    Id INTEGER NOT NULL,
    Type TEXT NOT NULL,
    Building_Number INTEGER NOT NULL,
    Apartment_Type TEXT NOT NULL,
    Apartment_Number TEXT NOT NULL,
    Address TEXT NOT NULL,
    Rent_Per_Month REAL NOT NULL,
    Bedrooms INTEGER NOT NULL,
    Bathrooms INTEGER NOT NULL,
    Parking TEXT NOT NULL,
    Phone_Number TEXT NOT NULL,    
    Available_From_Date DATE NOT NULL,
    Advance_Payment REAL NOT NULL,
    Tenant_Type TEXT NOT NULL,
    Security TEXT NOT NULL,
    Water TEXT NOT NULL,
    Description TEXT NOT NULL,
    Restrictions TEXT NOT NULL,
    Post_Date TEXT DEFAULT CURRENT_TIMESTAMP,
    user_id INTEGER,
    Ad_Active_Status TEXT NOT NULL,
    PRIMARY KEY (Id, Building_Number, Apartment_Type, Apartment_Number)
)
''')


conn.commit()
conn.close()

print("✅ Database and tables created successfully.")
