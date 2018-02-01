"""Functions for naming large integers (using only dictionary words)

    range: -999999999999999999999999999999999999999999999999999999999999999999
        to +999999999999999999999999999999999999999999999999999999999999999999

    This is the range of integers that can be named in the short scale using
    words found in dictionaries*.  There are quite a few ad-hoc systems for 
    naming numbers larger than this, but the lack of consistency and 
    consensus, even among the more 'authoritative' options, is a bit 
    unsatisfying, so I plan to stick with the core dictionary words.

    *Particularly, unabridged American dictionaries.  UK English dictionaries
    like the Oxford English Dictionary not to have number words after
    'decillion', which in the long scale allow you to name the exact same 
    range.  Britain traditionally used the long scale, like much of the rest
    of the world, but now uses the short scale in line with the USA.

    Much more info on the long and short scales can be found here:
    https://en.wikipedia.org/wiki/Long_and_short_scales
"""

from itertools import chain, repeat
from math import log10, trunc
import re
from typing import List

MAX_VALUE = 10**66 - 1

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
    '',  'thousand', 'million', 'billion', 'trillion', 'quadrillion', 
    'quintillion', 'sextillion', 'septillion', 'octillion', 'nonillion', 
    'decillion', 'undecillion', 'duodecillion', 'tredecillion', 
    'quattuordecillion', 'quindecillion', 'sexdecillion', 'septendecillion', 
    'octodecillion', 'novemdecillion', 'vigintillion'
    ]

ZILLIARDS = [z.replace('ion', 'iard') for z in ZILLIONS[2:]]

def num_digits(num: int) -> int:
    """Return the number of digits of an integer."""
    num = abs(num)
    return 1 if num == 0 else trunc(log10(num))


def num_to_words(num: int, scale='short') -> str:
    # check number within nameable range
    if abs(num) > MAX_VALUE:
        raise ValueError("Number out of range.")
    # return 'zero' if num = 0
    elif num == 0:
        return 'zero'

    sign = 'negative ' if num < 0 else ''
    num = abs(num)

    periods = get_periods(num)
    period_names = map(name_period, periods)
    zillions = get_zillions(scale)
    name_list = []
    for period_name, zillion in zip(period_names, zillions):
        if not period_name:
            continue
        name_segment = f"{period_name} {zillion}"
        name_list.append(name_segment)
    return re.sub(r' $', '', ' '.join(reversed(name_list)))


def get_periods(num: int) -> List[str]:
    digits = str(num)
    start = -3
    period = digits[start:]
    period_list = []
    while period:
        period_list.append(period)
        start, end = start - 3, start
        period = digits[start: end]
    return period_list


def name_period(period: str) -> str:
    period = int(period)
    h_digit = period // 100
    t_digit = (period % 100) // 10
    o_digit = period % 10
    h_name = ONES[h_digit] + " hundred " if h_digit else ""
    
    if t_digit == 0:
        to_name = ONES[o_digit]
    elif t_digit == 1:
        to_name = TEENS[o_digit]
    else:
        to_name = TENS[t_digit] + '-' + ONES[o_digit]

    name = h_name + to_name
    return re.sub(r'[ -]$', '', name)

def get_zillions(scale: str) -> List[str]:
    if scale == 'long_eu':
        return ZILLIONS[:2] + list(chain(*zip(ZILLIONS[2:], ZILLIARDS)))
    elif scale == 'long_br':
        return ZILLIONS[:2] + list(chain(*zip(ZILLIONS[2:],
                                   repeat("thousand"))))
    else:
        return ZILLIONS
