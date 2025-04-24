from config import supabase
from migration import create_sponsor_tiers





swags = [
    {
        "name": "Python Togo T-Shirt",
        "description": "Proudly represent the Python Togo community with our official t-shirt. Made from high-quality cotton.",
        "price": 2500,
        "priceDollar": 4,
        "originalPrice": 5000,
        "images": [
            "static/images/swags/tshirt.png",
            "static/images/swags/tshirt1.png",
            "static/images/swags/tshirt2.png",
            "static/images/swags/tshirt3.png",
            "static/images/swags/tshirt6.png",
            "static/images/swags/tshirt7.png",
            "static/images/swags/tshirt4.png",
            "static/images/swags/tshirt5.png",
        ],
    },
    {
        "name": "Python Togo Travel Mugs & Tumblers",
        "description": "This tumbler boasts a large capacity and an ergonomic handle for a comfortable hold.",
        "price": 5000,
        "priceDollar": 8,
        "originalPrice": 5000,
        "images": [
            "static/images/swags/bootle.png",
            "static/images/swags/bootle1.png",
            "static/images/swags/bootle2.png",
            "static/images/swags/bootle3.png",
            "static/images/swags/bootle4.png",
        ],
    },
    {
        "name": "Python Togo Hoodie",
        "description": "Stay warm with our Python Togo hoodie. Perfect for coding nights and meetups.",
        "price": 9500,
        "priceDollar": 15,
        "originalPrice": 9000,
        "images": [
            "static/images/swags/hoodie8.png",
            "static/images/swags/hoodie2.png",
            "static/images/swags/hoodie.png",
            "static/images/swags/hoodie1.png",
            "static/images/swags/hoodie7.png",
            "static/images/swags/hoodie4.png",
            "static/images/swags/hoodie5.png",
            "static/images/swags/hoodie6.png",
        ],
    },
    {
        "name": "Python Togo Cap",
        "description": "Complete your tech look with our exclusive Python Togo cap. Adjustable and comfortable.",
        "price": 1500,
        "priceDollar": 3,
        "originalPrice": 3500,
        "images": [
            "static/images/swags/cap7.png",
            "static/images/swags/cap.png",
            "static/images/swags/cap1.png",
            "static/images/swags/cap2.png",
            "static/images/swags/cap3.png",
            "static/images/swags/cap4.png",
            "static/images/swags/cap5.png",
            "static/images/swags/cap6.png",
        ],
    },
    {
        "name": "Python Togo Stickers",
        "description": "Decorate your laptop, phone, and more with our Python Togo stickers. Durable and waterproof.",
        "price": 500,
        "priceDollar": 1,
        "originalPrice": 1000,
        "images": [
            "static/images/swags/stickers1.png",
            "static/images/swags/stickers.png",
            "static/images/swags/stickers2.png",
        ],
    },
    {
        "name": "Python all over print",
        "description": "This all-over print is a unique and stylish way to show your love for Python.",
        "price": 15000,
        "priceDollar": 25,
        "originalPrice": 20000,
        "images": [
            "static/images/swags/allover3.png",
            "static/images/swags/allover1.png",
            "static/images/swags/allover2.png",
            "static/images/swags/allover4.png",
            "static/images/swags/allover5.png",
            "static/images/swags/allover6.png",
        ],
    },
]


def get_swags():
    return swags

def get_sponsorteirs():
    """
    Fetch all sponsor tiers from the database.
    """
    create_sponsor_tiers()
    response = supabase.table("sponsortiers").select("*").execute()
    data = response.data
    if len(data) == 0:
        print("No sponsor tiers found.")
        return []

    for tier in data:
        tier["amount_cfa"] = int(tier["amount_cfa"])
        tier["amount_usd"] = int(float(tier["amount_usd"]))
        tier["availability"] = int(tier["availability"])
    
    return data

def get_sponsortirtbytitle(title):
    """
    Fetch a specific sponsor tier by its title.
    """
    create_sponsor_tiers()
    response = supabase.table("sponsortiers").select("*").eq("title", title).execute()
    data = response.data
    if len(data) == 0:
        print(f"No sponsor tier found with title: {title}")
        return None
    data[0]["amount_cfa"] = int(data[0]["amount_cfa"])
    data[0]["amount_usd"] = int(float(data[0]["amount_usd"]))
    data[0]["availability"] = int(data[0]["availability"])
    
    return data[0]

def get_something_email(table, email):
    """
    Fetch a specific entry by email from a given table.
    """
    response = supabase.table(table).select("*").eq("email", email).execute()
    data = response.data
    if len(data) == 0:
        print(f"No entry found with email: {email}")
        return None
    return data[0]

def get_something_by_field(table, field, value):
    """
    Fetch a specific entry by a given field and value from a specified table.
    """
    response = supabase.table(table).select("*").eq(field, value).execute()
    data = response.data
    if len(data) == 0:
        print(f"No entry found with {field}: {value}")
        return None
    return data

def get_something_by_email_firstname_lastname(table, email, firstname, lastname):
    """
    Fetch a specific entry by email, first name, and last name from a given table.
    """
    response = supabase.table(table).select("*").eq("email", email).eq("firstname", firstname).eq("lastname", lastname).execute()
    data = response.data
    if len(data) == 0:
        print(f"No entry found with email: {email}, firstname: {firstname}, lastname: {lastname}")
        return None
    return data[0]


def insert_something(table, data):
    """
    Insert a new entry into a specified table.
    """
    response = supabase.table(table).insert(data).execute()
    if response:
        print("Data inserted successfully.")
        return True
    else:
        print(f"Failed to insert data: {response.error}")
        return False

def update_something(table, email, data):
    """
    Update an entry in a specified table based on email.
    """
    response = supabase.table(table).update(data).eq("email", email).execute()
    if response.status_code == 200:
        print("Data updated successfully.")
        return True
    else:
        print(f"Failed to update data: {response.error}")
        return False



if __name__ == "__main__":
    tiers = get_sponsorteirs()
    print(tiers)
  