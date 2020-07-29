# Copyright 2018 DeepMind Technologies Limited.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Functionality for displaying expressions.

SymPy provides a lot of functionality for displaying expressions, but it's
slightly too centered on being a symbolic maths engine to provides all our
needs. For example, it's impossible to display an unsimplified fraction like
3/6, or a decimal that isn't internally represented as a float and thus subject
to rounding.

Also provides some other convenience such as converting numbers to words, and
displaying percentages (properly formatted).
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import decimal

# Dependency imports
import sympy


# For converting integers to words:
_INTEGER_LOW = [
    ['ноль', 'ноль', "нуле", "нуля"], 
    ['один','один',"одном","одного"], 
    ['два','два',"двух","двух"], 
    ['три','три',"трёх", "трёх"], 
    ['четыре', 'четыре',"четырёх", "четырёх"],
    ['пять', "пять", "пяти", "пяти"], 
    ['шесть','шесть',"шести","шести"], 
    ['семь','семь',"семи","семи"], 
    ['восемь','восемь',"восьми","восьми"],
    ['девять','девять',"девяти","девяти"], 
    ['десять','десять','десяти',"десяти"], 
    ['одиннадцать','одиннадцать',"одиннадцати", "одиннадцати"], 
    ['двенадцать','двенадцать','двенадцати', "двенадцати"], 
    ['тринадцать','тринадцать','тринадцати',"тринадцати"],
    ['четырнадцать','четырнадцать','четырнадцати',"четырнадцати"], 
    ['пятнадцать','пятнадцать','пятнадцати','пятнадцати'],
    ['шестнадцать','шестнадцать','шестнадцати','шестнадцати'], 
    ['семнадцать','семнадцать','семнадцати', 'семнадцати'], 
    ['восемнадцать','восемнадцать','восемнадцати', 'восемнадцати'], 
    ['девятнадцать','девятнадцать','девятнадцати', 'девятнадцати']
]

_INTEGER_LOW_FEM = [
    ['ноль', 'ноль', "нуле", "нуля"], 
    ['одна','одну',"одной", "одной"], 
    ['две','две',"двух", "двух"], 
    ['три','три',"трёх", "трёх"], 
    ['четыре', 'четыре',"четырёх", "четырёх"],
    ['пять', "пять", "пяти", "пяти"], 
    ['шесть','шесть',"шести", "шести"], 
    ['семь','семь',"семи", "семи"], 
    ['восемь','восемь',"восьми", "восьми"],
    ['девять','девять',"девяти", "девяти"], 
    ['десять','десять','десяти', "десяти"], 
    ['одиннадцать','одиннадцать',"одиннадцати","одиннадцати"], 
    ['двенадцать','двенадцать','двенадцати', 'двенадцати'], 
    ['тринадцать','тринадцать','тринадцати', 'тринадцати'],
    ['четырнадцать','четырнадцать','четырнадцати', 'четырнадцати'], 
    ['пятнадцать','пятнадцать','пятнадцати', 'пятнадцати'],
    ['шестнадцать','шестнадцать','шестнадцати', 'шестнадцати'], 
    ['семнадцать','семнадцать','семнадцати', 'семнадцати'], 
    ['восемнадцать','восемнадцать','восемнадцати', 'восемнадцати'], 
    ['девятнадцать','девятнадцать','девятнадцати','девятнадцати']
]


