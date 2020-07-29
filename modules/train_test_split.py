"""Utility for train/test split based on hash value."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import hashlib


def is_train(value):
  """Returns whether `value` should be used in a training question."""
  value_as_string = str(value).encode('utf-8')
  return int(hashlib.md5(value_as_string).hexdigest(), 16) % 2 == 0
