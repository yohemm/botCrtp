import ta
import requests
import numpy as np
import pandas as pd
class Indicator():
    TYPES = ['trend', 'volatility']
    INDICATORS = ['sma', 'bollinger_bands' ,'rsi', 'ema', 'macd','fear', 'volume_anomali', 'ichimoku', 'stochastic_rsi', 'aroon', 'awesome_oscilllator', "super_trend"]
    INDICATORS_TYPE =  {'rsi':TYPES[0], 'bolliger_bands':TYPES[1],'sma':TYPES[0]}

    def __str__(self) -> str:
        return self.name + str(self.df.columns)

    
    def __init__(self, df: pd.DataFrame, name:INDICATORS) -> None:
        df = df.copy()
        self.name = name
        # self.type = Indicator.INDICATORS_TYPE[name]
        match name:
            case "rsi":
                df['rsi'] = ta.momentum.RSIIndicator(close=df['close'], window=14).rsi()
            case "stochastic_rsi":
                df['stoch_rsi'] = ta.momentum.stochrsi(close=df['close'], window=14)
                df['stochastic'] = ta.momentum.stoch(high=df['high'],low=df['low'],close=df['close'], window=14,smooth_window=3)
                df['stoch_signal'] =ta.momentum.stoch_signal(high =df['high'],low=df['low'],close=df['close'], window=14, smooth_window=3)
            case "sma":
                df["sma200"] = ta.trend.sma_indicator(df['close'], 200)
                df["sma600"] = ta.trend.sma_indicator(df['close'], 600)
            case "bollinger_bands":
                df["bol_high"] = ta.volatility.bollinger_hband(df['close'], window=20, window_dev=2)
                df["bol_low"] = ta.volatility.bollinger_lband(df['close'], window=20, window_dev=2)
                df["bol_medium"] = ta.volatility.bollinger_mavg(df['close'], window=20)
                df["bol_gap"] = ta.volatility.bollinger_wband(df['close'], window=20, window_dev=2)
                # Return binaire 0 ou 1 
                df["bol_higher"] = ta.volatility.bollinger_hband_indicator(df['close'], window=20, window_dev=2)
                df["bol_lower"] = ta.volatility.bollinger_lband_indicator(df['close'], window=20, window_dev=2)
            case "awesome_oscilllator":
                df['awesome_oscilllator'] = ta.momentum.awesome_oscillator(high=df['high'], low=df['low'], window1=5, window2=34)
            case "aroon":
                df['aroon_up'] = ta.trend.aroon_up(close=df['close'], window=25)
                df['aroon_dow'] = ta.trend.aroon_down(close=df['close'], window=25)
            case "volume_anomali":
                df["volume_anomaly"] = self.volume_anomalu(volume_window=10)
            case "ema":
                df['ema7']=ta.trend.ema_indicator(close=df['close'], window=7)
                df['ema30']=ta.trend.ema_indicator(close=df['close'], window=30)
                df['ema50']=ta.trend.ema_indicator(close=df['close'], window=50)
                df['ema100']=ta.trend.ema_indicator(close=df['close'], window=100)
                df['ema150']=ta.trend.ema_indicator(close=df['close'], window=150)
                df['ema200']=ta.trend.ema_indicator(close=df['close'], window=200)
                df['ema900']=ta.trend.ema_indicator(close=df['close'], window=900)
                df['ema1200']=ta.trend.ema_indicator(close=df['close'], window=1200)
            case "ichimoku":
                df['kijun'] = ta.trend.ichimoku_base_line(df['high'], df['low'])
                df['tenkan'] = ta.trend.ichimoku_conversion_line(df['high'], df['low'])
                df['ssa'] = ta.trend.ichimoku_a(df['high'], df['low'])
                df['ssb'] = ta.trend.ichimoku_b(df['high'], df['low'])
                df['ssa25'] = ta.trend.ichimoku_a(df['high'], df['low']).shift(25)
                df['ssb25'] = ta.trend.ichimoku_b(df['high'], df['low']).shift(25)
                df['ssa52'] = ta.trend.ichimoku_a(df['high'], df['low']).shift(50)
                df['ssb52'] = ta.trend.ichimoku_b(df['high'], df['low']).shift(50)
                df['close25'] = df['close'].shift(25)
                df['close1'] = df['close'].shift(1)
            case "macd":
                macd = ta.trend.MACD(close=df['close'], window_fast=12, window_slow=26, window_sign=9)
                df['macd'] = macd.macd()
                df['macd_signal'] = macd.macd_signal()
                df['macd_histo'] = macd.macd_diff() #Histogramme MACD
            case "fear":
                df['fear'] = self.fear_and_greed()
            case "super_trend":
                st_atr_window = 20
                st_atr_multiplier = 3

                super_trend = SuperTrend(df['high'], df['low'], df['close'], st_atr_window, st_atr_multiplier)
                df['super_trend_direction'] = super_trend.super_trend_direction() # True if bullish, False if bearish
                df['super_trend_upper'] = super_trend.super_trend_upper()
                df['super_trend_lower'] = super_trend.super_trend_lower()
        self.df = df
        del df['close']
        del df['open']
        del df['high']
        del df['low']

    def volume_anomalu(self, volume_window=10):
        dfInd = self.df.copy()
        dfInd["VolAnomaly"] = 0
        dfInd["PreviousClose"] = dfInd["close"].shift(1)
        dfInd['MeanVolume'] = dfInd['volume'].rolling(volume_window).mean()
        dfInd['MaxVolume'] = dfInd['volume'].rolling(volume_window).max()
        dfInd.loc[dfInd['volume'] > 1.5 * dfInd['MeanVolume'], "VolAnomaly"] = 1
        dfInd.loc[dfInd['volume'] > 2 * dfInd['MeanVolume'], "VolAnomaly"] = 2
        dfInd.loc[dfInd['volume'] >= dfInd['MaxVolume'], "VolAnomaly"] = 3
        dfInd.loc[dfInd['PreviousClose'] > dfInd['close'],
                "VolAnomaly"] = (-1) * dfInd["VolAnomaly"]
        return dfInd["VolAnomaly"]

    def fear_and_greed(self):
        response = requests.get("https://api.alternative.me/fng/?limit=0&format=json")
        dataResponse = response.json()['data']
        fear = pd.DataFrame(dataResponse, columns = ['timestamp', 'value'])

        fear = fear.set_index(fear['timestamp'])
        fear.index = pd.to_datetime(fear.index, unit='s')
        del fear['timestamp']
        df = pd.DataFrame(df['close'], columns = ['close'])
        df['fearResult'] = fear['value']
        df['FEAR'] = df['fearResult'].ffill()
        df['FEAR'] = df.FEAR.astype(float)
        return pd.Series(df['FEAR'], name="FEAR")

    def graph(self) -> None:
        pass