_INTEGER_MID = [
    ['',"",""], 
    ['',"",""], 
    ['двадцать', 'двадцать', 'двадцати', 'двадцати'], 
    ['тридцать','тридцать','тридцати', "тридцати"], 
    ['сорок','сорок','сорока', 'сорока'], 
    ['пятьдесят','пятьдесят','пятидесяти', 'пятидесяти'], 
    ['шестьдесят','шестьдесят','шестидесяти', 'шестидесяти'], 
    ['семьдесят','семьдесят','семидесяти', 'семидесяти'], 
    ['восемьдесят','восемьдесят','восьмидесяти', 'восьмидесяти'],
    ['девяносто','девяносто','девяноста', 'девяноста']
]
_INTEGER_HIGH = [
    (int(1e12), ['триллион','триллион','триллионе',"триллиона", "триллионов"]), 
    (int(1e9), ['миллиард',"миллиард","миллиарде","миллиарда", "миллиардов"]), 
    (int(1e6), ['миллион',"миллион","миллионе","миллиона", "миллионов"]),
    (int(1e3), ['тысяча',"тысячу","тысяче","тысячи", "тысяч"]), 
    (100, ['сотня',"сотню","сотне", "сотни", "сотен"])
]


# For converting rationals to words:
_SINGULAR_DENOMINATORS = [
    ['','','',], 
    ['','','',],
    ['вторая','вторую','второй',],
    ['третья','третью','третьей',], 
    ['четвертая','четвертую','четвертой',], 
    ['пятая','пятую','пятой',], 
    ['шестая','шестую','шестой',], 
    ['седьмая','седьмую','седьмой',], 
    ['восьмая','восьмую','восьмой',],
    ['девятая','девятую','девятой',], 
    ['десятая','десятую','десятой',], 
    ['одиннадцатая','одиннадцатую','одиннадцатой',], 
    ['двенадцатая','двенадцатую','двенадцатой',], 
    ['тринадцатая','тринадцатую','тринадцатой',], 
    ['четырнадцатая','четырнадцатую','четырнадцатой',],
    ['пятнадцатая','пятнадцатую','пятнадцатой',], 
    ['шестнадцатая','шестнадцатую','шестнадцатой',], 
    ['семнадцатая','семнадцатую','семнадцатой',], 
    ['восемнадцатая','восемнадцатую','восемнадцатой',], 
    ['девятнадцатая','девятнадцатую','девятнадцатой',],
    ['двадцатая','двадцатую','двадцатой',],
]



_PLURAL_DENOMINATORS = [
    '', '', 'вторых', 'третьих', 'четвертых', 'пятых', 'шестых', 'седьмых',
    'восьмых', 'девятых', 'десятых', 'одиннадцатых', 'двенадцатых', 'тринадцатых',
    'четырнадцатых', 'пятнадцатых', 'шестнадцатых', 'семнадцатых', 'восемнадцатых',
    'девятнадцатых', 'двадцатых'
]


# For converting ordinals to words:
_ORDINALS = [
    'нулевой', 'первый', 'второй', 'третий', 'четвертый', 'пятый', 'шестой', 'седьмой',
    'восьмой', 'девятый', 'десятый', 'одиннадцатый', 'двенадцатый', 'тринадцатый',
    'четырнадцатый', 'пятнадцатый', 'шестнадцатый', 'семнадцатый', 'восемнадцатый',
    'девятнадцатый', 'двадцатый'
]

_ORDINALS_NEU = [
    'нулевое', 'первое', 'второе', 'третье', 'четвертое', 'пятое', 'шестое', 'седьмое',
    'восьмое', 'девятое', 'десятое', 'одиннадцатое', 'двенадцатое', 'тринадцатое',
    'четырнадцатое', 'пятнадцатое', 'шестнадцатое', 'семнадцатое', 'восемнадцатое',
    'девятнадцатое', 'двадцатое'
]

_ORDINALS_FEM = [
    'нулевая', 'первая', 'вторая', 'третья', 'четвертая', 'пятая', 'шестая', 'седьмая',
    'восьмая', 'девятая', 'десятая', 'одиннадцатая', 'двенадцатая', 'тринадцатая',
    'четырнадцатая', 'пятнадцатая', 'шестнадцатая', 'семнадцатая', 'восемнадцатая',
    'девятнадцатая', 'двадцатая'
]

