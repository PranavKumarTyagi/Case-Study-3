from abc import ABC, abstractmethod

# 1. Abstract Base Class
class Payment(ABC):
    def __init__(self, user_name):
        self.user_name = user_name

    @abstractmethod
    def pay(self, amount):
        """Abstract method to calculate final amount."""
        pass

    def generate_receipt(self, original_amount, final_amount, method):
        """Concrete method to print the receipt."""
        print(f"\n[{method}] Transaction Successful")
        print(f"User Name        : {self.user_name}")
        print(f"Original Amount  : ₹{original_amount:.2f}")
        print(f"Final Amount Paid: ₹{final_amount:.2f}")
        print("-" * 40)

# 2. Child Classes with Business Logic
class CreditCardPayment(Payment):
    def pay(self, amount):
        gateway_fee = amount * 0.02
        gst_on_fee = gateway_fee * 0.18
        final_amount = amount + gateway_fee + gst_on_fee
        self.generate_receipt(amount, final_amount, "CREDIT CARD")

class UPIPayment(Payment):
    def pay(self, amount):
        cashback = 50 if amount > 1000 else 0
        final_amount = amount - cashback
        if cashback > 0:
            print(f"\n[UPI] Yay! Cashback of ₹{cashback} applied!")
        self.generate_receipt(amount, final_amount, "UPI")

class PayPalPayment(Payment):
    def pay(self, amount):
        international_fee = amount * 0.03
        conversion_fee = 20.0
        final_amount = amount + international_fee + conversion_fee
        self.generate_receipt(amount, final_amount, "PAYPAL")

class WalletPayment(Payment):
    def __init__(self, user_name, balance):
        super().__init__(user_name)
        self.balance = balance

    def pay(self, amount):
        if amount > self.balance:
            print(f"\n[WALLET] Transaction Failed!")
            print(f"Reason: Insufficient balance. (Balance: ₹{self.balance:.2f}, Attempted: ₹{amount:.2f})")
            print("-" * 40)
            return
        
        self.balance -= amount
        self.generate_receipt(amount, amount, "WALLET")
        print(f"-> Remaining Wallet Balance: ₹{self.balance:.2f}")
        print("-" * 40)

# 3. Polymorphic Function
def process_payment(payment, amount):
    payment.pay(amount)

# 4. Interactive Driver Code
if __name__ == "__main__":
    print("=" * 40)
    print("   SMART PAYMENT PROCESSING SYSTEM")
    print("=" * 40)

    # Get User Info
    customer_name = input("Enter your name to begin: ")
    starting_balance = 5000.0  # Giving the user a default starting balance
    print(f"Welcome, {customer_name}! Your Wallet has been funded with ₹{starting_balance:.2f}")

    # Initialize Objects
    cc = CreditCardPayment(customer_name)
    upi = UPIPayment(customer_name)
    paypal = PayPalPayment(customer_name)
    wallet = WalletPayment(customer_name, starting_balance)

    # Interactive Menu
    while True:
        print("\n=== SELECT PAYMENT METHOD ===")
        print("1. Credit Card (2% fee + 18% GST on fee)")
        print("2. UPI (₹50 cashback on amounts > ₹1000)")
        print("3. PayPal (3% international fee + ₹20 conversion)")
        print("4. Digital Wallet")
        print("5. Exit System")
        
        choice = input("Enter your choice (1-5): ")

        if choice == '5':
            print("\nExiting Smart Payment System. Have a great day!")
            break

        if choice in ['1', '2', '3', '4']:
            try:
                amount_str = input("Enter the payment amount: ₹")
                amount = float(amount_str)
                if amount <= 0:
                    print("Error: Amount must be greater than zero.")
                    continue
            except ValueError:
                print("Error: Please enter a valid number.")
                continue

            # Process based on user choice
            if choice == '1':
                process_payment(cc, amount)
            elif choice == '2':
                process_payment(upi, amount)
            elif choice == '3':
                process_payment(paypal, amount)
            elif choice == '4':
                process_payment(wallet, amount)
        else:
            print("Invalid choice! Please select a number between 1 and 5.")