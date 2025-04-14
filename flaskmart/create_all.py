from mart import app, db
from mart.models import User, Item

# Add User to the database
def add_user(username, email_address, password_hash, budget=1000):
    new_user = User(username=username, email_address=email_address, password_hash=password_hash, budget=budget)
    db.session.add(new_user)
    db.session.commit()
    print(f"✅ Added User: {new_user.username}")

# Add Item to the database
def add_item(name, price, barcode, description, user_id):
    new_item = Item(name=name, price=price, barcode=barcode, description=description, owner=user_id)
    db.session.add(new_item)
    db.session.commit()
    print(f"✅ Added Item: {new_item.name}")

# Run inside app context
with app.app_context():
    db.create_all()

    # Adding a user based on user input
    print("--- Enter details for User ---")
    username = input("Enter username: ")
    email_address = input("Enter email address: ")
    password_hash = input("Enter password hash: ")  # You should hash the password in real-world applications
    budget = int(input("Enter budget (default 1000): ") or 1000)

    add_user(username, email_address, password_hash, budget)

    # Fetch the user id of the newly added user
    user = User.query.filter_by(username=username).first()

    # Adding items based on user input
    num_to_add = int(input("\nHow many items would you like to add? "))

    for i in range(num_to_add):
        print(f"\n--- Enter details for item {i+1} ---")
        name = input("Enter item name: ")
        price = int(input("Enter item price: "))
        barcode = input("Enter item barcode: ")
        description = input("Enter item description: ")
        add_item(name, price, barcode, description, user.id)
