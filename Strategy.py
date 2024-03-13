import pandas as pd
from Indicator import Indicator
from oder import Order
class Strategy():
    STRATS = ['sma', 'The Filter', 'The Filter2', 'new', 'new2', 'new3']
    STRATS_INDICATORS = {'sma':[Indicator.INDICATORS[0]], 'The Filter' : [Indicator.INDICATORS[0],Indicator.INDICATORS[1],Indicator.INDICATORS[3]], 'The Filter2' : [Indicator.INDICATORS[0],Indicator.INDICATORS[1],Indicator.INDICATORS[3]], 'new' : [Indicator.INDICATORS[0],Indicator.INDICATORS[1],Indicator.INDICATORS[2],Indicator.INDICATORS[3]], 'new2' : [Indicator.INDICATORS[0],Indicator.INDICATORS[1],Indicator.INDICATORS[2],Indicator.INDICATORS[3]], 'new3' : [Indicator.INDICATORS[0],Indicator.INDICATORS[1],Indicator.INDICATORS[2],Indicator.INDICATORS[3],Indicator.INDICATORS[11]]}
    def __init__(self, df:pd.Series, strat:STRATS, amount:int = 200, interval:pd.Timedelta=pd.Timedelta(days=1),minSum:float=0.1, maxSum:float=0.8) -> None:
        self.interval = interval
        self.strat = strat
        self.reloadDf(df)
        self.amount = amount
        self.coin = 0
        self.fee = 0
        self.stable = amount
        self.minSum = minSum
        self.maxSum = maxSum
        self.maxOrderBuy = 7
        self.canSell = False
        self.canBuy = True
        # timestamp: transaction
        self.activeBuys = {}
        # Order
        
        # ?  dict{str:[Order]}
        self.orderWaitting = {"sell":[],"buy":[]}
    


        pass
    def graph(self) -> None:
        pass
    def graphWallet(self) -> None:
        pass
    def graphOrder(self) -> None:
        pass
    def graphSell(self) -> None:
        pass
    def graphBuy(self) -> None:
        pass
    def _graphCondition(self, condition) -> None:
        pass
    def buy(self,date, amountStable, order=None)->bool:
        if(self.stable >= amountStable and amountStable > 10):
            fee = 0.007 *amountStable
            self.fee += fee
            coinInTransaction =(amountStable/self.df['close'][date]) - 0.007 *(amountStable/self.df['close'][date])
            self.stable -= amountStable
            self.coin += coinInTransaction
            if(order==None):
                order = Order()
            order.open = date
            order.status = "buy"
            order.amount = coinInTransaction
            self.activeBuys[date] = order
            print(date,"REAL BUY $ =",self.stable,"btc :",self.coin, "coin in transaction :",coinInTransaction )
            try:
                self.orderWaitting['buy'].index(order)
                self.orderWaitting['buy'].remove(order)
            except ValueError:
                print("Cet élément n'existe pas")
        else:
            for activeBuy in self.activeBuys.values():
                print(activeBuy)
            print("ACHAT IMPOSSIBLE ______________", amountStable)
    def sell(self,date, amountCoin, order:Order):
        if(self.coin >= amountCoin and amountCoin*self.df['close'][date] > 10):
            fee = 0.007 *(amountCoin*self.df['close'][date])
            self.fee += fee
            self.coin -= amountCoin
            self.stable += (amountCoin*self.df['close'][date]) - fee
            print(date,"REAL SELL $ =",self.stable,"btc :",self.coin, " renta :",  (amountCoin*self.df['close'][date])/(amountCoin*self.df['close'][order.open])*100 -100, "%")
            del self.activeBuys[order.open]
            order.close=date
            order.status = "sell"
            try:
                self.orderWaitting['sell'].index(order)
                self.orderWaitting['sell'].remove(order)
            except ValueError:
                print("Cet élément n'existe pas")
            return order
        else:
            print("VENTE IMPOSSIBLE ______________", amountCoin*self.df['close'][date], '=', amountCoin, date)
            return None
            
            
    # return None
    # Ajoute direct l'achat a activeBuys
    # achet direct
    def tryBuy(self, index) -> None:
        lastIndex = self.generateIndex(index, -1)
        match self.strat:
            case "sma":
                if(len(self.activeBuys) + len(self.orderWaitting["buy"])< self.maxOrderBuy):
                    self.generateIndex(index, -1)

                    if(self.indicators['sma'].df['sma200'][index] > self.indicators['sma'].df['sma600'][index] and self.indicators['sma'].df['sma200'][lastIndex] < self.indicators['sma'].df['sma600'][lastIndex] ):
                        self.buy(index, self.stable)
                    #  peut faite de nouveau order Waitting
                else:
                    print("CAN EX ORDER")
                    # ! ne peut pas faire de nouveau waitting order
                pass
            case "The Filter":
                if(len(self.activeBuys) + len(self.orderWaitting["buy"])< self.maxOrderBuy):

                    if(self.indicators['sma'].df['sma200'][index] > self.indicators['sma'].df['sma600'][index] and self.indicators['sma'].df['sma200'][lastIndex] < self.indicators['sma'].df['sma600'][lastIndex] ):
                        if self.indicators['bollinger_bands'].df['bol_gap'][index] > 10 :
                            self.buy(index, self.stable)
                            print("achat a BON")
                        else:
                            if self.indicators['ema'].df['ema1200'][index] < self.indicators['sma'].df['sma600'][index]:
                                print("achat a Refléchis")
                                self.buy(index, self.stable)
                            else:
                                print("achat repporté")
                                self.orderWaitting['buy'].append(Order(status="not-buy"))

                    #  peut faite de nouveau order Waitting
                if len(self.orderWaitting["buy"])>0:
                    if self.indicators['sma'].df['sma200'][index] > self.indicators['sma'].df['sma600'][index]:
                        if self.indicators['bollinger_bands'].df['bol_gap'][index] > 10 and  self.indicators['ema'].df['ema1200'][index] < self.indicators['sma'].df['sma600'][index]:
                            print("achat odre")
                            self.buy(index, self.stable)
                            self.orderWaitting['buy'] = []
                            
                    else :
                        print("suppression ordre")
                        self.orderWaitting['buy'] = []
            case "The Filter2":
                if(len(self.activeBuys) + len(self.orderWaitting["buy"])< self.maxOrderBuy):

                    if(self.indicators['sma'].df['sma200'][index] > self.indicators['sma'].df['sma600'][index] and self.indicators['sma'].df['sma200'][lastIndex] < self.indicators['sma'].df['sma600'][lastIndex] ):
                        if self.indicators['bollinger_bands'].df['bol_gap'][index] > 10 :
                            self.buy(index, self.stable)
                            print("achat a BON")
                        else:
                            if self.indicators['ema'].df['ema1200'][index] < self.indicators['sma'].df['sma600'][index]:
                                print("achat a Refléchis")
                                self.buy(index, self.stable)
                            else:
                                print("achat repporté")
                                self.orderWaitting['buy'].append(Order(status="not-buy"))

                    #  peut faite de nouveau order Waitting
                if len(self.orderWaitting["buy"])>0:
                    if self.indicators['sma'].df['sma200'][index] > self.indicators['sma'].df['sma600'][index]:
                        if self.indicators['bollinger_bands'].df['bol_gap'][index] > 10 and  self.indicators['ema'].df['ema1200'][index] < self.indicators['sma'].df['sma600'][index]:
                            print("achat odre")
                            self.buy(index, self.stable)
                            self.orderWaitting['buy'] = []
                            
                    else :
                        print("suppression ordre")
                        self.orderWaitting['buy'] = []
            case "new":
                if(self.indicators['sma'].df['sma200'][index] < self.indicators['sma'].df['sma600'][index] and self.indicators['sma'].df['sma200'][lastIndex] > self.indicators['sma'].df['sma600'][lastIndex] ):
                    self.orderWaitting["buy"] = []
                    print("del waitting buy")
                if(self.indicators['sma'].df['sma200'][index] > self.indicators['sma'].df['sma600'][index] and self.indicators['sma'].df['sma200'][lastIndex] < self.indicators['sma'].df['sma600'][lastIndex] ):
                    self.orderWaitting['buy'].append(Order(status="not-buy"))
                    print("create order buy")
                for order in self.orderWaitting['buy']:
                    if self.indicators['bollinger_bands'].df['bol_gap'][index] > 10 and self.indicators['rsi'].df['rsi'][index] < 70:
                        print("buy")
                        self.buy(index, self.stable, order)
                    
                
            case "new2":
                if(self.indicators['sma'].df['sma200'][index] < self.indicators['sma'].df['sma600'][index] and self.indicators['sma'].df['sma200'][lastIndex] > self.indicators['sma'].df['sma600'][lastIndex] ):
                    print("del waitting sell")
                    self.orderWaitting["buy"] = []
                if(self.indicators['sma'].df['sma200'][index] > self.indicators['sma'].df['sma600'][index] and self.indicators['sma'].df['sma200'][lastIndex] < self.indicators['sma'].df['sma600'][lastIndex] ):
                    self.orderWaitting['buy'].append(Order(status="not-buy"))
                    print("create buy order")
                for order in self.orderWaitting['buy']:
                    if  self.indicators['rsi'].df['rsi'][index] < 70:
                        if self.indicators['ema'].df['ema1200'][index] < self.indicators['sma'].df['sma600'][index]:
                            self.buy(index, self.stable, order)
                            print("buy long therme")
                        else:
                            if self.indicators['bollinger_bands'].df['bol_gap'][index] > 10:
                                print("buy bool")
                                self.buy(index, self.stable, order)
            case "new3":
                if(self.indicators['sma'].df['sma200'][index] < self.indicators['sma'].df['sma600'][index] and self.indicators['sma'].df['sma200'][lastIndex] > self.indicators['sma'].df['sma600'][lastIndex] ):
                    print("del waitting sell")
                    self.orderWaitting["buy"] = []
                if(self.indicators['sma'].df['sma200'][index] > self.indicators['sma'].df['sma600'][index] and self.indicators['sma'].df['sma200'][lastIndex] < self.indicators['sma'].df['sma600'][lastIndex] ):
                    self.orderWaitting['buy'].append(Order(status="not-buy"))
                    print("create buy order")
                for order in self.orderWaitting['buy']:
                    if(order.status == "super_trend"):
                        if self.indicators['super_trend'].df['super_trend_direction'][index]:
                            self.buy(index, self.stable, order)
                    elif  self.indicators['rsi'].df['rsi'][index] < 70:
                        if self.indicators['ema'].df['ema1200'][index] < self.indicators['sma'].df['sma600'][index]:
                            order.status == "super_trend"
                            print("buy long therme")
                        else:
                            if self.indicators['bollinger_bands'].df['bol_gap'][index] > 10:
                                order.status == "super_trend"
                                print("buy bool")
                
                

                    # ! ne peut pas faire de nouveau waitting order
    # Retourn timestamp de l'ActivBuy a vendre
    # vent direct
    def trySell(self, index):
        finalOrder = None
        match self.strat:
            case "sma":
                lastIndex = self.generateIndex(index, -1)
                
                if(self.indicators['sma'].df['sma200'][index] < self.indicators['sma'].df['sma600'][index] and self.indicators['sma'].df['sma200'][lastIndex] > self.indicators['sma'].df['sma600'][lastIndex] ):
                    activeBuys = self.activeBuys.copy()
                    for key in activeBuys.keys():
                        finalOrder = self.sell(index, self.coin,self.activeBuys[key])
            case "The Filter":
                for order in self.activeBuys.copy().values():
                    # ? différencier les négades pos?
                    # if order.amount*self.df['close'][order.open] < order.amount*self.df['close'][index]:
                        # POSITIF TRADE
                        lastIndex = self.generateIndex(index, -1)

                        if self.indicators['sma'].df['sma200'][index] < self.indicators['sma'].df['sma600'][index]:
                            if self.indicators['bollinger_bands'].df['bol_gap'][index] > 10 :
                                finalOrder = self.sell(index, order.amount, order)
                                print("Vente a BON")
                                # print(self.indicators['bollinger_bands'].df['bol_gap'][index])
                                # print( self.indicators['sma'].df['sma200'][index], self.indicators['sma'].df['sma600'][index])
                                # print(order.amount*self.df['close'][order.open], order.amount*self.df['close'][index])336
                                
                            else:
                                if self.indicators['ema'].df['ema1200'][index] > self.indicators['sma'].df['sma600'][index]:
                                    print("Vente a Refléchis")
                                    # print(self.indicators['ema'].df['ema1200'][index] ,self.indicators['sma'].df['sma600'][index])
                                    # print(order.amount*self.df['close'][order.open], order.amount*self.df['close'][index])
                                    finalOrder = self.sell(index, order.amount, order)
                                # else:
                                #     print("Vente repporté")
                                #     print(order.amount*self.df['close'][order.open], order.amount*self.df['close'][index])
                                #     # self.orderWaitting['sell'].append(order)
                    # else:
                    #     if(self.Indicator['ema'].df['ema1200'][index] < self.indicators['sma'].df['sma600'][index]):
                    #             # ? sma haussier?
                    #         if self.indicators['sma'].df['sma200'][index] > self.indicators['sma'].df['sma600'][index]:
                    #             if self.Indicator['bollinger_bands'].df['bol_gap'][index] > 10 :
                    #                 finalOrder = self.sell(index, order.amount)
                    #     else:
                    #         # ? vendre
                        # NEGATIF TRADE
            case "The Filter2":
                for order in self.activeBuys.copy().values():
                    # ? différencier les négades pos?
                    if order.amount*self.df['close'][order.open] < order.amount*self.df['close'][index]:
                        # POSITIF TRADE
                        lastIndex = self.generateIndex(index, -1)

                        if self.indicators['sma'].df['sma200'][index] < self.indicators['sma'].df['sma600'][index]:
                            if self.indicators['bollinger_bands'].df['bol_gap'][index] > 10 :
                                finalOrder = self.sell(index, order.amount, order)
                                print("Vente a BON")
                                # print(self.indicators['bollinger_bands'].df['bol_gap'][index])
                                # print( self.indicators['sma'].df['sma200'][index], self.indicators['sma'].df['sma600'][index])
                                # print(order.amount*self.df['close'][order.open], order.amount*self.df['close'][index])336
                                
                            else:
                                if self.indicators['ema'].df['ema1200'][index] > self.indicators['sma'].df['sma600'][index]:
                                    print("Vente a Refléchis")
                                    # print(self.indicators['ema'].df['ema1200'][index] ,self.indicators['sma'].df['sma600'][index])
                                    # print(order.amount*self.df['close'][order.open], order.amount*self.df['close'][index])
                                    finalOrder = self.sell(index, order.amount, order)
                                # else:
                                #     print("Vente repporté")
                                #     print(order.amount*self.df['close'][order.open], order.amount*self.df['close'][index])
                                #     # self.orderWaitting['sell'].append(order)
                    else:
                        if(self.indicators['ema'].df['ema1200'][index] > self.indicators['sma'].df['sma600'][index]):
                            # ? sma haussier?
                            if self.indicators['sma'].df['sma200'][index] < self.indicators['sma'].df['sma600'][index]:
                                finalOrder = self.sell(index, order.amount, order)
                    #     else:
                    #         # ? vendre
                        # NEGATIF TRADE
                        #  peut faite de nouveau order Waitting
            case "new":
                lastIndex = self.generateIndex(index, -1)
                for order in self.activeBuys.copy().values():
                    if(self.indicators['sma'].df['sma200'][index] > self.indicators['sma'].df['sma600'][index] and self.indicators['sma'].df['sma200'][lastIndex] < self.indicators['sma'].df['sma600'][lastIndex] ):
                        print("del order sell")
                        self.orderWaitting["sell"] = []
                    if(self.indicators['sma'].df['sma200'][index] < self.indicators['sma'].df['sma600'][index] and self.indicators['sma'].df['sma200'][lastIndex] > self.indicators['sma'].df['sma600'][lastIndex] ):
                        print("create sell order")
                        order.status = "not-sell"
                        self.orderWaitting['sell'].append(order)
                for order in self.orderWaitting['sell']:
                    if self.indicators['bollinger_bands'].df['bol_gap'][index] > 10 and self.indicators['rsi'].df['rsi'][index] > 30:
                        print("sell")
                        finalOrder = self.sell(index, order.amount, order)
                    
                
            case "new2":
                lastIndex = self.generateIndex(index, -1)
                for order in self.activeBuys.copy().values():
                    if(self.indicators['sma'].df['sma200'][index] > self.indicators['sma'].df['sma600'][index] and self.indicators['sma'].df['sma200'][lastIndex] < self.indicators['sma'].df['sma600'][lastIndex] ):
                        print("del sell order")
                        self.orderWaitting["sell"] = []
                    if(self.indicators['sma'].df['sma200'][index] < self.indicators['sma'].df['sma600'][index] and self.indicators['sma'].df['sma200'][lastIndex] > self.indicators['sma'].df['sma600'][lastIndex] ):
                        order.status = "not-sell"
                        self.orderWaitting['sell'].append(order)
                        print("create sell order")
                for order in self.orderWaitting['sell']:
                    if self.indicators['rsi'].df['rsi'][index] > 30:
                        if self.indicators['bollinger_bands'].df['bol_gap'][index] > 10:
                            print("sell bool")
                            finalOrder = self.sell(index, order.amount, order)
                        elif self.indicators['ema'].df['ema1200'][index] > self.indicators['sma'].df['sma600'][index]:
                            print("sell longtherme")
                            finalOrder = self.sell(index, order.amount, order)     
            case "new3":
                lastIndex = self.generateIndex(index, -1)
                for order in self.activeBuys.copy().values():
                    if(self.indicators['sma'].df['sma200'][index] > self.indicators['sma'].df['sma600'][index] and self.indicators['sma'].df['sma200'][lastIndex] < self.indicators['sma'].df['sma600'][lastIndex] ):
                        print("del sell order")
                        self.orderWaitting["sell"] = []
                    if(self.indicators['sma'].df['sma200'][index] < self.indicators['sma'].df['sma600'][index] and self.indicators['sma'].df['sma200'][lastIndex] > self.indicators['sma'].df['sma600'][lastIndex] ):
                        order.status = "not-sell"
                        self.orderWaitting['sell'].append(order)
                        print("create sell order")
                for order in self.orderWaitting['sell']:
                    if self.indicators['rsi'].df['rsi'][index] > 30:
                        if self.indicators['bollinger_bands'].df['bol_gap'][index] > 10:
                            print("sell bool")
                            finalOrder = self.sell(index, order.amount, order)
                        elif self.indicators['ema'].df['ema1200'][index] > self.indicators['sma'].df['sma600'][index]:
                            print("sell longtherme")
                            finalOrder = self.sell(index, order.amount, order)

        return finalOrder
    # Gere les conflit entre achat et vent
    # Se base sur df.lastIndexValid et 
    def task(self, actualIndex=None)-> Order:
        finalOrder = None
        if(actualIndex==None):
            print("FOR TO DAY")
            actualIndex = self.df.last_valid_index()

        if(len(self.activeBuys) > 0):
            finalOrder = self.trySell(actualIndex)
        if(len(self.activeBuys) < self.maxOrderBuy):
            self.tryBuy(actualIndex)
        return self.stable, self.coin,finalOrder
    def reloadDf(self, df):
        self.indicators = {indicName : Indicator(df, indicName) for indicName in self.STRATS_INDICATORS[self.strat]}
        self.df = df
    
    def generateIndex(self,index:pd.Timestamp, step:int):
                newIndex = index + self.interval * step
                return self.df.index[self.df.index.get_loc(newIndex, method='nearest')]

        