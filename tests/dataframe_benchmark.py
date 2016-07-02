from utils.general_utils import csv_to_dataframes_dict
from logbook import Logger, StreamHandler
from time import time
import pandas
import sys
"""
Test the performance affected by working on data frame by rows vs columns.
"""

StreamHandler(sys.stdout).push_application()
logger = Logger(__name__)
test_set = csv_to_dataframes_dict("./data/bench/")  # 100 dataframes

def benchmark():

    logger.info("starting forloop benchmark")
    start = time()
    for table in test_set.values():
        table['forloop'] = pandas.Series(None, table.index)
        for row in table.index:
            table.set_value(row, 'forloop', table.loc[row, 'Open'] + table.loc[row, 'Close'])
    logger.info("finish forloop, took {} seconds\n".format(time() - start))

    logger.info("starting iterrows benchmark")
    start = time()
    for table in test_set.values():
        table['iterrows'] = pandas.Series(None, table.index)
        for index, row in table.iterrows():
            row.iterrows = row.Open + row.Close
    logger.info("finish iterrows, took {} seconds\n".format(time() - start))

    logger.info("starting itertuples benchmark")
    start = time()
    for table in test_set.values():
        table['itertuples'] = pandas.Series(None, table.index)
        col_idx = table.axes[1].tolist().index('itertuples')
        for row in table.iterrows():
            table.iloc[row[0], col_idx] = row[1].Open + row[1].Close
    logger.info("finish itertuples, took {} seconds\n".format(time() - start))

    logger.info("starting itertuples version2 benchmark")
    start = time()
    for table in test_set.values():
        table['itertuples2'] = pandas.Series(None, table.index)
        for row in table.iterrows():
            table.loc[row[0], 'itertuples'] = row[1].Open + row[1].Close
    logger.info("finish itertuples version 2, took {} seconds\n".format(time() - start))

    logger.info("starting itertuples version3 benchmark")
    start = time()
    for table in test_set.values():
        table['itertuples3'] = pandas.Series(None, table.index)
        #col_idx = table.axes[1].tolist().index('itertuples3')
        for row in table.iterrows():
            table.set_value(row[0], 'itertuples3', row[1].Open + row[1].Close)
    logger.info("finish itertuples version3, took {} seconds\n".format(time() - start))


    logger.info("starting columns benchmark")
    start = time()
    for table in test_set.values():
        table['columns'] = table.Open + table.Close
    logger.info("finish columns, took {} seconds\n".format(time() - start))

    import ipdb; ipdb.set_trace()


if __name__ == "__main__":
    benchmark()







