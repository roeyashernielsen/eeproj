from collections import OrderedDict

"""
This file defines the tables attributes that summarize the statistics tables that are displayed to the user.

"""


# The attributes of each table defined by the next OrderedDict. The items are tuples of (variable, title)

# This tables contains the all statistics of both the system and all the participated stocks
full_statistics = OrderedDict([('name', 'Name'), ('start_date', 'Start Date'), ('end_date', 'End Date'), ('period', 'Term (# days)'),
                               ('trades', 'Total Number of Trades'), ('winning_trades', '# of Winning Trades'), ('losing_trades', '# of Losing Trades'),
                               ('average_yield_percentages', 'Average Profit (%)'), ('stdev_yield_percentages', 'stdev'),
                               ('average_yield_points', 'Average Profit ($)'), ('stdev_yield_points', 'stdev'),
                               ('profit_loss_ratio_percentages', 'Profit Loss Ratio (%)'), ('profit_loss_ratio_points', 'Profit Loss Ratio ($)'),
                               ('max_profit_percentages', 'Max Profit (%)'), ('max_profit_points', 'Max Profit ($)'),
                               ('max_loss_percentages', 'Max Loss (%)'), ('max_loss_points', 'Max Loss ($)'),
                               ('total_holding_period', 'Total Holding Period'),
                               ('average_holding_period', 'Average Holding Period (per trade)'),
                               ('efficiency', '% Time of Open Position')])


# The next tables are per for specific stock, by user choice
general_details = OrderedDict([('name', 'Name'), ('start_date', 'Start Date'), ('end_date', 'End Date'),
                               ('period', 'Term (# days)'), ('total_holding_period', 'Total Holding Period'),
                               ('efficiency', '% Time of Open Position')])

performances = OrderedDict([('trades', 'Total Number of Trades'), ('winning_trades', '# of Winning Trades'),
                            ('losing_trades', '# of Losing Trades'), ('profit_loss_ratio_percentages', 'Profit Loss Ratio (%)'),
                            ('profit_loss_ratio_points', 'Profit Loss Ratio ($)')])

averages_and_bounds = OrderedDict([('average_yield_percentages', 'Average Profit (%)'), ('stdev_yield_percentages', 'stdev'),
                                   ('average_yield_points', 'Average Profit ($)'), ('stdev_yield_points', 'stdev'),
                                   ('average_holding_period', 'Average Holding Period (per trade)'), ('stdev_holding_period', 'stdev'),
                                   ('max_profit_percentages', 'Max Profit (%)'), ('max_profit_points', 'Max Profit ($)'),
                                   ('max_loss_percentages', 'Max Loss (%)'), ('max_loss_points', 'Max Loss ($)')])




