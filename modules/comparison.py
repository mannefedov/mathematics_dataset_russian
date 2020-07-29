"""Comparisons, e.g. "is 2 > 3?"."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import functools
import random

# Dependency imports
from mathematics_dataset import example
from mathematics_dataset.sample import number
from mathematics_dataset.sample import ops
from mathematics_dataset.util import composition
from mathematics_dataset.util import display
import numpy as np
from six.moves import range
import sympy


_ENTROPY_TRAIN = (3, 10)
_ENTROPY_INTERPOLATE = (8, 8)
_ENTROPY_EXTRAPOLATE = (12, 12)

_EXTRAPOLATION_EXTRA_COUNT = 2

_PROB_EQUAL = 0.2


def _make_modules(entropy):
  """Returns modules given "difficulty" parameters."""
  sample_args_pure = composition.PreSampleArgs(1, 1, *entropy)
  sample_args_composed = composition.PreSampleArgs(2, 4, *entropy)

  return {
      'pair': functools.partial(pair, sample_args_pure),
      'pair_composed': functools.partial(pair, sample_args_composed),
      'kth_biggest': functools.partial(kth_biggest, sample_args_pure),
      'kth_biggest_composed': functools.partial(
          kth_biggest, sample_args_composed),
      'closest': functools.partial(closest, sample_args_pure),
      'closest_composed': functools.partial(closest, sample_args_composed),
      'sort': functools.partial(sort, sample_args_pure),
      'sort_composed': functools.partial(sort, sample_args_composed),
  }


def train(entropy_fn):
  """Returns dict of training modules."""
  return _make_modules(entropy_fn(_ENTROPY_TRAIN))


def test():
  """Returns dict of testing modules."""
  return _make_modules(_ENTROPY_INTERPOLATE)


def test_extra():
  """Returns dict of extrapolation testing modules."""
  sample_args_pure = composition.PreSampleArgs(1, 1, *_ENTROPY_EXTRAPOLATE)

  def sort_count():
    lower = _sort_count_range(_ENTROPY_TRAIN[1])[1]
    return random.randint(lower + 1, lower + _EXTRAPOLATION_EXTRA_COUNT)
  def closest_count():
    lower = _closest_count_range(_ENTROPY_TRAIN[1])[1]
    return random.randint(lower + 1, lower + _EXTRAPOLATION_EXTRA_COUNT)
  def kth_biggest_more():
    return kth_biggest(sample_args_pure, count=sort_count())
  def sort_more():
    return sort(sample_args_pure, count=sort_count())
  def closest_more():
    return closest(sample_args_pure, count=closest_count())

  return {
      'kth_biggest_more': kth_biggest_more,
      'sort_more': sort_more,
      'closest_more': closest_more,
  }


def _make_comparison_question(context, left, right):
  """Makes a question for comparing two values."""
  if random.choice([False, True]) and sympy.Ne(left.value, right.value):
    # Do question of form: "Which is bigger: a or b?".
    if random.choice([False, True]):
      answer = (
          left.handle if sympy.Gt(left.value, right.value) else right.handle)
      template = random.choice([
          'Что больше: {left} или {right}?',
          'Какое из чисел больше: {left} или {right}?',
      ])
    else:
      answer = (
          left.handle if sympy.Lt(left.value, right.value) else right.handle)
      template = random.choice([
          'Что меньше: {left} или {right}?',
          'Какое число меньше: {left} или {right}?'
      ])
    return example.Problem(
        question=example.question(context, template, left=left, right=right),
        answer=answer)

  comparisons = {
      '<': sympy.Lt,
      '<=': sympy.Le,
      '>': sympy.Gt,
      '>=': sympy.Ge,
      '=': sympy.Eq,
      '!=': sympy.Ne,
  }

  templates = {
      '<': [
          'Правда ли, что {left} ' + ops.LT_SYMBOL + ' {right}?',
          '{left} меньше, чем {right}?',
          'Число {left} меньше числа {right}?',
      ],
      '<=': [
          'Правда ли, что {left} ' + ops.LE_SYMBOL + ' {right}?',
          'Правда ли, что {left} меньше или равно {right}?',
          'Число {left} не больше {right}?',
          'Число {left} не превосходит {right}?',
      ],
      '>': [
          'Правда ли, что {left} ' + ops.GT_SYMBOL + ' {right}?',
          '{left} больше, чем {right}?',
          'Число {left} больше числа {right}?',
      ],
      '>=': [
          'Правда ли, что {left} ' + ops.GE_SYMBOL + ' {right}?',
          'Правда ли, что {left} больше или равно {right}?',
          'Число {left} не меньше {right}?',
      ],
      '=': [
          'Правда ли, что {left} ' + ops.EQ_SYMBOL + ' {right}?',
          'Равны ли {left} и {right}?',
          'Число {left} равно числу {right}?',
          'Одинаковы ли {left} и {right}?',
      ],
      '!=': [
          'Правда ли, что {left} ' + ops.NE_SYMBOL + ' {right}?',
          'Число {left} не равно {right}?',
          'Числа {left} и {right} не равны?',
          'Значения числа {left} и числа {right} отличаются?',
          '{left} и {right} не равны друг другу?',
      ],
  }

  comparison = random.choice(list(comparisons.keys()))
  template = random.choice(templates[comparison])
  question = example.question(context, template, left=left, right=right)
  answer = comparisons[comparison](left.value, right.value)

  return example.Problem(question=question, answer=answer)


def integer_or_rational_or_decimal(entropy):
  if random.choice([False, True]):
    return number.integer_or_decimal(entropy, signed=True)
  else:
    return number.integer_or_rational(entropy, signed=True)


def pair(sample_args, context=None):
  """Compares two numbers, e.g., "is 1/2 < 0.5?"."""
  if context is None:
    context = composition.Context()
  entropy, sample_args = sample_args.peel()

  def integers_close():
    entropy_diff, entropy_left = entropy * np.random.dirichlet([1, 3])
    left = number.integer(entropy_left, True)
    right = left + number.integer(entropy_diff, True)
    return left, right

  def rational_and_integer():
    # Pick rational, and integer close to rational evaluation
    left = number.non_integer_rational(entropy, True)
    right = int(round(left)) + random.randint(-1, 1)
    return left, right

  def independent():
    # Return an independent pair.
    entropy_left, entropy_right = entropy * np.random.dirichlet([1, 1])
    left = integer_or_rational_or_decimal(entropy_left)
    right = integer_or_rational_or_decimal(entropy_right)
    return left, right

  generator = random.choice([integers_close, rational_and_integer, independent])

  left, right = generator()

  # maybe swap for symmetry
  if random.choice([False, True]):
    left, right = right, left
  left, right = context.sample(sample_args, [left, right])

  return _make_comparison_question(context, left, right)


def _entities_to_list(entities):
  entity_dict = {}
  values_template = ''
  for i, entity in enumerate(entities):
    if i > 0:
      values_template += ', '
    entity_name = 'entity_{}'.format(i)
    entity_dict[entity_name] = entity
    values_template += '{' + entity_name + '}'
  return entity_dict, values_template


def _entities_to_choices(entities, answer):
  """Generate a multichoice question template."""
  if len(entities) > 26:
    raise ValueError('Too many choices: {}'.format(len(entities)))

  entity_dict = {}
  choices_template = ''
  answer_choice = None
  for i, entity in enumerate(entities):
    choices_template += '  '
    entity_name = 'entity_{}'.format(i)
    entity_dict[entity_name] = entity
    letter = chr(ord('a') + i)
    choices_template += '({letter}) {{{entity_name}}}'.format(
        letter=letter, entity_name=entity_name)
    if entity is answer:
      assert answer_choice is None
      answer_choice = letter

  assert answer_choice is not None
  return entity_dict, choices_template, answer_choice


def _mark_choice_letters_used(count, context):
  """Marks the choice letters as used."""
  for i in range(count):
    context.mark_used(chr(ord('a') + i))


def _kth_biggest_list_question(context, entities, adjective, answer):
  """Ask for the biggest (or smallest, or second biggest, etc) in a list."""
  entity_dict, values_template = _entities_to_list(entities)

  question = example.question(
      context, 'Какое из значений {adjective} ' + values_template + '?',
      adjective=adjective, **entity_dict)
  return example.Problem(question=question, answer=answer.handle)


def _kth_biggest_multichoice_question(context, entities, adjective, answer):
  """Ask for the biggest (or smallest, or second biggest, etc) of choices."""
  entity_dict, choices_template, answer_choice = _entities_to_choices(
      entities, answer)
  question = example.question(
      context, 'Какое из значений {adjective} ?' + choices_template,
      adjective=adjective, **entity_dict)
  return example.Problem(question=question, answer=answer_choice)


def _entity_sort_key(entity):
  return sympy.default_sort_key(entity.value)


def _sort_count_range(entropy):
  min_ = 3
  return min_, min_ + int(entropy/2)


def _unique_values(entropy, only_integers=False, count=None):
  """Generates unique values."""
  if count is None:
    count = random.randint(*_sort_count_range(entropy))

  if only_integers:
    sampler = functools.partial(number.integer, signed=True)
  else:
    sampler = integer_or_rational_or_decimal

  for _ in range(1000):
    entropies = entropy * np.random.dirichlet(np.ones(count))
    entropies = np.maximum(1, entropies)
    values = [sampler(ent) for ent in entropies]
    if len(sympy.FiniteSet(*values)) == len(values):
      return values
  raise ValueError('Could not generate {} unique values with entropy={}'
                   .format(count, entropy))


def kth_biggest(sample_args, count=None):
  """Asks for the kth biggest value in a list."""
  sample_args = sample_args()
  context = composition.Context()

  entropy, sample_args = sample_args.peel()
  values = _unique_values(entropy, count=count)
  count = len(values)

  display_multichoice = random.choice([False, True])
  if display_multichoice:
    _mark_choice_letters_used(count, context)

  entities = context.sample(sample_args, values)
  sorted_entities = sorted(entities, key=_entity_sort_key)
  ordinal = random.randint(1, count)

  if random.choice([False, True]):
    # Do from biggest.
    answer = sorted_entities[-ordinal]
    adjective = 'наибольшее'
  else:
    # Do from smallest.
    answer = sorted_entities[ordinal - 1]
    adjective = 'наименьшее'

  if ordinal > 1:
    adjective = str(display.StringOrdinal_neu(ordinal)) + ' ' + adjective

  if display_multichoice:
    return _kth_biggest_multichoice_question(
        context=context, entities=entities, adjective=adjective, answer=answer)
  else:
    return _kth_biggest_list_question(
        context=context, entities=entities, adjective=adjective, answer=answer)


def _closest_in_list_question(context, entities, target, adjective, answer):
  """Ask for the closest to a given value in a list."""
  entity_dict, values_template = _entities_to_list(entities)

  question = example.question(
      context,
      'Что из ' + values_template + ' {adjective} к {target}?',
      adjective=adjective, target=target, **entity_dict)
  return example.Problem(question=question, answer=answer.handle)


def _closest_multichoice_question(context, entities, target, adjective, answer):
  """Ask for the closest to a given value in a set of choices."""
  entity_dict, choices_template, answer_choice = _entities_to_choices(
      entities, answer)

  question = example.question(
      context,
      'Что {adjective} к {target}?' + choices_template,
      adjective=adjective, target=target, **entity_dict)
  return example.Problem(question=question, answer=answer_choice)


def _closest_count_range(entropy):
  min_ = 3
  return min_, min_ + int(entropy/3)


def closest(sample_args, count=None):
  """Ask for the closest to a given value in a list."""
  sample_args = sample_args()
  context = composition.Context()

  entropy, sample_args = sample_args.peel()
  if count is None:
    count = random.randint(*_closest_count_range(entropy))

  display_multichoice = random.choice([False, True])
  if display_multichoice:
    _mark_choice_letters_used(count, context)

  entropy_target, entropy_list = entropy * np.random.dirichlet([1, count])
  target = integer_or_rational_or_decimal(entropy_target)

  while True:
    value_entropies = entropy_list * np.random.dirichlet(np.ones(count))
    value_entropies = np.maximum(1, value_entropies)
    values = [integer_or_rational_or_decimal(ent) for ent in value_entropies]
    differences = [abs(sympy.sympify(value) - target) for value in values]
    if len(sympy.FiniteSet(*differences)) == count:  # all differences unique
      break

  target_and_entities = context.sample(sample_args, [target] + values)
  target = target_and_entities[0]
  entities = target_and_entities[1:]

  min_difference = min(differences)
  answer_index = differences.index(min_difference)
  answer = entities[answer_index]
  adjective = random.choice(['ближе всего'])

  if display_multichoice:
    return _closest_multichoice_question(
        context=context, entities=entities, target=target, adjective=adjective,
        answer=answer)
  else:
    return _closest_in_list_question(
        context=context, entities=entities, target=target, adjective=adjective,
        answer=answer)


def sort(sample_args, count=None):
  """Ask to sort numbers in increasing or decreasing order."""
  sample_args = sample_args()
  context = composition.Context()

  entropy, sample_args = sample_args.peel()
  # Sometimes just integers, to allow for more terms in a short space.
  values = _unique_values(
      entropy, only_integers=random.choice([False, True]), count=count)

  entities = context.sample(sample_args, values)

  unsorted_dict, unsorted_template = _entities_to_list(entities)

  ascending = random.choice([False, True])
  templates = [
      'Отсортируйте ' + unsorted_template + ' {direction}.',
      'Расположите ' + unsorted_template + ' {direction}.',
  ]
  if ascending:
    direction = random.choice(['по возрастанию', 'в порядке возрастания',])
  else:
    direction = random.choice(['по убыванию', 'в порядке убывания',])
  template = random.choice(templates)

  sorted_entities = sorted(
      entities, key=_entity_sort_key, reverse=(not ascending))
  answer = ''
  for i, entity in enumerate(sorted_entities):
    if i > 0:
      answer += ', '
    answer += str(entity.handle)

  return example.Problem(
      question=example.question(
          context, template, direction=direction, **unsorted_dict),
      answer=answer)
