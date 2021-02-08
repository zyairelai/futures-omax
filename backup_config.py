live_trade      = True
clear_direction = True   # True to minimize lose, False to maximize profit

while True:
    print("\nHere are the supported Pairs: ")
    print("1. BTC-USDT")
    print("2. ETH-USDT")
    # print("3. LTC-USDT")

    input_pair = input("\nChoose your Pair :   ").upper() or 'BTC'

    if (input_pair == '1') or (input_pair == 'BTC'):
        coin            = "BTC"
        quantity        = 0.001     # Minimum 0.001
        leverage        = 50        # Maximum 125 // Recommended 75-99 // Oracle 50x
        round_decimal   = 2
        break

    elif (input_pair == '2') or (input_pair == 'ETH'):
        coin            = "ETH"
        quantity        = 0.01      # Minimum 0.01
        leverage        = 50        # Maximum 100 // Recommended 50-75 // Oracle 40x
        round_decimal   = 2
        break

    # elif (input_pair == '3') or (input_pair == 'LTC'):
    #     coin            = "LTC"
    #     quantity        = 0.05      # Minimum 0.01
    #     leverage        = 30        # Maximum 75 // Recommended 30-45
    #     round_decimal   = 2
    #     break

    else: print("❗Invalid Number❗Try again❗\n")

pair = coin + "USDT"

print("Pair Name        :   " + str(pair))
print("Trade Quantity   :   " + str(quantity) + " " + str(coin))
print()