"""Measurement questions, e.g., "How many hours are there in a day?"."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import collections
import functools
import random

# Dependency imports
import example
from modules import train_test_split
from sample import number
from util import composition
from util import display
import six
import sympy


def _make_modules(is_train):
  """Returns modules, with split based on the boolean `is_train`."""
  return {
      'conversion': functools.partial(
          conversion, is_train=is_train, is_extrapolation=False),
      'time': functools.partial(time, is_train=is_train),
  }


def train(entropy_fn):
  """Returns dict of training modules."""
  del entropy_fn  # unused
  return _make_modules(is_train=True)


def test():
  """Returns dict of testing modules."""
  return _make_modules(is_train=False)


def test_extra():
  """Returns dict of extrapolation testing modules."""
  return {
      'conversion': functools.partial(
          conversion, is_train=False, is_extrapolation=True),
  }


Unit = collections.namedtuple('Unit', ('name', 'symbol', 'name_perevedi', 'name_skolko', 'name_v', ))


MICRO_SYMBOL = 'u'


LENGTH = {
    Unit('метры', 'м', ('метр', 'метра', 'метров'), "метров", ("метре", "метрах","метрах")): 1,
    Unit('километры', 'км', ("километр", "километра", 'километров'), "километров", ("километре", "километрах", "километрах")): 1000,
    Unit('сантиметры', 'см', ("сантиметр","сантиметра", "сантиметров"), "сантиметров", ("сантиметре","сантиметрах","сантиметрах")): sympy.Rational(1, 100),
    Unit('миллиметры', 'мм', ("миллиметр", "миллиметра",'миллиметров'), "миллиметров", ("миллиметре", "миллиметрах","миллиметрах")): sympy.Rational(1, 1000),
    Unit('микрометры', 'мкм', ("микрометр", "микрометра",'микрометров'), "микрометров", ("микрометре", "микрометрах","микрометрах")): sympy.Rational(1, 1e6),
    Unit('нанометры', 'нм', ("нанометр","нанометра",'нанометров'), "нанометров", ("нанометре", "нанометрах","нанометрах")): sympy.Rational(1, 1e9),
}

TIME = {
    Unit('секунды', 'сек', ("секунду","секунды",'секунд'), "секунд", ("секунде","секундах","секундах")): 1,
    Unit('минуты', None, ("минуту","минуты","минут"), "минут", ("минуте", "минутах", "минутах")): 60,
    Unit('часы', None, ("час", "часа", "часов"), "часов", ("часе", "часах", "часах")): 60*60,
    Unit('дни', None, ("день", "дня", "дней"), "дней", ("дне", "днях", "днях")): 24*60*60,
    Unit('недели', None, ("неделю","недели","недель"), "недель", ("неделе", "неделях","неделях")): 7*24*60*60,
    Unit('миллисекунды', 'мсек', ("миллисекунду", "миллисекунды", 'миллисекунд'), "миллисекунд", ("миллисекунде", "миллисекундах",
                                                                                                  "миллисекундах") ): sympy.Rational(1, 1e3),
    Unit('микросекунды', 'мксек', ("микросекунду", "микросекунды", 'микросекунд'), "микросекунд", ("микросекунде", "микросекундах",
                                                                                                    "микросекундах")): sympy.Rational(1, 1e6),
    Unit('наносекунды', 'нсек', ("наносекунду", "наносекунды", 'наносекунд'), "наносекунд", ("наносекунде", "наносекундах",
                                                                                              "наносекундах")): sympy.Rational(1, 1e9),
}

TIME_YEARLY = {
    Unit('годы', None, ("год", "года", "лет"), "лет", ("годе", "годах", "годах")): 1,
    Unit('десятилетия', None, ("десятилетие","десятилетия","десялетий"), 
                              "десятилетий", ("десятилетии", "десятилетиях","десятилетиях")): 10,
    Unit('века', None, ("век", "века","веков"), "веков", ("веке", "веках","веках")): 100,
    Unit('тысячелетия', None, ("тысячелетие","тысячелетия","тысячелетий"), 
                              "тысячелетий", ("тысячелетии", "тысячелетиях", "тысячелетиях")): 1000,
    Unit('месяцы', None, ("месяц", "месяца", "месяцев"), 
                              "месяцев", ("месяце","месяцах", "месяцах")): sympy.Rational(1, 12),
}

MASS = {
    Unit('килограммы', 'кг', ("килограмм", "килограмма","килограммов"), "килограмм", ("килограмме","килограммах",
                                                                                      "килограммах")): 1,  # Yes, the *kilo*gram is the SI base unit.
    Unit('тонны', 'т', ("тонну", "тонны", "тонн"), "тонн", ("тонне", "тоннах", "тоннах")): 1000,
    Unit('граммы', 'г', ("грамм", "грамма","граммов"), "грамм", ("грамме", "граммах", "граммах")): sympy.Rational(1, 1e3),
    Unit('миллиграммы', 'мг', ("миллиграмм", "миллиграмма","миллиграммов"), "миллиграмм", ("миллиграмме", "миллиграммах",
                                                                                          "миллиграммах")): sympy.Rational(1, 1e6),
    Unit('микрограммы', 'мкг', ("миграграмм","микрограмма","микрограммов"), "микрограмм", ("микрограмме", "микрограммах","микрограммах")): sympy.Rational(1, 1e9),
    Unit('нанограммы', 'нг',("нанограмм","нанограмма","нанограммов"), "нанограмм", ("нанограмме", "нанограммах", "нанограммах")): sympy.Rational(1, 1e12),
}

VOLUME = {
    Unit('литры', 'л', ("литр", "литра", "литров"), "литров", ("литре", "литрах", "литрах")): 1,
    Unit('миллилитры', 'мл',  ("миллилитр","миллилитра","миллилитров"), "миллилитров", ("миллилитре", 
                                                                                        "миллилитрах","миллилитрах")): sympy.Rational(1, 1000),
}


DIMENSIONS = [LENGTH, TIME, TIME_YEARLY, MASS, VOLUME]

# singular_prep = {'граммах':"грамме", 'килограммах':"килограмме", 'миллиграммах':"миллиграмме", 'микрограммах':"микрограмме",
# 'тоннах':"тонне", 'нанограммах':"нанограмме",  "литрах":"литре", "миллилтрах":"миллилитре", 
# "годах":"годе","десятилетиях":"десятилетии","веках":"веке","тесячелетиях":"тысячелетии","месяцах":"месяце",
# "секундах":"секунде", "минутах":"минуте","часах":"часе","днях":"дне","неделях":"неделе",
# "миллисекундах":"миллисекунде", "микросекундах":"микросекунде", "наносекундах":"наносекунде",
# "метрах":"метре", "километрах":"километре","сантиметрах":"сантиметре","миллиметрах":"миллиметре",
# "микрометрах":"микрометре", "нанометрах":"нанометре"}


# singular_gen = {
# 'граммов':"грамм", 'килограммов':"килограмм", 'миллиграммов':"миллиграмм", 'микрограммов':"микрограмм",
# 'тонн':"тонну", 'нанограммов':"нанограмм",  "литров":"литр", "миллилитров":"миллилитр", 
# "лет":"год","десятилетия":"десятилетие","века":"век","тесячелетия":"тысячелетие","месяцах":"месяце",
# "секунд":"секунде", "минутах":"минуте","часах":"часе","днях":"дне","неделях":"неделе",
# "миллисекунд":"миллисекунде", "микросекундах":"микросекунде", "наносекундах":"наносекунде",
# "метров":"метре", "километрах":"километре","сантиметрах":"сантиметре","миллиметрах":"миллиметре",
# "микрометрах":"микрометре", "нанометрах":"нанометре",} 

# n234_gen = {
# 'граммов':"грамма", 'килограммов':"килограмма", 'миллиграммов':"миллиграмма", 'микрограммов':"микрограмма",
# 'тонн':"тонны", 'нанограммов':"нанограмма",  "литров":"литра", "миллилитров":"миллилитра", 
# "лет":"год","десятилетия":"десятилетие","века":"век","тесячелетия":"тысячелетие","месяцах":"месяце",
# "секундах":"секунде", "минутах":"минуте","часах":"часе","днях":"дне","неделях":"неделе",
# "миллисекундах":"миллисекунде", "микросекундах":"микросекунде", "наносекундах":"наносекунде",
# "метрах":"метре", "километрах":"километре","сантиметрах":"сантиметре","миллиметрах":"миллиметре",
# "микрометрах":"микрометре", "нанометрах":"нанометре",} 

# def to_singular(name):
#   name = 
#   return name + 'ы'
def check_one_ending(num):
    if num < 2:
      return 1
    num = str(num)
    if num[-1] == '1':
        if len(num) == 1 or num[-2] != '1':
            chosen = 0
        else:
            chosen = 2
    elif num[-1] in '234':
        if len(num) == 1 or num[-2] != '1':
            chosen = 1
        else:
            chosen = 2
    else:
        chosen = 2
        
    return chosen



def _factor_non_decimal(value):
  """Extras x dividing value such that x is coprime to 2 and 5."""
  result = 1
  factors = sympy.factorint(value)
  for factor, power in six.iteritems(factors):
    if factor not in [2, 5]:
      result *= factor ** power
  return result


def _sample_conversion_decimal(dimension, is_extrapolation):
  """Samples to and from units and values."""
  base_unit, target_unit = random.sample(list(dimension.keys()), 2)
  scale = sympy.Rational(dimension[base_unit]) / dimension[target_unit]
  scale_non_decimal = _factor_non_decimal(sympy.denom(scale))
  entropy = 9 if is_extrapolation else 7
  base_value = number.non_integer_decimal(entropy, signed=False)
  base_value = display.Decimal(base_value.value * scale_non_decimal)
  target_value = display.Decimal(base_value.value * scale)
  return base_value, base_unit, target_value, target_unit


def _conversion_decimal(context, is_train, is_extrapolation):
  """E.g., "How many grams are in 5kg?"."""
  dimension = random.choice(DIMENSIONS)
  while True:
    base_value, base_unit, target_value, target_unit = (
        _sample_conversion_decimal(dimension, is_extrapolation))
    if train_test_split.is_train(base_value) == is_train:
      break


  templates = [
      'Сколько {target_name_skolko} в {base_value} {base_name_v}?',
      'Переведите {base_value} {base_name_perevedi} в {target_name}.',
      'Сконвертируйте {base_value} {base_name_perevedi} в {target_name}.',
  ]
  if base_unit.symbol is not None:
    templates += [
        'Сколько {target_name_skolko} в {base_value}{base_symbol}?',
        'Переведите {base_value}{base_symbol} в {target_name}?',
        'Сконвертируйте {base_value}{base_symbol} в {target_name}.',
    ]
  template = random.choice(templates)

  base_name = base_unit.name
  target_name = target_unit.name

  base_name_skolko = base_unit.name_skolko
  target_name_skolko = target_unit.name_skolko

  # всегда единицы для нецелых
  base_name_perevedi = base_unit.name_perevedi[1]


  base_name_v = base_unit.name_v[check_one_ending(base_value)]

  question = example.question(
      context,
      template,
      base_name=base_name,
      base_name_skolko=base_name_skolko,
      base_name_perevedi=base_name_perevedi,
      base_name_v=base_name_v,
      base_symbol=base_unit.symbol,
      base_value=base_value,
      target_name=target_name,
      target_name_skolko=target_name_skolko)

  return example.Problem(question=question, answer=target_value)


def _conversion_fraction(context, is_train):
  """E.g., "How many grams are in three quarters of a kg?"."""
  dimension = random.choice(DIMENSIONS)

  # Limit probability of giving zero answer.
  allow_zero = random.random() < 0.2

  # Repeat until we find a pair with an integral answer. (Avoids ambiguity with
  # decimals.)
  while True:
    base_unit, target_unit = random.sample(list(dimension.keys()), 2)
    base_value = number.non_integer_rational(2, signed=False)
    if train_test_split.is_train(base_value) != is_train:
      continue
    answer = (base_value * sympy.Rational(dimension[base_unit])
              / sympy.Rational(dimension[target_unit]))
    if (abs(answer) <= 100000
        and sympy.denom(answer) == 1
        and (allow_zero or answer != 0)):
      break

  template, case = random.choice([
      ('Сколько {target_name_skolko} в {base_value} {base_name_fraction}?', 'v'),
      ('Переведите {base_value} {base_name_fraction} в {target_name}?', 'perevedi'),
  ])

  if sympy.denom(base_value) > 20 or random.choice([False, True]):
    base_value_string = base_value  # Will be represented as e.g., 2/3.
  else:
    base_value_string = display.StringNumber(base_value, case=case, gender='fem')  # e.g., two thirds
  # тут всегда единственное у меры

  question = example.question(
      context, template,
      base_name=base_unit.name,
      base_name_fraction=base_unit.name_perevedi[1],
      base_value=base_value_string,
      target_name=target_unit.name,
      target_name_skolko=target_unit.name_skolko)
  return example.Problem(question=question, answer=answer)


def conversion(is_train, is_extrapolation):
  """Conversion question, in decimal or fraction."""
  context = composition.Context()
  # TODO(b/124038528): implement extrapolation for fraction conversions too
  if is_extrapolation or random.choice([False, True]):
    return _conversion_decimal(
        context, is_train=is_train, is_extrapolation=is_extrapolation)
  else:
    return _conversion_fraction(context, is_train=is_train)



def time(is_train):
  """Questions for calculating start, end, or time differences."""
  context = composition.Context()
  start_minutes = random.randint(1, 24*60 - 1)
  while True:
    duration_minutes = random.randint(1, 12*60 - 1)
    if train_test_split.is_train(duration_minutes) == is_train:
      break
  end_minutes = start_minutes + duration_minutes

  def format_24hr(minutes):
    """Format minutes from midnight in 12 hr format."""
    hours = (minutes // 60) % 24
    minutes %= 60
    # am_pm = 'AM' if hours < 12 else 'PM'
    hours = (hours - 1) % 24 + 1
    return '{}:{:02}'.format(hours, minutes)

  start = format_24hr(start_minutes)
  end = format_24hr(end_minutes)

  which_question = random.randint(0, 3)
  if which_question == 0:
    # Question: What is start = end - duration?
    template = random.choice([
        'Сейчас {end}. Сколько времени было {duration} минут назад?',
    ])


    return example.Problem(
        question=example.question(
            context, template, duration=duration_minutes, end=end),
        answer=start)
  elif which_question == 1:
    # Question: What is end = start + duration?
    template = random.choice([
        'Сейчас {start}. Сколько будет через {duration} минут?',
    ])
    return example.Problem(
        question=example.question(
            context, template, duration=duration_minutes, start=start),
        answer=end)
  else:
    # Question: What is duration = end - start?
    template = random.choice([
        'Сколько минут между {start} и {end}?',
    ])
    return example.Problem(
        question=example.question(context, template, start=start, end=end),
        answer=duration_minutes)
