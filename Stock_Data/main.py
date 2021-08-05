from Stock_Data.SMA import SMA
from Stock_Data.SectorComparison import SectorComparison

def main():
    # instantiate an object of the sma class.
    sma100 = SMA()
    sma100.printToExcel()  # print to the excel file (first one in directory)

    return


if __name__ == '__main__':
    main()

"""
create a data class (import filepath and everything.
inherit to sma class and sector comparison class.



"""