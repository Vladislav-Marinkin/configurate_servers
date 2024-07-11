import os

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

class Menu:
    def __init__(self, title, options):
        self.title = title
        self.options = options
        self.previous_menu = None

    def display(self):
        clear_screen()
        print(self.title)
        for i, option in enumerate(self.options, 1):
            print(f"{i}. {option}")
        print("\nType 'exit' to quit or 'back' to go to the previous menu.")

    def get_choice(self):
        while True:
            choice = input("Select an option: ").strip().lower()
            if choice == 'exit':
                exit(0)
            if choice == 'back' and self.previous_menu:
                return 'back'
            if choice.isdigit() and 1 <= int(choice) <= len(self.options):
                return int(choice)
            print("Invalid choice. Please try again.")
            
    def check_yes_no(self, answer):
        while True:
            use_login_password = input(answer).lower()
            if use_login_password in ('yes', 'no') or ('y', 'n'):
                if use_login_password == 'yes' or 'y':
                    return True
                else:
                    return False
            else:
                print("Invalid input. Please enter 'yes' or 'no'.")
                
    def print_server_list(self, client_list):
        for server in client_list:
            print(f"{server['ip']}, {server['mac']}, SSH open: {server['ssh']}")