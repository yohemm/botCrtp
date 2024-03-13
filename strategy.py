import pandas as pd
from indicator import Indicator
from log import Log
class Strategie():
    STRATS = {"sma":['sma200/600'], "new_strat":['sma200/600','bollinger_bands'], "rsi": ['rsi'], "rsi/macd":['rsi', 'macd']}

    def __init__(self, strat) -> None:
        if(strat in Strategie.STRATS.keys()):
            self.strat = strat
            self.ordersLogs = []
            self.indicators = {indicator:Indicator(indicator) for indicator in self.STRATS[strat]}
        pass
    def resume(self)-> dict:
        stats = {'highBuy': Log.highBuy(self.ordersLogs),'lowBuy':  Log.lowBuy(self.ordersLogs), 'avgBuy':  Log.avgBuy(self.ordersLogs), 'countBuy' : Log.countBuy(self.ordersLogs), 'highSell': Log.highSell(self.ordersLogs), 'lowSell':Log.lowSell(self.ordersLogs), 'avgSell':  Log.avgSell(self.ordersLogs), 'countSell' : Log.countSell(self.ordersLogs)}
        return stats

    def addIndicator(self, df) -> list:
        for indicator in self.indicators.values():
            indicator.addIndicator(df)
        return df
    def addLog(self, orderTurn: int, price, time):
        self.ordersLogs.append(Log(orderTurn, price, time))
        
    # int [-1;1]
    def doOrder(self, df, closeIndex, lastIndex) -> int:
        res = 0
        match self.strat:
            case "new_strat":
                if(self.indicators['bollinger_bands'].signal(df, closeIndex, lastIndex) == 1):
                    res = self.indicators['sma200/600'].signal(df, closeIndex, lastIndex)
                # boolPerc = 1 - df['bolbandl'][closeIndex]/df['bolbandh'][closeIndex]
                # if(boolPerc> 0.12):
                #     if df['SMA200'][closeIndex] > df['SMA600'][closeIndex]:
                #         res = 1
                #     if df['SMA200'][closeIndex] < df['SMA600'][closeIndex]:
                #         res = -1
            case "sma":
                res = self.indicators['sma200/600'].signal(df, closeIndex, lastIndex)
            case "rsi":
                # res = 0
                # if df['RSI'][closeIndex] < 30:
                #     res = 1
                # if df['RSI'][closeIndex] > 70:
                #     res = -1
                res = self.indicators['rsi'].signal(df, closeIndex, lastIndex)
            case "rsi/macd":
                if (self.indicators['rsi'].signal(df, closeIndex, lastIndex) > 0 and self.indicators['macd'].signal(df, closeIndex, lastIndex) == 1) | (self.indicators['rsi'].signal(df, closeIndex, lastIndex) < 0 and self.indicators['macd'].signal(df, closeIndex, lastIndex) == 1):
                    res = abs(self.indicators['rsi'].signal(df, closeIndex, lastIndex))
                if (self.indicators['rsi'].signal(df, closeIndex, lastIndex) < 0 and self.indicators['macd'].signal(df, closeIndex, lastIndex) == -1) | (self.indicators['rsi'].signal(df, closeIndex, lastIndex) > 0 and self.indicators['macd'].signal(df, closeIndex, lastIndex) == -1):
                    res = abs(self.indicators['rsi'].signal(df, closeIndex, lastIndex)) * -1
                if res != 0:
                    print(res)
                # elif self.indicators['rsi'].signal(df, closeIndex, lastIndex) != 0 and self.indicators['macd'].signal(df, closeIndex, lastIndex) != 0:
                #     print(self.indicators['rsi'].signal(df, closeIndex, lastIndex),self.indicators['macd'].signal(df, closeIndex, lastIndex))
        if(res!=0):
            self.addLog(res, df['close'][closeIndex], df['timestamp'][closeIndex])
        return res


