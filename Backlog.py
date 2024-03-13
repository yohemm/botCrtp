from datetime import timedelta
from Strategy import Strategy
from binance.client import Client
import pandas as pd

class BackLog():
    INTERVALS = {Client.KLINE_INTERVAL_30MINUTE: pd.Timedelta(minutes=30),Client.KLINE_INTERVAL_1HOUR: pd.Timedelta(hours=1),Client.KLINE_INTERVAL_2HOUR: pd.Timedelta(hours=2),Client.KLINE_INTERVAL_4HOUR: pd.Timedelta(hours=4),Client.KLINE_INTERVAL_8HOUR: pd.Timedelta(hours=8),Client.KLINE_INTERVAL_12HOUR: pd.Timedelta(hours=12),Client.KLINE_INTERVAL_1DAY: pd.Timedelta(days=1),Client.KLINE_INTERVAL_1WEEK: pd.Timedelta(weeks=1)}
    def __init__(self, df:pd.DataFrame, symbol:str="EXEMPLEUSDT", interval=Client.KLINE_INTERVAL_1HOUR, amount:int=0, strategyName:str='') -> None:
        client = Client()
        self.timeInterval = interval

        if(symbol != "EXEMPLEUSDT"):
            self.symbol = symbol
        else:
            self.symbol = input("Choisir un Coin : ").upper() + "USDT"
        if amount <= 0:    
            self.walletStart = int(input("Choisir un montant de départ : "))
        else:
            self.walletStart = amount
        # print(df)
        if len(df) > 0:
            self.startDay = "01 january 2017"
            klinesT = client.get_historical_klines(self.symbol, self.timeInterval, self.startDay )

            # Créer un tableau grâce aux données
            df = pd.DataFrame(klinesT, columns = ['timestamp', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'quote_av', 'trades', 'tb_base_av', 'tb_quote_av', 'ignore' ])

        
        self.startDay = df.last_valid_index()

        # Supprime les colonnes inutiles
        df.drop(columns = df.columns.difference(['timestamp','open','high','low','close','volume']), inplace=True)

        # Convertit les colonnes en numéric
        for col in df.columns:
            df[col] = pd.to_numeric(df[col])

        # Convertit les dates dans un format lisible
        df = df.set_index(df['timestamp'])
        df.index = pd.to_datetime(df.index, unit='ms')
        del df['timestamp']

        while not(strategyName in Strategy.STRATS):
            print(Strategy.STRATS)
            strategyName = input("Choissé votre stratégie : ")
        self.strategy = Strategy(df,strategyName, self.walletStart, self.INTERVALS[self.timeInterval])
        self.df = df
        print("loaded :",self)
        pass

    def start(self):
        print("start :",self)
        self.result = {'index':[], 'stable': [], 'coin':[]}
        self.orders = []
        for index, row in self.df.iterrows():
            stable, coin, finalOrder = self.strategy.task(index)
            self.result['stable'].append(stable)
            self.result['coin'].append(coin)
            self.result['index'].append(index)
            if(finalOrder != None):
                self.orders.append(finalOrder)

    def seeResult(self):
        coinInStable = (self.result['coin'][-1] * self.df['close'][self.startDay]) - 0.0007 * (self.result['coin'][-1] * self.df['close'][self.startDay])
        bAH = self.walletStart/self.df['close'][self.df.first_valid_index()]*self.df['close'][self.startDay]
        print("==========================================================================")
        print("------- Backtest Informations -------")
        print("Pair Symbol :", self.symbol)
        print("Strategy : "+ self.strategy.strat)
        print("Period :", str(self.df.first_valid_index()) +"->"+ str(self.startDay))
        print("Starting balance :", str(self.strategy.amount)+"$")
        print("------- General Informations -------")
        print("Final balance :", str(round(self.result['stable'][-1] +coinInStable, 2))+"$")
        print("Performance Vs Us Dollar :",str(round((self.result['stable'][-1] +coinInStable)/self.walletStart*100, 2))+"%")
        print("Performance Vs Buy and Hold :",  str(round((self.result['stable'][-1] +coinInStable)/bAH*100,2))+"%")
        print("Best Trade :",  str(round(self.bestTrade(), 2))+"%")
        print("Worst Trade :",  str(round(self.worstTrade(), 2))+"%")
        print("Worst drawBack :",  str(round(self.drawBack(),2))+ "%")
        print("Total fees :",  str(round(self.strategy.fee,2)) + "$")
        print("------- Trades Informations -------")
        print("Total Trade on Period :",  len(self.orders))
        print("Number of negative trades :",  str(round(self.negativeTrade(),2)))
        print("Number of positive trades :",  str(round(self.positiveTrade(),2)))
        print("Trade win rate ration :",  round((self.positiveTrade()/self.negativeTrade()),2))
        print("Trade win rate ration percent :",  round((self.avgPositiveTrade()/(-1*self.avgNegativeTrade())),2))
        print("Average performance trades :",  str(round(self.avgTrade(),2))+ "%")
        print("Average positive trades :",  str(round(self.avgPositiveTrade(),2))+ "%")
        print("Average negative trades :",  str(round(self.avgNegativeTrade(),2))+ "%")
        print("Average negative/positiv trades :",  str(round((self.avgPositiveTrade()+self.avgNegativeTrade())/2,2))+ "%")
        print("------- Trades Reasons -------")
        pass

    def drawBack(self):
        amountPerDay = self.amountDict()
        best = amountPerDay['amount'][0]
        drawBack = 0
        if self.orders == None:
            return 0
        for amount in amountPerDay['amount']:
            if best < amount:
                best = amount
            else:
                actualdrawback = (1 - (amount / best))* 100
                if actualdrawback > drawBack :
                    drawBack = actualdrawback
        return drawBack
    def amountDict(self):
        res = {'index':[], 'amount':[]}
        for i in range(len(self.result['stable'])):
            index = self.result['index'][i]
            coinInStable = (self.result['coin'][-1] * self.df['close'][index]) - 0.0007 * (self.result['coin'][-1] * self.df['close'][index])
            res['index'].append(index)
            res['amount'].append(self.result['stable'][i] + coinInStable)
        return res


    def bestTrade(self):
        best = (self.orders[0].amount*self.df['close'][self.orders[0].close])/(self.orders[0].amount*self.df['close'][self.orders[0].open])*100 -100
        if self.orders == None:
            return 0
        for order in self.orders:
            renta = (order.amount*self.df['close'][order.close])/(order.amount*self.df['close'][order.open])*100 -100
            best = renta if best < renta else best
        return best
            
    def worstTrade(self):
        worst = (self.orders[0].amount*self.df['close'][self.orders[0].close])/(self.orders[0].amount*self.df['close'][self.orders[0].open])*100 -100
        if self.orders == None:
            return 0
        for order in self.orders:
            renta = (order.amount*self.df['close'][order.close])/(order.amount*self.df['close'][order.open])*100 -100
            worst = renta if worst > renta else worst
        return worst
    def negativeTrade(self):
        total = 0
        if self.orders == None:
            return 0
        for order in self.orders:
            renta = (order.amount*self.df['close'][order.close])/(order.amount*self.df['close'][order.open])*100 -100
            total+=1 if 0 > renta else 0
        return total
    def positiveTrade(self):
        total = 0
        if self.orders == None:
            return 0
        for order in self.orders:
            renta = (order.amount*self.df['close'][order.close])/(order.amount*self.df['close'][order.open])*100 -100
            total+=1 if 0 < renta else 0
        return total
    def avgTrade(self):
        total = 0
        if self.orders == None:
            return 0
        for order in self.orders:
            total+= (order.amount*self.df['close'][order.close])/(order.amount*self.df['close'][order.open])*100 -100
        return total/len(self.orders)
    def avgPositiveTrade(self):
        total = 0
        if self.orders == None:
            return 0
        for order in self.orders:
            renta = (order.amount*self.df['close'][order.close])/(order.amount*self.df['close'][order.open])*100 -100
            total+= renta if renta > 0 else 0 
        return total/self.positiveTrade()
    def avgNegativeTrade(self):
        total = 0
        if self.orders == None:
            return 0
        for order in self.orders:
            renta = (order.amount*self.df['close'][order.close])/(order.amount*self.df['close'][order.open])*100 -100
            total+= renta if renta < 0 else 0 
        return total/self.negativeTrade()

    def graph(self):
        pass

    def __str__(self) -> str:
        return "Stratégie : "+ self.strategy.strat + " | Symbol : "+self.symbol+" | interval : "+ self.timeInterval+" | Start At  "+str(self.start)
symbols = [ "ETHUSDT"]
strats = ["new3", "new2"]
interval = Client.KLINE_INTERVAL_1HOUR
backLogs = []
amount=100

for symbol in symbols:
    startDay = "01 january 2017"
    klinesT = Client().get_historical_klines(symbol, interval, startDay )

    # Créer un tableau grâce aux données
    df = pd.DataFrame(klinesT, columns = ['timestamp', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'quote_av', 'trades', 'tb_base_av', 'tb_quote_av', 'ignore' ])
    for strat in strats:
        print(symbol, interval, startDay, strat)
        backLogs.append(BackLog(df=df,symbol=symbol, interval=interval, amount=amount, strategyName=strat))
for backlog in backLogs:
    backlog.start()
for backlog in backLogs:
    backlog.seeResult()
        
        

