import config, os
import binance_futures
from datetime import datetime
from termcolor import colored
troubleshooting = config.troubleshooting

# ==========================================================================================================================================================================
#                                              Heikin Ashi Calculations & Candle Types
# ==========================================================================================================================================================================
def initial_Open(klines)  : return (float(klines[-4][1]) + float(klines[-4][4])) / 2
def initial_Close(klines) : return (float(klines[-4][1]) + float(klines[-4][2]) + float(klines[-4][3]) + float(klines[-4][4])) / 4

def firstrun_Open(klines) : return (initial_Open(klines) + initial_Close(klines)) / 2
def firstrun_Close(klines): return (float(klines[-3][1]) + float(klines[-3][2]) + float(klines[-3][3]) + float(klines[-3][4])) / 4
def firstrun_High(klines) : return max(float(klines[-3][2]), firstrun_Open(klines), firstrun_Close(klines))
def firstrun_Low(klines)  : return min(float(klines[-3][3]), firstrun_Open(klines), firstrun_Close(klines))

def previous_Open(klines) : return (firstrun_Open(klines) + firstrun_Close(klines)) / 2
def previous_Close(klines): return (float(klines[-2][1]) + float(klines[-2][2]) + float(klines[-2][3]) + float(klines[-2][4])) / 4
def previous_High(klines) : return max(float(klines[-2][2]), previous_Open(klines), previous_Close(klines))
def previous_Low(klines)  : return min(float(klines[-2][3]), previous_Open(klines), previous_Close(klines))

def current_Open(klines)  : return (previous_Open(klines) + previous_Close(klines)) / 2
def current_Close(klines) : return (float(klines[-1][1]) + float(klines[-1][2]) + float(klines[-1][3]) + float(klines[-1][4])) / 4
def current_High(klines)  : return max(float(klines[-1][2]), current_Open(klines), current_Close(klines))
def current_Low(klines)   : return min(float(klines[-1][3]), current_Open(klines), current_Close(klines))

def firstrun_candle(klines):
    if   (firstrun_Open(klines) == firstrun_High(klines)): return "RED"
    elif (firstrun_Open(klines) == firstrun_Low(klines)) : return "GREEN"
    elif (firstrun_Open(klines) > firstrun_Close(klines)): return "RED_INDECISIVE"
    elif (firstrun_Close(klines) > firstrun_Open(klines)): return "GREEN_INDECISIVE"
    else: return "NO_MOVEMENT"

def previous_candle(klines):
    if   (previous_Open(klines) == previous_High(klines)): return "RED"
    elif (previous_Open(klines) == previous_Low(klines)) : return "GREEN"
    elif (previous_Open(klines) > previous_Close(klines)): return "RED_INDECISIVE"
    elif (previous_Close(klines) > previous_Open(klines)): return "GREEN_INDECISIVE"
    else: return "NO_MOVEMENT"

def current_candle(klines):
    if   (current_Open(klines) == current_High(klines)): return "RED"
    elif (current_Open(klines) == current_Low(klines)) : return "GREEN"
    elif (current_Open(klines) > current_Close(klines)): return "RED_INDECISIVE"
    elif (current_Close(klines) > current_Open(klines)): return "GREEN_INDECISIVE"
    else: return "NO_MOVEMENT"

# ==========================================================================================================================================================================
#                                                        OUTPUT TO CONSOLE
# ==========================================================================================================================================================================
def output_current(klines): # return GREEN // GREEN_INDECISIVE // RED // RED_INDECISIVE // NO_MOVEMENT
    if troubleshooting:
        print("The current_Open  is :   " + str(current_Open(klines)))
        print("The current_Close is :   " + str(current_Close(klines)))
        print("The current_High  is :   " + str(current_High(klines)))
        print("The current_Low   is :   " + str(current_Low(klines)))

    milliseconds = int(klines[-1][0]) - int(klines[-2][0])
    if milliseconds == 1 * 60000: interval = "1 MINUTE  "
    elif milliseconds == 3 * 60000: interval = "3 MINUTE  "
    elif milliseconds == 5 * 60000: interval = "5 MINUTE  "
    elif milliseconds == 15 * 60000: interval = "15 MINUTE "
    elif milliseconds == 30 * 60000: interval = "30 MINUTE "
    elif milliseconds == 1 * 60 * 60000: interval = "1 HOUR    "
    elif milliseconds == 2 * 60 * 60000: interval = "2 HOUR    "
    elif milliseconds == 4 * 60 * 60000: interval = "4 HOUR    "
    elif milliseconds == 6 * 60 * 60000: interval = "6 HOUR    "
    elif milliseconds == 12 * 60 * 60000: interval = "12 HOUR   "

    current = current_candle(klines)
    if   current == "GREEN" or current == "GREEN_INDECISIVE": print(colored("RECENT " + interval + ":   " + current, "green"))
    elif current == "RED"   or current == "RED_INDECISIVE"  : print(colored("RECENT " + interval + ":   " + current, "red"))
    else: print(colored("RECENT " + interval + ":   " + current, "yellow"))
    return current