_ORDINALS_FEM_GEN = [
    'нулевую', 'первую', 'вторую', 'третью', 'четвертую', 'пятую', 'шестую', 'седьмую',
    'восьмую', 'девятую', 'десятую', 'одиннадцатую', 'двенадцатую', 'тринадцатую',
    'четырнадцатую', 'пятнадцатую', 'шестнадцатую', 'семнадцатую', 'восемнадцатую',
    'девятнадцатую', 'двадцатую'
]


def check_one_ending(num):
    num = str(num)
    if num[-1] == '1':
        if len(num) == 1 or num[-2] != '1':
            return True
        else:
            return False
    else:
        return False
        



class Decimal(object):
  """Display a value as a decimal."""

  def __init__(self, value):
    """Initializes a `Decimal`.

    Args:
      value: (Sympy) value to display as a decimal.

    Raises:
      ValueError: If `value` cannot be represented as a non-terminating decimal.
    """
    self._value = sympy.Rational(value)

    numer = int(sympy.numer(self._value))
    denom = int(sympy.denom(self._value))

    denom_factors = list(sympy.factorint(denom).keys())
    for factor in denom_factors:
      if factor not in [2, 5]:
        raise ValueError('Cannot represent {} as a non-recurring decimal.'
                         .format(value))
    self._decimal = decimal.Decimal(numer) / decimal.Decimal(denom)

  @property
  def value(self):
    """Returns the value as a `sympy.Rational` object."""
    return self._value

  def _sympy_(self):
    return self._value

  def decimal_places(self):
    """Returns the number of decimal places, e.g., 32 has 0 and 1.43 has 2."""
    if isinstance(self._decimal, int):
      return 0
    elif isinstance(self._decimal, decimal.Decimal):
      return -self._decimal.as_tuple().exponent

  def __str__(self):
    sign, digits, exponent = self._decimal.as_tuple()
    sign = '' if sign == 0 else '-'

    num_left_digits = len(digits) + exponent  # number digits "before" point

    if num_left_digits > 0:
      int_part = ''.join(str(digit) for digit in digits[:num_left_digits])
    else:
      int_part = '0'

    if exponent < 0:
      frac_part = '.'
      if num_left_digits < 0:
        frac_part += '0' * -num_left_digits
      frac_part += ''.join(str(digit) for digit in digits[exponent:])
    else:
      frac_part = ''

    return sign + int_part + frac_part

  def __add__(self, other):
    if not isinstance(other, Decimal):
      raise ValueError('Arithmetic support limited to other `Decimal`s.')
    return Decimal(self.value + other.value)

  def __sub__(self, other):
    if not isinstance(other, Decimal):
      raise ValueError('Arithmetic support limited to other `Decimal`s.')
    return Decimal(self.value - other.value)

  def __mul__(self, other):
    if not isinstance(other, Decimal):
      raise ValueError('Arithmetic support limited to other `Decimal`s.')
    return Decimal(self.value * other.value)

  def __neg__(self):
    return Decimal(-self.value)

  def round(self, ndigits=0):
    """Returns a new `Decimal` rounded to this many decimal places."""
    scale = sympy.Integer(10 ** ndigits)
    numer = sympy.numer(self.value) * scale
    denom = sympy.denom(self.value)
    return Decimal(int(round(numer / denom)) / scale)

  def __round__(self, ndigits):
    return self.round(ndigits)

  def __int__(self):
    """Returns conversion to integer if possible; TypeError if non-integer."""
    if self.decimal_places() == 0:
      return int(self._decimal)
    else:
      raise TypeError('Cannot represent {} as an integer.'.format(str(self)))

  # NOTE: this is implemented in addition to `__cmp__` because SymPy does not
  # support inequality comparison between sympy objects and objects that are not
  # convertible to sympy objects (such as strings).
  def __eq__(self, other):
    return self.value == other

  # Python 2 comparison
  def __cmp__(self, other):
    if self.value == other:
      return 0
    if self.value < other:
      return -1
    return 1

  # Python 3 comparison:
  def __lt__(self, other):
    return self.value < other

  def __le__(self, other):
    return self.value <= other

  def __gt__(self, other):
    return self.value > other

  def __ge__(self, other):
    return self.value >= other