# Supertrend
# Classe de définition
class SuperTrend():
    def __init__(
        self,
        high,
        low,
        close,
        atr_window=10,
        atr_multi=3
    ):
        self.high = high
        self.low = low
        self.close = close
        self.atr_window = atr_window
        self.atr_multi = atr_multi
        self._run()
        
    def _run(self):
        # calculate ATR
        price_diffs = [self.high - self.low, 
                    self.high - self.close.shift(), 
                    self.close.shift() - self.low]
        true_range = pd.concat(price_diffs, axis=1)
        true_range = true_range.abs().max(axis=1)
        # default ATR calculation in supertrend indicator
        atr = true_range.ewm(alpha=1/self.atr_window,min_periods=self.atr_window).mean() 
        # atr = ta.volatility.average_true_range(high, low, close, atr_period)
        # df['atr'] = df['tr'].rolling(atr_period).mean()
        
        # HL2 is simply the average of high and low prices
        hl2 = (self.high + self.low) / 2
        # upperband and lowerband calculation
        # notice that final bands are set to be equal to the respective bands
        final_upperband = upperband = hl2 + (self.atr_multi * atr)
        final_lowerband = lowerband = hl2 - (self.atr_multi * atr)
        
        # initialize Supertrend column to True
        supertrend = [True] * len(self.close)
        
        for i in range(1, len(self.close)):
            curr, prev = i, i-1
            
            # if current close price crosses above upperband
            if self.close[curr] > final_upperband[prev]:
                supertrend[curr] = True
            # if current close price crosses below lowerband
            elif self.close[curr] < final_lowerband[prev]:
                supertrend[curr] = False
            # else, the trend continues
            else:
                supertrend[curr] = supertrend[prev]
                
                # adjustment to the final bands
                if supertrend[curr] == True and final_lowerband[curr] < final_lowerband[prev]:
                    final_lowerband[curr] = final_lowerband[prev]
                if supertrend[curr] == False and final_upperband[curr] > final_upperband[prev]:
                    final_upperband[curr] = final_upperband[prev]

            # to remove bands according to the trend direction
            if supertrend[curr] == True:
                final_upperband[curr] = np.nan
            else:
                final_lowerband[curr] = np.nan
                
        self.st = pd.DataFrame({
            'Supertrend': supertrend,
            'Final Lowerband': final_lowerband,
            'Final Upperband': final_upperband
        })
        
    def super_trend_upper(self):
        return self.st['Final Upperband']
        
    def super_trend_lower(self):
        return self.st['Final Lowerband']
        
    def super_trend_direction(self):
        return self.st['Supertrend']