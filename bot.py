import pandas as pd
from strategy import Strategie
from binance.client import Client
import matplotlib.pyplot as plt
class Bot():
    def __init__(self, timeFrame:str, start:str, initialInvest:int = 1000, pair:str="BTCUSDT") -> None:
        self.initialInvest = initialInvest
        self.timeFrame = timeFrame
        self.start = start
        self.pair = pair
        self.strat = Strategie("rsi/macd")

    def __str__(self) -> str:
        return "TimeFrame : " + self.timeFrame+" | coin : "+self.coinName()+ " | first chandel at " + self.start
    
    def klinesTab(self) -> list:
        klinesT = Client().get_historical_klines(self.pair, self.timeFrame, self.start)
        df = pd.DataFrame(klinesT, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'quote_av', 'trades', 'tb_base_av', 'tb_qutoe_av', 'ignore'])
        del df['close_time']
        del df['quote_av']
        del df['trades']
        del df['tb_base_av']
        del df['tb_qutoe_av']
        del df['ignore']
        df['close'] = pd.to_numeric(df['close'])
        df['high'] = pd.to_numeric(df['high'])
        df['low'] = pd.to_numeric(df['low'])
        df['open'] = pd.to_numeric(df['open'])

        df = df.set_index(df['timestamp'])
        df.index = pd.to_datetime(df.index, unit='ms')
        return df

    
    def backlog(self) -> int:
        print(self)
        invest = self.initialInvest
        df = self.klinesTab()
        self.strat.addIndicator(df)
        

        # BACKTEST
        usdt = invest
        coin = 0
        closeIndex = df.first_valid_index()
        lastIndex = df.first_valid_index()
        
        for index, row in df.iterrows():
            res = self.strat.doOrder(df, closeIndex, lastIndex)
            if(res > 0 and usdt > 10):
                coin = (res * usdt) / df['close'][index]
                coin = coin - 0.007 * coin
                usdt = 0
                print("Achat de "+self.coinName()+" a ", df['close'][index], "$ le ", index)
                
            elif(res < 0 and coin > 0.0001):
                usdt = (res * -1 * coin) * df['close'][index]
                usdt = usdt - 0.007 * usdt
                coin = 0
                print("Vente de "+self.coinName()+" a ", df['close'][index], "$ le ", index)
            lastIndex = closeIndex
            closeIndex = index
        finalResult = usdt + coin * df['close'].iloc[-1]
        buyAndHold = invest/df['close'].iloc[0] * df['close'].iloc[-1]
        resumStat = self.strat.resume()
        print(resumStat)
        print("  Resultat              : "+ str(round(finalResult, 4)) + "$ | "+ str(round(finalResult/invest*100, 4)) + "%")
        print("    Res VS Buy and Hold : "+ str(round(buyAndHold, 4)) + "$ | "+ str(round(finalResult/buyAndHold*100, 4))+"%")
        print("    Stats               : highBuy="+ str(resumStat['highBuy'].price) + "$ | lowBuy="+ str(resumStat['lowBuy'].price) + "$ | avgBuy="+ str(resumStat['avgBuy']) + "$ | countBuy="+ str(resumStat['countBuy'])+ " | highSell="+ str(resumStat['highSell'].price) + "$ | lowSell="+ str(resumStat['lowSell'].price) + "$ | avgSell="+ str(resumStat['avgSell']) + "$ | countSell="+ str(resumStat['countSell']))
        graph = df.cumsum()
        indicateur = df.copy()
        graph.plot(x = 'close')
        del indicateur['close']
        del indicateur['open']
        del indicateur['high']
        del indicateur['low']
        del indicateur['timestamp']
        indicateur.cumsum().plot( kind='line')
        plt.show()
        # plt.plot(df['close'], df["df['timestamp']"])
        # plt.xlabel(self.coinName())
        # plt.ylabel("temps")
        # plt.title("BTC/USD")
        return finalResult
    
    def coinName(self):
        return self.pair[:].replace("USDT","")
    

intervalList =[Client.KLINE_INTERVAL_1MINUTE, Client.KLINE_INTERVAL_5MINUTE, Client.KLINE_INTERVAL_15MINUTE, Client.KLINE_INTERVAL_30MINUTE, Client.KLINE_INTERVAL_1HOUR, Client.KLINE_INTERVAL_2HOUR, Client.KLINE_INTERVAL_4HOUR, Client.KLINE_INTERVAL_8HOUR, Client.KLINE_INTERVAL_12HOUR, Client.KLINE_INTERVAL_1DAY, Client.KLINE_INTERVAL_1WEEK, Client.KLINE_INTERVAL_1MONTH]
minIterval = int(input("Saisir le debut des timeFrames [-1:"+str(len(intervalList))+"] : "))
maxIterval = int(input("Saisir la fin des timeFrames [-1:"+str(len(intervalList))+"] : "))
strats = input("liste des stratégies a utilisé : ").replace(" ","").split(",")
bot = Bot(intervalList[0], '01 January 2017', 200)
for strat in strats:
    bot.strat = Strategie(strat)
    for interval in intervalList[minIterval:maxIterval]:
        bot.timeFrame = interval
        bot.pair = "BTCUSDT"
        bot.backlog()
        bot.pair = "ETHUSDT"
        bot.backlog()
    
