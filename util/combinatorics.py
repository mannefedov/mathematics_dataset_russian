"""Combinatorics utility functions."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import math
import random

# Dependency imports
from six.moves import range
from six.moves import zip


def uniform_positive_integers_with_sum(count, sum_):
  """Returns list of size `count` of integers >= 1, summing to `sum_`."""
  assert sum_ >= 0
  if count > sum_:
    raise ValueError('Cannot find {} numbers >= 1 with sum {}'
                     .format(count, sum_))
  if count == 0:
    return []
  # Select `count - 1` numbers from {1, ..., sum_ - 1}
  separators = random.sample(list(range(1, sum_)), count - 1)
  separators = sorted(separators)
  return [right - left
          for left, right in zip([0] + separators, separators + [sum_])]


def uniform_non_negative_integers_with_sum(count, sum_):
  """Returns list of size `count` of integers >= 0, summing to `sum_`."""
  positive = uniform_positive_integers_with_sum(count, sum_ + count)
  return [i - 1 for i in positive]


def log_number_binary_trees(size):
  """Returns (nat) log of number of binary trees with `size` internal nodes."""
  # This is equal to log of C_size, where C_n is the nth Catalan number.
  assert isinstance(size, int)
  assert size >= 0
  log = 0.0
  for k in range(2, size + 1):
    log += math.log(size + k) - math.log(k)
  return log
