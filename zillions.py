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

from math import log10, trunc

MAX_VALUE = 10**66 - 1

def num_digits(num: int) -> int:
    """Return the number of digits of an integer."""
    num = abs(num)
    return 1 if num == 0 else trunc(log10(num))

def name_int(num: int, scale='short') -> str:

    # check number within nameable range
    if abs(num) > MAX_VALUE:
        raise ValueError("Number out of range.")
    # return 'zero' if num = 0
    elif num == 0:
        return 'zero'

    sign = 'negative ' if num < 0 else ''
    num = abs(num)

    period_len = 3 if scale == 'short' else 6
    init_period_len = num_digits(num) % period_len
    if init_period_len == 0:
        init_period_len == period_len
    pass
    

# dictionary: sexdecillion
# henckle: sexdecillion
# natural: sexdecillion
# zilli: sexdecillion
# conway: sedecillion
# conway_modified: sedecillion
# conway_simplified: sexdecillion
# conway_reversed: sexdecillion
