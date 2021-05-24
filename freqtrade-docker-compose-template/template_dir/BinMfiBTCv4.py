# --- Do not remove these libs ---
from datetime import datetime
from datetime import timedelta

import numpy as np
# --------------------------------
import talib.abstract as ta
from pandas import DataFrame

from freqtrade.persistence import Trade
from freqtrade.strategy import CategoricalParameter
from freqtrade.strategy import DecimalParameter
from freqtrade.strategy import IntParameter
from freqtrade.strategy import merge_informative_pair
from freqtrade.strategy.interface import IStrategy


#   --------------------------------------------------------------------------------
#   Author: rextea      2021/05/21     Version: 4.0
#   --------------------------------------------------------------------------------
#   Strategy based on the legendary BinHV45:
#   https://github.com/freqtrade/freqtrade-strategies
#
#
#   Posted on Freqtrade discord channel: https://discord.gg/Xr4wUYc6

def EWO(dataframe, sma_length=5, sma2_length=35):
    df = dataframe.copy()
    sma1 = ta.SMA(df, timeperiod=sma_length)
    sma2 = ta.SMA(df, timeperiod=sma2_length)
    smadif = (sma1 - sma2) / df['close'] * 100
    return smadif


def bollinger_bands(stock_price, window_size, num_of_std):
    rolling_mean = stock_price.rolling(window=window_size).mean()
    rolling_std = stock_price.rolling(window=window_size).std()
    lower_band = rolling_mean - (rolling_std * num_of_std)
    return np.nan_to_num(rolling_mean), np.nan_to_num(lower_band)


