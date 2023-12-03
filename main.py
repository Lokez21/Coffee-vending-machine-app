from decimal import Decimal

# When the system is run for the first time the inventory gets refilled
inventory = {  # to store the available resources and subtract resources every time a coffee is made
    'coffee': Decimal('250'),  # kgs
    'water': Decimal('2500'),  # litres
    'milk': Decimal('2500'),  # litres
}

cost = {
    'espresso': Decimal('1.50'),
    'latte': Decimal('2.90'),
    'cappuccino': Decimal('2.75'),
}

recipe = {
    'espresso': {'coffee': Decimal('100'), 'water': Decimal('50'), 'milk': Decimal('0')},
    'latte': {'coffee': Decimal('100'), 'water': Decimal('100'), 'milk': Decimal('200')},
    'cappuccino': {'coffee': Decimal('150'), 'water': Decimal('150'), 'milk': Decimal('150')},
}

money_in_machine = {
    Decimal('0.01'): 100,
    Decimal('0.02'): 100,
    Decimal('0.05'): 100,
    Decimal('0.10'): 100,
    Decimal('0.20'): 100,
    Decimal('0.50'): 100,
    Decimal('1.00'): 100,
    Decimal('2.00'): 100,
    Decimal('5.00'): 100,
    Decimal('10.00'): 100,
    Decimal('20.00'): 100,
    Decimal('50.00'): 100,
}

# checks for inventory when called .report
def check_resource(selection) -> True:  # Admin user enters '.report' command
    for item, recipe_value in recipe[selection].items():
        if inventory[item] - recipe_value < 0:
            return False
    return True


# takes coins and returns change to users or if cancelled refunds the money to the users
def process_coins(selection):
    money_collected = Decimal('0.00')
    session_money = {
        Decimal('0.01'): 0,
        Decimal('0.02'): 0,
        Decimal('0.05'): 0,
        Decimal('0.10'): 0,
        Decimal('0.20'): 0,
        Decimal('0.50'): 0,
        Decimal('1.00'): 0,
        Decimal('2.00'): 0,
        Decimal('5.00'): 0,
        Decimal('10.00'): 0,
        Decimal('20.00'): 0,
        Decimal('50.00'): 0,
    }

    to_pay = cost[selection]
    payment_session = True
    print(f'Balance to pay: {to_pay:.2f}')
    while payment_session:
        money_inserted = input(f"Insert money: [ex: 1.00, 0.50, 0.20, ... or 'cancel']: ")
        # accepted money - coins / cash
        if money_inserted not in ('0.01', '0.02', '0.05', '0.10', '0.20', '0.50', '1.00', '2.00',
                                  '5.00', '10.00', '20.00', '50.00', 'cancel'):
            print('Invalid input. Please enter correct values.')
        else:
            if money_inserted == 'cancel':  # if the user cancels payment at any time
                payment_session = False
                print('Payment cancelled.')
                for key, value in session_money.items():
                    while value > 0:
                        print(f'Return {key}')
                        value -= 1
                break

            money_inserted = Decimal(money_inserted)
            session_money[money_inserted] += 1
            money_collected += money_inserted
            if money_collected >= to_pay:
                print('Thank you for the payment.')

                # logic to add money to respective money_in_machine slots
                for coin, value in session_money.items():
                    if value:
                        money_in_machine[coin] = money_in_machine[coin] + value
                return_balance = money_collected - to_pay
                if return_balance > 0:
                    print(f'Please take the change: {return_balance:.2f}')
                    change = {}
                    coin_denominations = sorted(money_in_machine.keys(), reverse=True)
                    for coin in coin_denominations:
                        while return_balance >= coin and money_in_machine[coin] > 0:
                            # Deduct the coin from the balance and update the count
                            return_balance -= coin
                            money_in_machine[coin] -= 1

                            # Update the change dictionary
                            if coin in change:
                                change[coin] += 1
                            else:
                                change[coin] = 1

                    # Add a check for the smallest denomination (0.01)
                    if return_balance > 0 and Decimal('0.01') in money_in_machine and money_in_machine[
                        Decimal('0.01')] > 0:
                        change[Decimal('0.01')] = round(return_balance / Decimal('0.01'), 2)

                print(change)
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
    return cup


def print_inventory():  # called using .report command
    print('Inventory level: ')
    for item, value in inventory.items():
        print(f'{item} - {value}')
    for coin, value in money_in_machine.items():
        print(f'{coin} - {value}')

def get_selection(user_input):
    if user_input == '1':
        selection = 'espresso'
        check = check_resource(selection)
        if check:
            print('You have selected Espresso')
        else:
            selection = None
            print('Sorry! Not enough resources to make Espresso')
    elif user_input == '2':
        selection = 'latte'
        check = check_resource(selection)
        if check:
            print('You have selected Latte')
        else:
            selection = None
            print('Sorry! Not enough resources to make Latte')
    elif user_input == '3':
        selection = 'cappuccino'
        check = check_resource(selection)
        if check:
            print('You have selected Cappuccino')
        else:
            selection = None
            print('Sorry! Not enough resources to make Cappuccino')
    elif user_input == '.report':
        selection = user_input
        print_inventory()
    elif user_input == '.off':
        selection = user_input
    else:
        print('Invalid choice. Please try again. ')
        selection = None
    return selection


def turn_off():  # Admin user enters '.off' command
    print('Shutting down')
    power = False
    return power


def warn_low_resource():
    if any(value <= Decimal('300') for value in inventory.values()):
        return f'!! ---Warning. Low on resources {inventory}--- !!'
    return None


def warn_low_on_change():
    if any(value <= Decimal('15') for value in money_in_machine.values()):
        return f'!! ---Warning. Low on change {money_in_machine}--- !!'
    return None

power = True
while power:  # System is ON
    print('-- Python Coffee Vending Machine --')
    print('Welcome. What would you like?')
    selection = None

    while selection is None:
        user_input = input('Type [1] for Espresso, [2] for Latte, [3] for Cappuccino?')
        selection = get_selection(user_input)

        if selection == '.off':  # code is terminated, turning off for maintenance and refilling
            power = turn_off()

        elif selection in ['espresso', 'latte', 'cappuccino']:
            payment = process_coins(selection)
            if payment:
                drink = prepare_drink(selection)
                print(f'Please grab your {selection}(Ingredients: {drink}). Enjoy.\n\n')

        print(warn_low_resource()) if warn_low_resource() is not None else ''
        print(warn_low_on_change()) if warn_low_on_change() is not None else ''

    print(money_in_machine)
