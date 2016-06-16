"""
file to put all the general utils in it
"""


def type_checking(expected_type, *objects):
    """
    Checks that each object in objects is of the expected type, otherwise raise TypeError
    @:param expected_type: also can be a list of type. Is so, it sufficient that one of the types is fit with the objects
    """
    assert objects
    if type(expected_type) is list or type(expected_type) is tuple:
        if any([object for object in objects if type(object) not in expected_type]):
            raise TypeError
    else:
        if any([object for object in objects if type(object) is not expected_type]):
            raise TypeError
