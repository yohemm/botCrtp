import pandas as pd
class Order():
    def __init__(self, openn:pd.Timestamp=None, close:pd.Timestamp=None, amount:float=-1, status:str="initial") -> None:
        self.open = openn
        self.close = close 
        self.status = status
        self.amount = amount
        pass
    def __str__(self) -> str:
        return str(self.close) + ' '+str(self.amount)+self.status 
