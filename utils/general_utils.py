from pandas import DataFrame
import os
#from logbook import Logger
"""
file to put all the general utils in it
"""
#from logger.__init__  import log_handler
#log_handler.push_application()
#log = Logger(__name__)

def type_checking(expected_type, *objects):
    """
    Checks that each object in objects is of the expected type, otherwise raise TypeError
    @:param expected_type: also can be a list of type. Is so, it sufficient that one of the types is fit with the objects
    """
    assert objects
    if type(expected_type) is list or type(expected_type) is tuple:
        if any([object_i for object_i in objects if [not isinstance(object_i, e_type) for e_type in expected_type]]):
            raise TypeError
    else:
        if any([object for object in objects if not isinstance(object, expected_type)]):
            raise TypeError


def csv_file_to_data_frame(path):
    return DataFrame.from_csv(path, index_col=None, infer_datetime_format=True)


def make_filepath(directory, filename, extension=None):
    """
    Create file in path = directory/filename.extension. Also create the directory it doesn't exist.
    :return: The file path
    """
    if not os.path.exists(directory):
        os.makedirs(directory)
        # log.info('New directory was created at {}'.format(os.path.abspath('.')+'/'+directory))
    filepath = directory + '/' + filename
    if extension:
        filepath += "." + extension
    return filepath




