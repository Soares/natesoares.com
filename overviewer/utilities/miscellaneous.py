def roman_numeral(number):
    """
    Convert a number between 0 and 4999 inclusive to roman numerals
    >>> roman_numeral(0)
    ''
    >>> roman_numeral(1)
    'I'
    >>> roman_numeral(3)
    'III'
    >>> roman_numeral(8)
    'VIII'
    >>> roman_numeral(97)
    'XCVII'
    >>> roman_numeral(1900)
    'MCM'
    >>> roman_numeral(4999)
    'MMMMCMXCIX'
    """
    numerals = (
        (1000, 'M'),
        (900, 'CM'),
        (500, 'D'),
        (400, 'CD'),
        (100, 'C'),
        (90, 'XC'),
        (50, 'L'),
        (40, 'XL'),
        (10, 'X'),
        (9, 'IX'),
        (5, 'V'),
        (4, 'IV'),
        (1, 'I'),
    )
    def shift((number, string), (value, roman)):
        quotient = number // value
        return number - (value * quotient), string + (roman * quotient)
    return reduce(shift, numerals, (number, ''))[1]
