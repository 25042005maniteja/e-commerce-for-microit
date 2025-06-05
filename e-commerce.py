import sys

class Product:
    def __init__(self, pid, name, price, stock):
        self.id = pid
        self.name = name
        self.price = price
        self.stock = stock

    def __str__(self):
        return f"{self.id}: {self.name} - ${self.price:.2f} (Stock: {self.stock})"

class User:
    def __init__(self, username):
        self.username = username
        self.cart = {}

    def add_to_cart(self, product, quantity):
        if quantity <= 0:
            print("Quantity must be positive.")
            return False
        if product.stock < quantity:
            print(f"Sorry, only {product.stock} items are in stock.")
            return False
        if product.id in self.cart:
            if self.cart[product.id] + quantity > product.stock:
                print(f"Sorry, adding {quantity} exceeds available stock.")
                return False
            self.cart[product.id] += quantity
        else:
            self.cart[product.id] = quantity
        print(f"Added {quantity} x {product.name} to your cart.")
        return True

    def remove_from_cart(self, product_id, quantity):
        if product_id not in self.cart:
            print("Product not in your cart.")
            return False
        if quantity <= 0:
            print("Quantity must be positive.")
            return False
        if quantity >= self.cart[product_id]:
            del self.cart[product_id]
            print("Removed the product from your cart.")
        else:
            self.cart[product_id] -= quantity
            print(f"Removed {quantity} items from your cart.")
        return True

    def view_cart(self, catalog):
        if not self.cart:
            print("\nYour cart is empty.\n")
            return
        print("\nYour Cart:")
        total = 0.0
        for pid, qty in self.cart.items():
            product = catalog.get(pid)
            if product:
                subtotal = product.price * qty
                total += subtotal
                print(f" - {product.name}: {qty} x ${product.price:.2f} = ${subtotal:.2f}")
        print(f"Total amount: ${total:.2f}\n")

    def checkout(self, catalog):
        if not self.cart:
            print("Your cart is empty. Cannot checkout.")
            return False
        total = 0.0
        # Check stock again before purchase
        for pid, qty in self.cart.items():
            product = catalog.get(pid)
            if product.stock < qty:
                print(f"Sorry, {product.name} stock has changed. Only {product.stock} items left.")
                return False
        print("\nOrder Summary:")
        for pid, qty in self.cart.items():
            product = catalog.get(pid)
            subtotal = product.price * qty
            total += subtotal
            print(f" - {product.name}: {qty} x ${product.price:.2f} = ${subtotal:.2f}")

        print(f"Total amount due: ${total:.2f}")
        confirm = input("Confirm purchase? (y/n): ").strip().lower()
        if confirm == 'y':
            # Deduct stock
            for pid, qty in self.cart.items():
                catalog[pid].stock -= qty
            self.cart.clear()
            print("Purchase successful! Thank you for shopping.")
            return True
        else:
            print("Purchase cancelled.")
            return False


def list_products(catalog, page=1, per_page=5):
    products = list(catalog.values())
    total_pages = (len(products) + per_page - 1) // per_page
    if page < 1 or page > total_pages:
        print("Invalid page number.")
        return [], total_pages
    start = (page -1) * per_page
    end = start + per_page
    print(f"\nProducts (Page {page}/{total_pages}):")
    for prod in products[start:end]:
        print(f"  {prod}")
    return products[start:end], total_pages

def find_product(catalog, pid):
    return catalog.get(pid)

def main():
    print("Welcome to the Python CLI E-Commerce Store!")
    username = input("Please enter your username to continue: ").strip()
    if not username:
        print("Username cannot be empty. Exiting...")
        sys.exit()

    user = User(username)
    print(f"Hello, {user.username}! Let's start shopping.\n")

    # Sample catalog: id, name, price, stock
    catalog = {
        "P1001": Product("P1001", "Wireless Mouse", 25.99, 15),
        "P1002": Product("P1002", "Mechanical Keyboard", 79.99, 10),
        "P1003": Product("P1003", "HD Monitor 24 inch", 150.00, 7),
        "P1004": Product("P1004", "USB-C Hub", 39.99, 25),
        "P1005": Product("P1005", "External SSD 1TB", 120.50, 5),
        "P1006": Product("P1006", "Gaming Headset", 49.99, 12),
        "P1007": Product("P1007", "Webcam 1080p", 60.00, 8),
        "P1008": Product("P1008", "Laptop Stand", 29.99, 20),
        "P1009": Product("P1009", "Portable Charger", 35.00, 30),
        "P1010": Product("P1010", "Smartwatch", 199.99, 4)
    }

    current_page = 1
    while True:
        print("\nMenu Options:")
        print("  1. Browse products")
        print("  2. View cart")
        print("  3. Add product to cart")
        print("  4. Remove product from cart")
        print("  5. Checkout")
        print("  6. Exit")

        choice = input("Select an option (1-6): ").strip()
        if choice == '1':
            per_page = 5
            while True:
                products_page, total_pages = list_products(catalog, current_page, per_page)
                print("\n(N)ext page | (P)revious page | (B)ack to menu")
                nav = input("Choose an option: ").strip().lower()
                if nav == 'n':
                    if current_page < total_pages:
                        current_page += 1
                    else:
                        print("Already at last page.")
                elif nav == 'p':
                    if current_page > 1:
                        current_page -= 1
                    else:
                        print("Already at first page.")
                elif nav == 'b':
                    break
                else:
                    print("Invalid option.")
        elif choice == '2':
            user.view_cart(catalog)
        elif choice == '3':
            pid = input("Enter product ID to add: ").strip()
            product = find_product(catalog, pid)
            if not product:
                print("Product not found.")
                continue
            print(f"Selected {product.name} - Price ${product.price:.2f}, Stock: {product.stock}")
            try:
                qty = int(input("Enter quantity to add: ").strip())
            except ValueError:
                print("Invalid quantity.")
                continue
            if qty <= 0:
                print("Quantity must be positive.")
                continue
            user.add_to_cart(product, qty)
        elif choice == '4':
            if not user.cart:
                print("Your cart is empty.")
                continue
            pid = input("Enter product ID to remove: ").strip()
            if pid not in user.cart:
                print("Product not in your cart.")
                continue
            try:
                qty = int(input("Enter quantity to remove: ").strip())
            except ValueError:
                print("Invalid quantity.")
                continue
            if qty <= 0:
                print("Quantity must be positive.")
                continue
            user.remove_from_cart(pid, qty)
        elif choice == '5':
            user.checkout(catalog)
        elif choice == '6':
            print(f"Goodbye, {user.username}! Thanks for visiting.")
            break
        else:
            print("Invalid option. Please choose 1-6.")

if __name__ == "__main__":
    main()

