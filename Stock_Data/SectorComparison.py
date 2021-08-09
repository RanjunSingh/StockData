from Stock_Data.SMA import SMA

"""
pull data for these tickers, data -> alpha and beta.
sort into array
create a data class? pull data sort into appropriate sectors?



"""

class SectorComparison(SMA):
    # top 15 or so.
    techStocksSymbols = ["AAPL", "AMD", "MSFT", "ORCL", "INTC", "HPQ", "CSCO", "MU", "NVDA", "V", "QCOM", "HPE", "CRM",
                         "AMAT", "PYPL", "TXN",
                         "CTSH", "IBM", "AVGO", "FISV", "WDC", "APH", "JNPR", "GLW", "WU", "MA", "NLOK", "MXIM", "ADBE"]

    def __init__(self):
        self.__temp = None



