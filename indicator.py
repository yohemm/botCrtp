from ta.volatility import BollingerBands
from ta.trend import sma_indicator, macd
from ta.momentum import rsi
class Indicator():
    INDACTORS = ['bollinger_bands', 'sma200/600', 'rsi', 'macd']
    def __init__(self, indicator:str) -> None:
        self.indicator = indicator
        pass
    def __str__(self) -> str:
        return self.indicator
    def addIndicator(self, df) -> list:
        match self.indicator:
            case 'bollinger_bands':
                indicatorBb = BollingerBands(df['close'], 20, 2)
                df['bolbandh'] = indicatorBb.bollinger_hband()
                df['bolbandl'] = indicatorBb.bollinger_lband()
            case 'sma200/600':
                df['SMA200'] = sma_indicator(df['close'], 200)
                df['SMA600'] = sma_indicator(df['close'], 600)
            case 'rsi':
                df['RSI'] = rsi(df['close'], 14)
            case 'macd':
                df['MACD'] = macd(df['close'], 26, 12)
        return df
    def signal(self, df, closeIndex, lastIndex) -> int:
        match self.indicator:
            case "bollinger_bands":
                res = 0
                boolPerc = 1 - df['bolbandl'][closeIndex]/df['bolbandh'][closeIndex]
                if(boolPerc> 0.12):
                    res = 1
                return res
            case "sma200/600":
                res = 0
                if df['SMA200'][closeIndex] > df['SMA600'][closeIndex]:
                    res = 1
                if df['SMA200'][closeIndex] < df['SMA600'][closeIndex]:
                    res = -1
                return res
            case "rsi":
                res = 0
                if df['RSI'][closeIndex] < 30:
                    res = 1
                elif df['RSI'][closeIndex] < 40:
                    res = (df['RSI'][closeIndex] - 30)/10
                if df['RSI'][closeIndex] > 70:
                    res = -1
                elif df['RSI'][closeIndex] > 60:
                    res = -((df['RSI'][closeIndex] - 60)/10)
                return res
            case "macd":
                res = 0
                if df['MACD'][closeIndex] > 0 and df['MACD'][lastIndex] < 0:
                    res = 1
                if df['MACD'][closeIndex] < 0 and df['MACD'][lastIndex] > 0:
                    res = -1
                return res
        return 0
