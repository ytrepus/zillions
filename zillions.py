"""A function for naming large integers

    Primary range: |x| < 10^66
    Extended range: |x| < 10^306

    The primary range is the range of integers that can be named in the short
    scale (which is used in the English-speaking world) using number words 
    that can be found in dictionaries.  This is the range enabled by default
    and the only 'official' names for numbers, apart from a few scattered
    larger ones like 'googol' and 'centillion'.
    
    The function can also name some larger integers if required.  For the
    extended range, the names of large numbers are no longer standardized,
    and this program uses a less-common system of words that first saw the
    light of day in the nineteenth century, credited to a 'W.G. Henkle' and 
    resurrected and tidied up in the publication 'Word Ways' over a series
    of articles, including by Rudolf Ondrejka in 1968.

    Functions:
        num_to_words(num: int, extended: bool=False) -> str:
            Returns the English name of a larger number.
"""

from math import ceil
import re
from typing import Generator

def num_to_words(num: int, extended: bool=False) -> str:
    """Returns the English name of a large number.

    If extended set to False (the default), the range is |x| < 10^66,
    otherwise, numbers up to |x| < 10^306 can be named.
    """

    max_value = 10**306 - 1 if extended else 10**66 - 1
    if abs(num) > max_value:
        raise ValueError("Number out of naming range.")
    elif num == 0:
        return 'zero'

    sign_word = 'negative ' if num < 0 else ''
    num = abs(num)

    digits = str(num)

    # small names are the names of each group of three digits, and zlist
    # is an iterator containing large number words, the 'zillions'
    small_names = _small_name_gen(digits)
    zillions_list = _zillions_list_gen(digits)
    
    number_name = []
    for name, zillion in zip(small_names, zillions_list):
        if name:
            number_name.append(name + zillion)
    number_name = sign_word + ' '.join(number_name)
    return re.sub(r',$', '', number_name)

def _small_name_gen(digits: str) -> Generator[str, None, None]:
    """Generate a list of number names for each group of three digits"""
    slice_stop = 3 if len(digits) % 3 == 0 else len(digits) % 3
    digit_slice = slice(0, slice_stop)
    group = digits[digit_slice]
    while group:
        yield _get_small_name(group)
        digit_slice = slice(digit_slice.stop, digit_slice.stop + 3)
        group = digits[digit_slice]

def _get_small_name(group: str) -> str:
    """Name numbers 1 to 999"""
    group = int(group)
    hundreds_digit = group // 100
    tens_digit = (group % 100) // 10
    ones_digit = group % 10
    hundreds_name = ONES[hundreds_digit] + " hundred " if hundreds_digit else ""
    
    if tens_digit == 0:
        tens_and_ones_name = ONES[ones_digit]
    elif tens_digit == 1:
        tens_and_ones_name = TEENS[ones_digit]
    else:
        tens_and_ones_name = TENS[tens_digit] + '-' + ONES[ones_digit]

    name = hundreds_name + tens_and_ones_name
    return re.sub(r'[-\s]$', '', name)

def _zillions_list_gen(digits: int) -> Generator[str, None, None]:
    """Generate a list of large number words required for the number name."""
    max_zillions_index = ceil(len(digits) / 3) - 2
    if max_zillions_index > 20:
        yield from _large_zlist_gen(max_zillions_index)
        max_zillions_index = 20
    for index in range(max_zillions_index, -1, -1):
        yield ' ' + ZILLIONS[index]
    yield ''

def _large_zlist_gen(max_zillions_index: int) -> Generator[str, None, None]:
    """Generate names for the extended range of zillions."""
    for index in range(max_zillions_index, 20, -1):
        prefix = LARGE_ZILLION_PREFIXES[index % 10]
        zillion = LARGE_ZILLIONS[index // 10]
        yield ' ' + prefix + zillion

# lists of number words
ONES = [
    '', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine'
    ]

TEENS = [
    'ten', 'eleven', 'twelve', 'thirteen', 'fourteen', 'fifteen', 'sixteen', 
    'seventeen', 'eighteen', 'nineteen'
    ]

TENS = [
    '', 'ten', 'twenty', 'thirty', 'forty', 'fifty', 'sixty', 'seventy', 
    'eighty', 'ninety'
    ]

ZILLIONS = [
    'thousand', 'million', 'billion', 'trillion', 'quadrillion', 
    'quintillion', 'sextillion', 'septillion', 'octillion', 'nonillion', 
    'decillion', 'undecillion', 'duodecillion', 'tredecillion', 
    'quattuordecillion', 'quindecillion', 'sexdecillion', 'septendecillion', 
    'octodecillion', 'novemdecillion', 'vigintillion'
    ]

LARGE_ZILLION_PREFIXES = [
    '', 'primo-', 'secundo-', 'tertio-', 'quarto-', 'quinto-', 'sexto-',
    'septimo-', 'octavo-', 'nono-'
    ]

LARGE_ZILLIONS = [
    '', 'decillion', 'vigintillion', 'trigintillion', 'quadragintillion',
    'quinquagintillion', 'sexagintillion', 'septuagintillion', 
    'octogintillion', 'nonagintillion', 'centillion'
    ]
