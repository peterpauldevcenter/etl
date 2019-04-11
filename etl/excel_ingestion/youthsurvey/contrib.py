from typing import Tuple, Set


class ExcelIngestionException(Exception):
    pass


def excel_column_alpha_to_index(column_alpha: str) -> int:
    """Given an Excel column alpha (case insensitive) value return the index

    .. note:: The index is 0 based like a normal list

    Examples:
        >>>> excel_column_alpha_to_index('atp') # 1211

    Args:
        column_alpha: alpha identifier of the column like "AA" or "AAB"

    Returns:
        index
    """
    if not column_alpha.isalpha():
        raise ValueError(
            f'{column_alpha} must be all alpha'
        )
    string = column_alpha.lower()
    letters = [char for char in string]
    letters.reverse()

    total = -1
    for index, letter in enumerate(letters):
        letter_base_value = ord(letter) - 96
        val = letter_base_value * 26 ** index
        total = total + val
    return total


def add_to_set_indicate_size_change(set_: set, element) -> Tuple[Set, bool]:
    """Return the set and whether or not the element changed the size.

    .. note::  There's probably a better way to do this...
    """
    size = len(set_)
    added = True
    set_.add(element)
    if size == len(set_):
        added = False
    return set_, added