class Percentage(object):
  """Container for a percentage."""

  def __init__(self, value):
    """Initializes a `Percentage`.

    Args:
      value: Percentage as a fractional value. E.g., pass in
          `sympy.Rational(2, 5)` to create the percentage "40%".
    """
    self._value = value

  def _sympy_(self):
    return self._value

  def __str__(self):
    # Display percentages as decimals (not fractions).
    value = Decimal(self._value * 100)
    return str(value) + '%'


class NonSimpleRational(object):
  """Container for rational a / b where allow gcd(a, b) > 1."""

  def __init__(self, numer, denom):
    self._numer = numer
    self._denom = denom

  @property
  def numer(self):
    return self._numer

  @property
  def denom(self):
    return self._denom

  def __str__(self):
    return '{}/{}'.format(self._numer, self._denom)


class StringNumber(object):
  """A string representing a number, that can also be sympified."""

  def __init__(self, value, join_number_words_with_hyphens=True, case='nom', 
    desyatok=False, gender=False, singular=False):
    """Initializes a `StringNumber`.

    Args:
      value: An integer or rational.
      join_number_words_with_hyphens: Whether to join the words in integers with
          hyphens when describing as a string.
    """
    self._case = ['nom', 'perevedi', 'v', 'do'].index(case)
    self._sing = singular
    self._gender = gender
    self._join_number_words_with_hyphens = join_number_words_with_hyphens
    self._sympy_value = sympy.sympify(value)
    self._string = self._to_string(value)
    
    

  def _integer_to_words(self, integer, composite=False):
    """Converts an integer to a list of words."""
    if integer < 0:
      raise ValueError('Cannot handle negative numbers.')
    if integer == 10 and not composite:
      return [['десятки',"десятки", "десятки", "десятков"][self._case]]
    if integer < 20:
      return [_INTEGER_LOW[integer][self._case]] if not self._gender else [_INTEGER_LOW_FEM[integer][self._case]]

    words = None

    if integer < 100:
      tens, ones = divmod(integer, 10)
      if ones > 0:
        return [_INTEGER_MID[tens][self._case], _INTEGER_LOW[ones][self._case]] \
                            if not self._gender else [_INTEGER_MID[tens][self._case],
                                                      _INTEGER_LOW_FEM[ones][self._case]]
      else:
        return [_INTEGER_MID[tens][self._case]]

    for value, word in _INTEGER_HIGH:
      if integer >= value:
        den, rem = divmod(integer, value)
        if den == 1:
          if self._sing:
            idx = -2
          else:
            idx = -1
          words = [word[idx]]
        else:
          if self._sing:
            idx = -2
          else:
            idx = -1
          words = self._integer_to_words(den, composite=True) + [word[idx]]
        if rem > 0:
          # if rem < 100:
          #   words.append('и')
          words += self._integer_to_words(rem, composite=True)
        return words

  def _rational_to_string(self, rational):
    """Converts a rational to words, e.g., "two thirds"."""
    numer = sympy.numer(rational)
    if check_one_ending(numer):
        self._gender='fem'
    denom = sympy.denom(rational)

    numer_words = self._to_string(numer)

    if denom == 1:
      return numer_words

    if denom <= 0 or denom >= len(_PLURAL_DENOMINATORS):
      raise ValueError('Unsupported denominator {}.'.format(denom))

    if numer == 1 or check_one_ending(numer):
      denom_word = _SINGULAR_DENOMINATORS[denom][self._case]
    else:
      denom_word = _PLURAL_DENOMINATORS[denom]

    return '{} {}'.format(numer_words, denom_word)

  def _to_string(self, number):
    """Converts an integer or rational to words."""
    if isinstance(number, sympy.Integer) or isinstance(number, int):
      words = self._integer_to_words(number)
      join_char = ' '
      return join_char.join(words)
    elif isinstance(number, sympy.Rational):
      return self._rational_to_string(number)
    else:
      raise ValueError('Unable to handle number {} with type {}.'
                       .format(number, type(number)))

  def _sympy_(self):
    return self._sympy_value

  def __str__(self):
    return self._string



