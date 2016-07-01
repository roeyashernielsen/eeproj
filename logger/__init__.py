from logbook import FileHandler


LOG_DIR = './logs/'

"""
Inititate logging environment and log files.

usage- import the log handler in the __init__ file of the module we want to use the logger, and inside the file
create instance of Logger that use the file name as print prefix: logger = Logger(__name__)
"""


# TODO add timestamp (without creating 2 files)
#timestamp = LOG_DIR + str(datetime.now()).replace(' ', '_')

general_log_handler = FileHandler(LOG_DIR + 'general.log', mode='w', bubble=True).push_application()

