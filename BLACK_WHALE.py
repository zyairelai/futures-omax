try:
    import os, time, requests, socket, urllib3
    import config
    import heikin_ashi
    import get_position
    import binance_futures
    from datetime import datetime
    from termcolor import colored
    from binance.exceptions import BinanceAPIException
    live_trade = config.live_trade
    profit = 0.6
# ==========================================================================================================================================================================
#                    BLACK WHALE - ONLY ENTER WHEN THE VOLUME IS SMALL MEDIUM LARGE AND CANDLE SIZE WAR FORMATION
# ==========================================================================================================================================================================
    def lets_make_some_money():
        position_info = get_position.get_position_info()
        klines_1min   = binance_futures.KLINE_INTERVAL_1MINUTE()
        klines_1HOUR  = binance_futures.KLINE_INTERVAL_1HOUR()

        print("First hr Volume  :   " + str(binance_futures.firstrun_volume(klines_1HOUR)))
        print("Previous Volume  :   " + str(binance_futures.previous_volume(klines_1HOUR)))
        print("Current Volume   :   " + str(binance_futures.current_volume(klines_1HOUR)))

        heikin_ashi.output_firstrun(klines_1HOUR)
        heikin_ashi.output_previous(klines_1HOUR)

        direction = heikin_ashi.output_current(klines_1HOUR)
        heikin_ashi.output_current(klines_1min)

        if position_info == "LONGING":
            if get_position.get_unRealizedProfit(profit) == "PROFIT" and heikin_ashi.one_minute_exit_test(klines_1min, "LONG"):
                if live_trade: binance_futures.close_position("LONG")
                record_timestamp(klines_1HOUR, "BLACK_WHALE")
                print("ACTION           :   💰 CLOSE_LONG 💰")
            else: print(colored("ACTION           :   HOLDING_LONG", "green"))

        elif position_info == "SHORTING":
            if get_position.get_unRealizedProfit(profit) == "PROFIT" and heikin_ashi.one_minute_exit_test(klines_1min, "SHORT"):
                if live_trade: binance_futures.close_position("SHORT")
                record_timestamp(klines_1HOUR, "BLACK_WHALE")
                print("ACTION           :   💰 CLOSE_SHORT 💰")
            else: print(colored("ACTION           :   HOLDING_SHORT", "red"))

        else:
            if direction == "GREEN" and GO_LONG(klines_1HOUR, klines_1min) and (retrieve_timestamp("BLACK_WHALE") != current_kline_timestamp(klines_1HOUR)):
                if live_trade: binance_futures.open_position("LONG", config.quantity)
                record_timestamp(klines_1HOUR, "BLACK_WHALE")
                print(colored("ACTION           :   🚀 GO_LONG 🚀", "green"))

            elif direction == "RED" and GO_SHORT(klines_1HOUR, klines_1min) and (retrieve_timestamp("BLACK_WHALE") != current_kline_timestamp(klines_1HOUR)):
                if live_trade: binance_futures.open_position("SHORT", config.quantity)
                record_timestamp(klines_1HOUR, "BLACK_WHALE")
                print(colored("ACTION           :   💥 GO_SHORT 💥", "red"))

            else: print("ACTION           :   🐺 WAIT 🐺")

        print("Last action executed @ " + datetime.now().strftime("%H:%M:%S") + "\n")

# ==========================================================================================================================================================================
#                                                    ENTRY_EXIT CONDITIONS
# ==========================================================================================================================================================================
    def GO_LONG(klines_1HOUR, klines_1min):
        if  heikin_ashi.strength_of_current(klines_1min) == "STRONG" and \
            heikin_ashi.current_candle(klines_1min) == "GREEN" and \
            heikin_ashi.pencil_wick_test(klines_1min) and \
            heikin_ashi.WAR_FORMATION(klines_1HOUR) and \
            VOLUME_FORMATION(klines_1HOUR): return True

    def GO_SHORT(klines_1HOUR, klines_1min):
        if  heikin_ashi.strength_of_current(klines_1min) == "STRONG" and \
            heikin_ashi.current_candle(klines_1min) == "RED" and \
            heikin_ashi.pencil_wick_test(klines_1min) and \
            heikin_ashi.WAR_FORMATION(klines_1HOUR) and \
            VOLUME_FORMATION(klines_1HOUR): return True

    def VOLUME_FORMATION(klines):
        if  binance_futures.current_volume(klines) > binance_futures.previous_volume(klines) and \
            binance_futures.previous_volume(klines) > binance_futures.firstrun_volume(klines): return True

# ==========================================================================================================================================================================
#                                                      RECORD TIMESTAMP
# ==========================================================================================================================================================================
    def record_timestamp(kline, filename):
        if not os.path.exists("TIMESTAMP"): os.makedirs("TIMESTAMP")
        if not os.path.exists(os.path.join("TIMESTAMP", config.pair)): os.makedirs(os.path.join("TIMESTAMP", config.pair))

        with open((os.path.join("TIMESTAMP", config.pair, filename + ".txt")), "w", encoding="utf-8") as timestamp_record:
            timestamp_record.write(str(current_kline_timestamp(kline)))

    def retrieve_timestamp(filename):
        with open((os.path.join("TIMESTAMP", config.pair, filename + ".txt")), "r", encoding="utf-8") as timestamp_record:
            return int(timestamp_record.read())

    def current_kline_timestamp(kline):
        return kline[-1][0] # This will return <int> type of timestamp

# ==========================================================================================================================================================================
#                                                        DEPLOY THE BOT
# ==========================================================================================================================================================================

    if config.live_trade: print(colored("LIVE TRADE IS ENABLED\n", "green"))
    else: print(colored("LIVE TRADE IS NOT ENABLED\n", "red"))

    if binance_futures.position_information()[0].get('marginType') != "isolated": binance_futures.change_margin_to_ISOLATED()
    if int(binance_futures.position_information()[0].get("leverage")) != config.leverage:
        binance_futures.change_leverage(config.leverage)
        print(colored("CHANGED LEVERAGE :   " + binance_futures.position_information()[0].get("leverage") + "x\n", "red"))

    while True:
        try:
            lets_make_some_money()
            time.sleep(5)

        except (socket.timeout,
                BinanceAPIException,
                urllib3.exceptions.ProtocolError,
                urllib3.exceptions.ReadTimeoutError,
                requests.exceptions.ConnectionError,
                requests.exceptions.ConnectTimeout,
                requests.exceptions.ReadTimeout,
                ConnectionResetError, KeyError, OSError) as e:

            if not os.path.exists("ERROR"): os.makedirs("ERROR")
            with open((os.path.join("ERROR", config.pair + ".txt")), "a", encoding="utf-8") as error_message:
                error_message.write("[!] " + config.pair + " - " + "Created at : " + datetime.today().strftime("%d-%m-%Y @ %H:%M:%S") + "\n")
                error_message.write(str(e) + "\n\n")

except KeyboardInterrupt: print("\n\nAborted.\n")
