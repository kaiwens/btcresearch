
import pandas as pd
import array
import matplotlib.pyplot as plt
import pynance.tech.movave as mav
from numpy import diff

LONG_AVG_TIME = 15
SHORT_AVG_TIME = 7
#DERIVATIVE_THRESHOLD = 10
MACD_THRESHOLD = 0.3 # Between 0 and 1

def main():

    hist = pd.read_csv('Raw2.csv')
    hist.columns = ['Price']
    print(hist.columns)

    exp = mav.ema(hist, span=LONG_AVG_TIME)
    exp2 = mav.ema(hist, span=SHORT_AVG_TIME)
    MACD =  exp2.subtract(exp)
    difMACD = pd.Series.diff(MACD)
    difMACD.columns = ['Deriv']

    maxMACDSwing = max(abs(MACD['EMA']))


    buy = []
    for i in range(1,len(MACD) - 1):
        #if (MACD['EMA'][i] < 0 < MACD['EMA'][i + 1] and (difMACD['Deriv'][i] > DERIVATIVE_THRESHOLD)):
        if (MACD['EMA'][i] > maxMACDSwing * MACD_THRESHOLD):
            buy.append(max(hist['Price']))
        else:
            buy.append(min(hist['Price']))


    sell = []
    for i in range(1,len(MACD) - 1):
        #if (MACD['EMA'][i] > 0 > MACD['EMA'][i + 1] and (difMACD['Deriv'][i] < -DERIVATIVE_THRESHOLD)):
        if (MACD['EMA'][i] < -(maxMACDSwing * MACD_THRESHOLD)):
            sell.append(max(hist['Price']))
        else:
            sell.append(min(hist['Price']))

    print(maxMACDSwing * MACD_THRESHOLD)
    f, ax = plt.subplots(2, sharex=True)
    ax[0].plot(hist)
    ax[0].plot(exp)
    ax[0].plot(exp2,color='purple')
    ax[0].plot(buy,color='green')
    ax[0].plot(sell,color='red')
    ax[1].plot(MACD)
    #ax[2].plot(difMACD)
    plt.grid(True)

    plt.show()



if  __name__ =='__main__':main()
