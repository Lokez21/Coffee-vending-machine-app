# When the system is run for the first time the inventory gets refilled
inventory = {
    'coffee': 1000,  # kgs
    'water': 1000,  # litres
    'milk': 1000,  # litres
    'money_remaining': 50.0  # currency
}

cost = {
    'espresso': 1.50,
    'latte': 2.90,
    'cappuccino': 2.75,
}

recipe = {
    'espresso': {'coffee': 100, 'water': 50, 'milk': 0},
    'latte': {'coffee': 100, 'water': 50, 'milk': 200},
    'cappuccino': {'coffee': 150, 'water': 150, 'milk': 150},
}


# checks for inventory when called .report
def check_resource(selection) -> True:     # Admin user input(Maintenance mode) - '\report']
    for item, recipe_value in recipe[selection].items():
        if inventory[item] - recipe_value < 0:
            return False
    return True


# takes coins and returns change to users or if cancelled return the money to users
def process_coins(selection):
    money_collected = 0.00
    money_dict = {
        0.01: 0,
        0.02: 0,
        0.05: 0,
        0.10: 0,
        0.20: 0,
        0.50: 0,
        1.00: 0,
        2.00: 0,
        5.00: 0,
        10.00: 0,
        20.00: 0,
        50.00: 0,
        }

    to_pay = cost[selection]
    payment_session = True
    print(f'Balance to pay: {to_pay}')
    while payment_session:
        money_inserted = input(f'Insert money: ')
        # accepted money - coins / cash
        if money_inserted not in ('0.01', '0.02', '0.05', '0.10', '0.20', '0.50', '1.00', '2.00',
                                  '5.00', '10.00', '20.00', '50.00', 'cancel'):
            print('Invalid input. Please enter correct values.')
        else:
            if money_inserted == 'cancel':
                payment_session = False  # todo test
                print('Payment cancelled. Returning your money.. ')
                for key, value in money_dict.items():
                    while value > 0:
                        print(f'Return {key}')
                        value -= value
                break

            money_inserted = float(money_inserted)
            money_dict[money_inserted] += 1
            money_collected += money_inserted
            if money_collected >= to_pay:
                print('Thank you for the payment.')
                return_balance = money_collected - to_pay
                if return_balance > 0:
                    print(f'Please take the change: {return_balance}')
                break
    return payment_session


# checks for inventory and prepares drink
def prepare_drink(selection: str) -> bool:
    cup = []
    for item, qty in recipe[selection].items():
        if not inventory[item] - qty < 0:
            inventory[item] -= qty
            cup.append({item: qty})
        else:
            return False
    return True


def print_inventory():
    print('Inventory level: ')
    for item, value in inventory.items():
        print(f'{item} - {value}')


power = True

while power:  # System is ON
    print('-- Python Coffee Vending Machine --')
    print('Welcome. What would you like?')
    power = True
    selection = None

    while selection is None:
        user_input = input('Type [1] for Espresso, [2] for Latte, [3] for Cappuccino?')

        if user_input == '1':
            selection = 'espresso'
            check = check_resource(selection)
            if check:
                print('You have selected Espresso')
            else:
                print('Sorry! Not enough resources to make Espresso')
        elif user_input == '2':
            selection = 'latte'
            check = check_resource(selection)
            if check:
                print('You have selected Latte')
            else:
                print('Sorry! Not enough resources to make Latte')
        elif user_input == '3':
            selection = 'cappuccino'
            check = check_resource(selection)
            if check:
                print('You have selected Cappuccino')
            else:
                print('Sorry! Not enough resources to make Cappuccino')
        elif user_input == '.report':
            selection = user_input
        elif user_input == '.off':
            selection = user_input
            power = False
            print('Turning off!')
        else:
            print('Invalid choice. Please try again. ')

    if ~power:  # code is terminated, turning off for maintenance and refilling,
        print('Shutting down...')
        break

    if selection == '.report':  # checks the resources remaining
        print_inventory()

    if selection in ['espresso', 'latte', 'cappuccino'] and check:
        payment = process_coins(selection)
        if payment:
            drink = prepare_drink(selection)
            print(f'Please grab your {selection}({drink}). Enjoy.\n\n')
        else:
            print()