class StringOrdinal(object):
  """A string representation of an ordinal, e.g., "first"."""

  def __init__(self, position):
    """Initializes a `StringOrdinal`.

    Args:
      position: An integer >= 0.

    Raises:
      ValueError: If `position` is non-positive or out of range.
    """
    if position < 0 or position >= len(_ORDINALS):
      raise ValueError('Unsupported ordinal {}.'.format(position))
    self._string = _ORDINALS[position]

  def __str__(self):
    return self._string

class StringOrdinal_neu(object):
  """A string representation of an ordinal, e.g., "first"."""

  def __init__(self, position):
    """Initializes a `StringOrdinal`.

    Args:
      position: An integer >= 0.

    Raises:
      ValueError: If `position` is non-positive or out of range.
    """
    if position < 0 or position >= len(_ORDINALS):
      raise ValueError('Unsupported ordinal {}.'.format(position))
    self._string = _ORDINALS_NEU[position]

  def __str__(self):
    return self._string



class StringOrdinal_fem_gen(object):
  """A string representation of an ordinal, e.g., "first"."""

  def __init__(self, position):
    """Initializes a `StringOrdinal`.

    Args:
      position: An integer >= 0.

    Raises:
      ValueError: If `position` is non-positive or out of range.
    """
    if position < 0 or position >= len(_ORDINALS_FEM_GEN):
      raise ValueError('Unsupported ordinal {}.'.format(position))
    self._string = _ORDINALS_FEM_GEN[position]

  def __str__(self):
    return self._string

class StringOrdinal_fem(object):
  """A string representation of an ordinal, e.g., "first"."""

  def __init__(self, position):
    """Initializes a `StringOrdinal`.

    Args:
      position: An integer >= 0.

    Raises:
      ValueError: If `position` is non-positive or out of range.
    """
    if position < 0 or position >= len(_ORDINALS_FEM):
      raise ValueError('Unsupported ordinal {}.'.format(position))
    self._string = _ORDINALS_FEM[position]

  def __str__(self):
    return self._string



class NumberList(object):
  """Contains a list of numbers, intended for display."""

  def __init__(self, numbers):
    self._numbers = numbers

  def __str__(self):
    """Converts the list to a string.

    Returns:
      Human readable string.

    Raises:
      ValueError: if any of the strings contain a comma and thus would lead to
          an ambigious representation.
    """
    strings = []
    for number in self._numbers:
      string = str(number)
      if ',' in string:
        raise ValueError('String representation of the list will be ambigious, '
                         'since term "{}" contains a comma.'.format(string))
      strings.append(string)
    return ', '.join(strings)


class NumberInBase(object):
  """Contains value, represented in a given base."""

  def __init__(self, value, base):
    """Initializes a `NumberInBase`.

    Args:
      value: Positive or negative integer.
      base: Integer in the range [2, 36].

    Raises:
      ValueError: If base is not in the range [2, 36] (since this is the limit
          that can be represented by 10 numbers plus 26 letters).
    """
    if not 2 <= base <= 36:
      raise ValueError('base={} must be in the range [2, 36]'.format(base))
    self._value = value
    self._base = base

    chars = []
    remainder = abs(value)
    while True:
      digit = remainder % base
      char = str(digit) if digit <= 9 else chr(ord('a') + digit - 10)
      chars.append(char)
      remainder = int(remainder / base)
      if remainder == 0:
        break
    if value < 0:
      chars.append('-')

    self._str = ''.join(reversed(chars))

  def __str__(self):
    return self._str

  def _sympy_(self):
    return self._value
