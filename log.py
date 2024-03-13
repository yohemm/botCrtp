class Log():
    def __init__(self, order, price, time) -> None:
        self.order = order
        self.time = time
        if self.order != 0:
            self.price = price
        pass
    def __str__(self) -> str:
        order = "Neutral"
        if(self.order != 0):
            order = "Buy" if self.order >0 else "Sell"
            return order + " : "+str(self.order)+"% | price : "+ str(self.price) + " | at : "+self.time
        return order

    @staticmethod
    def highBuy(logList:list):
        max = None
        for log in logList:
            if(log.order > 0):
                if max == None:
                    max = log
                else:
                    max = log if max.price < log.price else max
        return max

    @staticmethod
    def lowBuy(logList:list):
        min = None
        for log in logList:
            if(log.order > 0):
                if min == None:
                    min = log
                else:
                    min = log if min.price > log.price else min
        return min

    @staticmethod
    def avgBuy(logList:list):
        total = 0
        moy = 0
        for log in logList:
            if(log.order > 0):
                moy += log.price
                total +=1
        return -1 if total <1 else moy/total
    
    
    @staticmethod
    def countBuy(logList:list):
        total = 0
        for log in logList:
            if(log.order > 0):
                total +=1
        return total
        

    @staticmethod
    def highSell(logList:list):
        max = None
        for log in logList:
            if(log.order < 0):
                if max == None:
                    max = log
                else:
                    max = log if max.price < log.price else max
        return max

    @staticmethod
    def lowSell(logList:list):
        min = None
        for log in logList:
            if(log.order < 0):
                if min == None:
                    min = log
                else:
                    min = log if min.price > log.price else min
        return min
    
    @staticmethod
    def avgSell(logList:list):
        total = 0
        moy = 0
        for log in logList:
            if(log.order < 0):
                moy += log.price
                total +=1
        return -1 if total <1 else moy/total
    
    @staticmethod
    def countSell(logList:list):
        total = 0
        for log in logList:
            if(log.order < 0):
                total +=1
        return total