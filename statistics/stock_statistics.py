"""
This file liable for the statistics calculations of the trades per single stock
The statistics are based on the trades than been done over the analyzed time. Those trades are represented by the
stock data table post the processing progress (shrunk table contains only rows contains the open and close triggers),
but some of them may be need also the full table.
"""

def calculate_stock_statistics(filtered_stock_data):
    """
    This function calculates all the statistics over the traders history
    :param filtered_stock_data: DataFrame table filled with the rows of the open days and close days.
    :return:
    """
    check_filtered_data(filtered_stock_data)




def

