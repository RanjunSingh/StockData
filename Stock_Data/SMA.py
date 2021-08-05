import glob
import os
import statistics
from datetime import date

import pandas as pd
from pandas_datareader import data


class SMA:

    # constructor, travel behaviour needs to be added in
    def __init__(self):
        """

        """
        self.__THRESHHOLD = 5.0  # setting the threshhold to 5 for now.
        self.__filePath = ''
        self.__sma100List = []
        self.__symbolList = []
        self.__percentDeviations = []
        self.__outliers = []  # list of assets that deviate over the threshold.
        self.__latestPrice = []
        self.setup()

    def setup(self):
        print("Setting up files, symbols and calculating stuff...")
        self.getFilePath()
        self.readSymbols()

        print("Computing Moving Averages..")
        for i in self.__symbolList:
            self.__sma100List.append(self.getSma100(i))
            print(".", end="")

        print()

        print("Computing Deviations..")
        self.computeDeviations()

        self.accumulateOutliers()

        self.printOutliersToTxt()

        return

    def getFilePath(self):
        cwd = os.getcwd()
        print("CWD: " + cwd)
        self.__filePath = glob.glob(cwd + "/*.xlsx")[0]
        print("Using file " + self.__filePath)
        # self.__filePath = glob.glob(cwd + "/*.csv")[0]

    def getSma100(self, ticker):
        # have to calculate end date as today.
        # go back a 100 days to get start.
        startDate = '2021-03-01'  # rough can optimize.
        currentDate = date.today()

        data_frame = data.DataReader(ticker, 'yahoo', startDate, currentDate)
        todays_price_frame = data.DataReader(ticker, 'yahoo', currentDate)
        todays_price_close = todays_price_frame['Close']
        close = data_frame['Close']

        all_weekdays = pd.date_range(start=startDate, end=currentDate, freq='B')
        close = close.reindex(all_weekdays)
        close = close.fillna(method='ffill')

        # short_rolling_close = close.rolling(window=20).mean()
        sma100 = statistics.mean(close[-100:])

        # print(close[-1])
        # print(close.max())

        # print('100 day moving average: ' + str(sma100))

        return sma100

    # reads in the tickers from the excel spreadsheet.
    def readSymbols(self):
        cols = [1]
        # symbols = pd.read_excel(r'C:\Users\7438978\PycharmProjects\StockData\sample.xlsx', usecols=cols)
        symbols = pd.read_excel(self.__filePath, usecols=cols)

        # here we convert it into a symbolList to make it easier to use.
        for index, row in symbols.iterrows():
            self.__symbolList.append(row['Symbol'])

        return

    # function to calculate the difference between price and the 100 sma.
    def computeDeviations(self):
        cols = [2]
        prices = pd.read_excel(self.__filePath, usecols=cols)
        priceList = []

        for index, row in prices.iterrows():
            priceList.append(row['Price'])

        # percentDev = []

        for i in range(len(priceList)):
            self.__percentDeviations.append(self.percentDiff(priceList[i], self.__sma100List[i]))
            print(".", end="")

        print()
        print(self.__percentDeviations[0])

        return

    def accumulateOutliers(self):
        for i in range(len(self.__percentDeviations)):
            if abs(self.__percentDeviations[i]) >= self.__THRESHHOLD:
                self.__outliers.append((self.__symbolList[i], self.__percentDeviations[i]))

    def printOutliersToTxt(self):
        # Appending to te outlier file.
        with open('outliers.txt', 'a') as f:
            today = date.today()
            f.write(str(today) + '\n\n')

            for item in self.__outliers:
                # f.write("%s\n" % item)
                # f.write("".join(item))
                f.write(' '.join(str(field) for field in item) + '\n')

    def percentDiff(self, price, sma):
        perDiff = round(100 * (price - sma) / sma, 2)

        return perDiff

    # outputs the data array to the excel spreadsheet.
    def printToExcel(self):
        # fn = r'C:\Users\7438978\PycharmProjects\StockData\sample.xlsx'

        df = pd.read_excel(self.__filePath)
        df2 = pd.DataFrame({'Data': self.__sma100List})
        df3 = pd.DataFrame({'Deviations': self.__percentDeviations})
        newPrices = pd.DataFrame({'Prices': self.__latestPrice})

        writer = pd.ExcelWriter(self.__filePath, engine='openpyxl')

        df.to_excel(writer, index=False)
        df2.to_excel(writer, startcol=8, startrow=1, header=None, index=False)
        df3.to_excel(writer, startcol=9, startrow=1, header=None, index=False)
        newPrices.to_excel(writer, startcol=10, startrow=1, header="PriceUpdate", index=False)

        writer.save()
