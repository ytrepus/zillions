# zillions
A module for naming large integers

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
