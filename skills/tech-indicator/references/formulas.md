# 技术指标纯 Python 计算公式

## 通用约定
- close: 收盘价列表（按时间正序）
- high: 最高价列表
- low: 最低价列表
- vol: 成交量列表
- 所有计算结果保留 2 位小数

## MA（简单移动平均）
```
MA(close, N) = sum(close[-N:]) / N
```

## EMA（指数移动平均）
```
EMA[0] = close[0]
EMA[i] = close[i] * alpha + EMA[i-1] * (1 - alpha)
alpha = 2 / (N + 1)
```

## MACD
```
EMA12 = EMA(close, 12)
EMA26 = EMA(close, 26)
DIF = EMA12 - EMA26
DEA = EMA(DIF, 9)
MACD柱 = 2 * (DIF - DEA)
```

## RSI（相对强弱指标）
```
gain = max(close[i] - close[i-1], 0)
loss = max(close[i-1] - close[i], 0)
avg_gain = MA(gain, N)
avg_loss = MA(loss, N)
RS = avg_gain / avg_loss
RSI = 100 - 100 / (1 + RS)
```

## KDJ
```
RSV = (close - low_N) / (high_N - low_N) * 100
K = EMA(RSV, 3)    # 或 SMA(K, 3, 1)
D = EMA(K, 3)
J = 3*K - 2*D
```

## BOLL（布林带）
```
MID = MA(close, 20)
STD = sqrt(sum((close[i] - MID)^2) / 20)
UP = MID + 2*STD
DOWN = MID - 2*STD
```