def output_previous(klines): # return GREEN // GREEN_INDECISIVE // RED // RED_INDECISIVE // NO_MOVEMENT
    if troubleshooting:
        print("The previous_Open  is :   " + str(previous_Open(klines)))
        print("The previous_Close is :   " + str(previous_Close(klines)))
        print("The previous_High  is :   " + str(previous_High(klines)))
        print("The previous_Low   is :   " + str(previous_Low(klines)))

    milliseconds = int(klines[-1][0]) - int(klines[-2][0])
    if milliseconds == 1 * 60000: interval = "1 MINUTE"
    elif milliseconds == 3 * 60000: interval = "3 MINUTE"
    elif milliseconds == 5 * 60000: interval = "5 MINUTE"
    elif milliseconds == 1 * 60 * 60000: interval = "1 HOUR  "
    elif milliseconds == 2 * 60 * 60000: interval = "2 HOUR  "
    elif milliseconds == 4 * 60 * 60000: interval = "4 HOUR  "
    elif milliseconds == 6 * 60 * 60000: interval = "6 HOUR  "
    elif milliseconds == 12 * 60 * 60000: interval = "12 HOUR "

    previous = previous_candle(klines)
    if   previous == "GREEN" or previous == "GREEN_INDECISIVE": print(colored("PREVIOUS " + interval + ":   " + previous, "green"))
    elif previous == "RED"   or previous == "RED_INDECISIVE"  : print(colored("PREVIOUS " + interval + ":   " + previous, "red"))
    else: print(colored("RECENT " + interval + ":   " + previous, "yellow"))
    return previous

def output_firstrun(klines): # return GREEN // GREEN_INDECISIVE // RED // RED_INDECISIVE // NO_MOVEMENT
    if troubleshooting:
        print("The firstrun_Open  is :   " + str(firstrun_Open(klines)))
        print("The firstrun_Close is :   " + str(firstrun_Close(klines)))
        print("The firstrun_High  is :   " + str(firstrun_High(klines)))
        print("The firstrun_Low   is :   " + str(firstrun_Low(klines)))

    milliseconds = int(klines[-1][0]) - int(klines[-2][0])
    if milliseconds == 1 * 60000: interval = "1 MINUTE"
    elif milliseconds == 3 * 60000: interval = "3 MINUTE"
    elif milliseconds == 5 * 60000: interval = "5 MINUTE"
    elif milliseconds == 1 * 60 * 60000: interval = "1 HOUR  "
    elif milliseconds == 2 * 60 * 60000: interval = "2 HOUR  "
    elif milliseconds == 4 * 60 * 60000: interval = "4 HOUR  "
    elif milliseconds == 6 * 60 * 60000: interval = "6 HOUR  "
    elif milliseconds == 12 * 60 * 60000: interval = "12 HOUR "

    firstrun = firstrun_candle(klines)
    if   firstrun == "GREEN" or firstrun == "GREEN_INDECISIVE": print(colored("FIRSTRUN " + interval + ":   " + firstrun, "green"))
    elif firstrun == "RED"   or firstrun == "RED_INDECISIVE"  : print(colored("FIRSTRUN " + interval + ":   " + firstrun, "red"))
    else: print(colored("RECENT " + interval + ":   " + firstrun, "yellow"))
    return firstrun
# ==========================================================================================================================================================================
#                                                             WAR FORMATION
# ==========================================================================================================================================================================
def WAR_FORMATION(klines):
    if current_candle(klines) == "GREEN" or current_candle(klines) == "GREEN_INDECISIVE":
        if  previous_High(klines) > firstrun_High(klines) and \
            previous_Close(klines) > firstrun_Close(klines) and \
            strength_of_current(klines) == "STRONG": return True

    elif current_candle(klines) == "RED" or current_candle(klines) == "RED_INDECISIVE":
        if  previous_Low(klines) < firstrun_Low(klines) and \
            previous_Close(klines) < firstrun_Close(klines) and \
            strength_of_current(klines) == "STRONG": return True
            
def pencil_wick_test(klines):
    volume_confirmation = (binance_futures.current_volume(klines) > (binance_futures.previous_volume(klines) / 2))

    if current_candle(klines) == "GREEN":
        if  current_High(klines)  > previous_High(klines)  and \
            current_Close(klines) > previous_Close(klines) and \
            volume_confirmation: 
            return True
    elif current_candle(klines) == "RED":
        if  current_Low(klines)   < previous_Low(klines)   and \
            current_Close(klines) < previous_Close(klines) and \
            volume_confirmation:
                return True

