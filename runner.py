from kite_client import KiteClient

kite = KiteClient()

def menu():
    print("\n=== Kite Client CLI ===")
    print("1. Show Profile")
    print("2. Show Holdings")
    print("3. Show Positions")
    print("4. Show MF Holdings")
    print("5. Get Quote (not supported)") # in free app version by zerodha
    print("6. Exit")

while True:
    menu()
    choice = input("Enter choice: ")

    if choice == "1":
        print(kite.get_profile())
    elif choice == "2":
        kite.print_holdings()
    elif choice == "3":
        print(kite.get_positions())
    elif choice == "4":
        kite.print_mf_holdings()
    elif choice == "5":
        symbol = input("Enter symbol (e.g., NSE:INFY): ")
        print(kite.get_quote(["NSE:"+symbol]))
    elif choice == "6":
        print("Exiting...")
        break
    else:
        print("Invalid choice.")
