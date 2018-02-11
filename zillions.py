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

from collections import deque
from itertools import chain, repeat
from math import ceil, log10, trunc
import re
from typing import List, Generator

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
    zlist = _zlist_gen(digits)
    
    number_name = []
    for name, zillion in zip(small_names, zlist):
        if name:
            number_name.append(name + zillion)
    number_name = sign_word + ' '.join(number_name)
    return re.sub(r',$', '', number_name)

def _small_name_gen(digits: str) -> Generator:
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
    h_digit = group // 100
    t_digit = (group % 100) // 10
    o_digit = group % 10
    h_name = ONES[h_digit] + " hundred " if h_digit else ""
    
    if t_digit == 0:
        to_name = ONES[o_digit]
    elif t_digit == 1:
        to_name = TEENS[o_digit]
    else:
        to_name = TENS[t_digit] + '-' + ONES[o_digit]

    name = h_name + to_name
    return re.sub(r'[-\s]$', '', name)

def _zlist_gen(digits: int) -> Generator:
    """Generate a list of large number words required for the number name."""
    zstart = ceil(len(digits) / 3) - 2
    if zstart > 20:
        yield from _large_zlist_gen(zstart)
        zstart = 20
    for index in range(zstart, -1, -1):
        yield ' ' + ZILLIONS[index]
    yield ''

def _large_zlist_gen(zstart: int) -> Generator:
    """Generate names for the extended range of zillions."""
    for index in range(zstart, 20, -1):
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