def one_minute_exit_test(klines, POSITION):
    if POSITION == "LONG":
        if (previous_Close(klines) > current_High(klines)) or (previous_Close(klines) > current_Close(klines)): return True
    elif POSITION == "SHORT":
        if (previous_Close(klines) < current_Low(klines)) or (previous_Close(klines) < current_Close(klines)): return True

def pattern_broken(klines): # return "BROKEN" // "NOT_BROKEN"
    current  = current_candle(klines)
    if ((current == "GREEN" or current == "GREEN_INDECISIVE") and (firstrun_High(klines) > previous_High(klines)) and (previous_High(klines) > current_High(klines))) or \
       ((current == "RED"   or current == "RED_INDECISIVE")   and (firstrun_Low(klines)  < previous_Low(klines))  and (previous_Low(klines)  < current_Low(klines))) or \
       ((current == "GREEN" or current == "GREEN_INDECISIVE") and (previous_Close(klines) > current_Close(klines))) or \
       ((current == "RED"   or current == "RED_INDECISIVE")   and (previous_Close(klines) < current_Close(klines))): return "BROKEN"
    else: return "NOT_BROKEN"

# ==========================================================================================================================================================================
#                                                          IDENTIFY STRENGTH
# ==========================================================================================================================================================================
def strength_of_current(klines):
    previous = previous_candle(klines)
    current = current_candle(klines)

    open  = current_Open(klines)
    close = current_Close(klines)
    high  = current_High(klines)
    low   = current_Low(klines)

    if current == "GREEN": 
        upper_wick = high - close
        candlebody = close - open
        if upper_wick > candlebody: strength = "WEAK"
        else: strength = "STRONG"

    elif current == "RED":
        lower_wick = close - low
        candlebody = open - close
        if lower_wick > candlebody: strength = "WEAK"
        else: strength = "STRONG"
    
    elif current == "GREEN_INDECISIVE":
        upper_wick = high - close
        lower_wick = open - low
        candlebody = close - open
        if candlebody > lower_wick:
            if previous == "GREEN": strength = "WEAK"
            else: strength = "STRONG"
        else:
            if  high  > previous_High(klines)  and \
                close > previous_Close(klines) and \
                open  > previous_Open(klines)  and \
                low   > previous_Low(klines): strength = "STRONG"
            else: strength = "WEAK"

    elif current == "RED_INDECISIVE":
        upper_wick = high - open
        lower_wick = close - low
        candlebody = open - close
        if candlebody > upper_wick:
            if previous == "RED": strength = "WEAK"
            else: strength = "STRONG"
        else:
            if  high  < previous_High(klines)  and \
                close < previous_Close(klines) and \
                open  < previous_Open(klines)  and \
                low   < previous_Low(klines): strength = "STRONG"
            else: strength = "WEAK"
    return strength

def strength_of_previous(klines):
    firstrun = firstrun_candle(klines)
    previous = previous_candle(klines)

    open  = previous_Open(klines)
    close = previous_Close(klines)
    high  = previous_High(klines)
    low   = previous_Low(klines)

    if previous == "GREEN": 
        upper_wick = high - close
        candlebody = close - open
        if upper_wick > candlebody: strength = "WEAK"
        else: strength = "STRONG"

    elif previous == "RED":
        lower_wick = close - low
        candlebody = open - close
        if lower_wick > candlebody: strength = "WEAK"
        else: strength = "STRONG"
    
    elif previous == "GREEN_INDECISIVE":
        upper_wick = high - close
        lower_wick = open - low
        candlebody = close - open
        if candlebody > lower_wick:
            if firstrun == "GREEN": strength = "WEAK"
            else: strength = "STRONG"
        else:
            if  high  > firstrun_High(klines)  and \
                close > firstrun_Close(klines) and \
                open  > firstrun_Open(klines)  and \
                low   > firstrun_Low(klines): strength = "STRONG"
            else: strength = "WEAK"

    elif previous == "RED_INDECISIVE":
        upper_wick = high - open
        lower_wick = close - low
        candlebody = open - close
        if candlebody > upper_wick:
            if firstrun == "RED": strength = "WEAK"
            else: strength = "STRONG"
        else:
            if  high  < firstrun_High(klines)  and \
                close < firstrun_Close(klines) and \
                open  < firstrun_Open(klines)  and \
                low   < firstrun_Low(klines): strength = "STRONG"
            else: strength = "WEAK"
    return strength