class BinMfiBTCv4(IStrategy):
    timeframe = '5m'
    btc_timeframe = '5m'
    btc_pair = 'BTC/USDT'

    stoploss = -0.095
    use_custom_stoploss = True

    minimal_roi = {
        "0": 0.08,
        "1": 0.015,
        "10": 0.02,
        "90": 0.005
    }

    use_sell_signal = False

    trailing_stop = True
    trailing_stop_positive = 0.0075
    trailing_stop_positive_offset = 0.02
    trailing_only_offset_is_reached = True

    process_only_new_candles = True
    startup_candle_count: int = 15

    # Strict mode buy params:
    strict_bbdelta_close = DecimalParameter(0.0, 0.045, default=0.03344, space='buy', optimize=False, load=True)
    strict_closedelta_close = DecimalParameter(-0.015, 0.045, default=0.00681, space='buy', optimize=False, load=True)
    strict_tail_bbdelta = DecimalParameter(0.0, 2.0, default=1.73588, space='buy', optimize=False, load=True)
    strict_mfi_limit = IntParameter(-15, 70, default=25, space='buy', optimize=False, load=True)

    # Loose mode buy params:
    loose_bbdelta_close = DecimalParameter(0.0, 0.045, default=0.03344, space='buy', optimize=False, load=True)
    loose_closedelta_close = DecimalParameter(-0.015, 0.045, default=0.00681, space='buy', optimize=False, load=True)
    loose_tail_bbdelta = DecimalParameter(0.0, 2.0, default=1.73588, space='buy', optimize=False, load=True)
    loose_mfi_limit = IntParameter(-15, 100, default=25, space='buy', optimize=False, load=True)

    ewo_low = DecimalParameter(-20.0, -8.0, default=-12.0, space='buy', optimize=False)
    ewo_high = DecimalParameter(2.0, 12.0, default=6.0, space='buy', optimize=False)
    rsi_buy = IntParameter(30, 70, default=55, space='buy', optimize=False, load=True)

    btc_bail_roc = DecimalParameter(-20.0, -2.0, default=-5.0, space='sell', optimize=False, load=True)
    bail_after_period = CategoricalParameter([60, 120, 240, 280, 340, 400, 480, 600, 800, 1200], default=480,
                                             space='sell', optimize=True)
    bail_ng_profit = CategoricalParameter([0, -0.01, -0.02, -0.03, -0.05, -0.06], default=-0.03,
                                          space='sell', optimize=True)
    bail_ng_profit_2 = CategoricalParameter([-0.05, -0.06, -0.07, -0.08, -0.09], default=-0.07,
                                            space='sell', optimize=True)
    bail_ewo = CategoricalParameter([0, -0.5, -1, -1.5, -2, -2.5], default=-1,
                                    space='sell', optimize=True)
    bail_ewo_2 = CategoricalParameter([0, -0.5, -1, -1.5, -2, -2.5], default=0,
                                      space='sell', optimize=True)

    ignore_roi_ewo = DecimalParameter(0.0, 10.0, default=3.0, space='sell', optimize=True)
    ignore_roi_rsi = IntParameter(30, 90, default=50, space='sell', optimize=True)

    buy_params = {
        'loose_bbdelta_close': 0.03,
        'loose_closedelta_close': 0.019,
        'loose_mfi_limit': 43,
        'loose_tail_bbdelta': 1.739,
        'strict_bbdelta_close': 0.042,
        'strict_closedelta_close': 0.008,
        'strict_mfi_limit': 59,
        'strict_tail_bbdelta': 0.788
    }

    sell_params = {
        "bail_after_period": 480,
        "bail_ewo": -2,
        "bail_ewo_2": -2.5,
        "bail_ng_profit": -0.05,
        "bail_ng_profit_2": -0.07,
        "ignore_roi_ewo": 3.636,
        "ignore_roi_rsi": 31,
        "btc_bail_roc": -5.0,  # value loaded from strategy
    }

    def informative_pairs(self):
        return [(self.btc_pair, self.btc_timeframe)]

    def custom_stoploss(self, pair: str, trade: 'Trade', current_time: datetime,
                        current_rate: float, current_profit: float, **kwargs) -> float:
        dataframe, _ = self.dp.get_analyzed_dataframe(pair, self.timeframe)
        current_candle = dataframe.iloc[-1].squeeze()

        if current_candle['btc-roc'] < self.btc_bail_roc.value:
            return 0.01

        if current_profit < 0:
            if current_profit > self.bail_ng_profit.value:
                if (current_time - timedelta(minutes=int(self.bail_after_period.value)) > trade.open_date_utc) & (
                        current_candle['EWO'] < self.bail_ewo.value):
                    return 0.01
            elif current_profit < self.bail_ng_profit_2.value:
                if current_candle['EWO'] < self.bail_ewo_2.value:
                    return 0.01
        return 0.99

    def populate_btc_indicators(self, dataframe):
        informative = self.dp.get_pair_dataframe(self.btc_pair, self.btc_timeframe)
        informative['sma25'] = ta.SMA(informative, timeperiod=25)
        informative['sma100'] = ta.SMA(informative, timeperiod=100)
        informative['btc_sma_delta'] = (((informative['sma25'] - informative['sma100']) / informative['sma25']) * 100)
        informative['bull_100'] = informative['sma100'].gt(informative['sma100'].shift(10))
        informative['bear_100'] = informative['sma100'].lt(informative['sma100'].shift(10))
        informative['btc-roc'] = ta.ROC(informative, timeperiod=6)

        dataframe = merge_informative_pair(dataframe, informative, self.timeframe, self.btc_timeframe, ffill=True)
        skip_columns = [(s + "_" + self.btc_timeframe) for s in ['date', 'open', 'high', 'low', 'close', 'volume']]
        dataframe.rename(
            columns=lambda s: s.replace("_{}".format(self.btc_timeframe), "") if (not s in skip_columns) else s,
            inplace=True)
        return dataframe

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe = self.populate_btc_indicators(dataframe.copy())

        dataframe['hl2'] = (dataframe["high"] + dataframe["low"]) / 2
        mid, lower = bollinger_bands(dataframe['hl2'], window_size=16, num_of_std=2)
        dataframe['lower'] = lower
        dataframe['bbdelta'] = (mid - dataframe['lower']).abs()
        dataframe['closedelta'] = (dataframe['close'] - dataframe['close'].shift()).abs()
        dataframe['tail'] = (dataframe['close'] - dataframe['low']).abs()

        dataframe['mfi'] = ta.MFI(dataframe, timeperiod=14)
        dataframe['rsi'] = ta.RSI(dataframe, timeperiod=14)
        dataframe['EWO'] = EWO(dataframe, 5, 35)
        dataframe['3close'] = dataframe['close'].rolling(window=3).mean()
        return dataframe

    def populate_buy_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        # loose params
        bbdelta = self.loose_bbdelta_close.value
        closedelta = self.loose_closedelta_close.value
        tail_bbdelta = self.loose_tail_bbdelta.value
        mfi = self.loose_mfi_limit.value

        # strict params
        strict_bbdelta = self.strict_bbdelta_close.value
        strict_closedelta = self.strict_closedelta_close.value
        strict_tail_bbdelta = self.strict_tail_bbdelta.value
        strict_mfi = self.strict_mfi_limit.value

        dataframe.loc[
            (
                (
                        (dataframe['bull_100']) &
                        (dataframe['mfi'] <= mfi) &
                        (
                                dataframe['lower'].shift().gt(0) &
                                dataframe['bbdelta'].gt(dataframe['close'] * bbdelta) &
                                dataframe['closedelta'].gt(dataframe['close'] * closedelta) &
                                dataframe['tail'].lt(dataframe['bbdelta'] * tail_bbdelta) &
                                dataframe['close'].lt(dataframe['lower'].shift()) &
                                dataframe['close'].le(dataframe['close'].shift())
                        )
                        |
                        (dataframe['bear_100']) &
                        (dataframe['mfi'] <= strict_mfi) &
                        (
                                dataframe['lower'].shift().gt(0) &
                                dataframe['bbdelta'].gt(dataframe['close'] * strict_bbdelta) &
                                dataframe['closedelta'].gt(dataframe['close'] * strict_closedelta) &
                                dataframe['tail'].lt(dataframe['bbdelta'] * strict_tail_bbdelta) &
                                dataframe['close'].lt(dataframe['lower'].shift()) &
                                dataframe['close'].le(dataframe['close'].shift())
                        )
                )
            )
            |
            # Elliot wave trend: buy when it's really low -> usually goes up from here:
            (dataframe['EWO'] < self.ewo_low.value)
            |
            # Buy when Elliot wave trend is up, btc trend is up, and rsi not too high:
            (
                    (dataframe['bull_100']) &
                    (dataframe['EWO'] > self.ewo_high.value) &
                    (dataframe['rsi'] < self.rsi_buy.value)
            )
            ,
            'buy'
        ] = 1

        # Avoid buying when BTC dumping
        dataframe.loc[(dataframe['btc-roc'] < self.btc_bail_roc.value) &
                      dataframe['btc-roc'] < dataframe['btc-roc'].shift(), 'buy'] = 0

        return dataframe

    def populate_sell_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[:, 'sell'] = 0
        return dataframe

    def confirm_trade_exit(self, pair: str, trade: Trade, order_type: str, amount: float,
                           rate: float, time_in_force: str, sell_reason: str, **kwargs) -> bool:
        # Ignore ROI if seems to go up:
        if sell_reason == 'roi':
            dataframe, _ = self.dp.get_analyzed_dataframe(pair, self.timeframe)
            last_candle = dataframe.iloc[-1].squeeze()

            if last_candle['rsi'] > self.ignore_roi_rsi.value:
                return False
            if last_candle['EWO'] > self.ignore_roi_ewo.value:
                return False
            if last_candle['close'] > last_candle['3close']:
                return False

            return True
        return True
