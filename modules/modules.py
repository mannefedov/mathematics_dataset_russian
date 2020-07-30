"""The various mathematics modules."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from modules import algebra
from modules import arithmetic
from modules import calculus
from modules import comparison
from modules import measurement
from modules import numbers
from modules import polynomials
from modules import probability
import six


all_ = {
    'algebra': algebra,
    'arithmetic': arithmetic,
    'calculus': calculus,
    'comparison': comparison,
    'measurement': measurement,
    'numbers': numbers,
    'polynomials': polynomials,
    'probability': probability,
}


def train(entropy_fn):
  """Returns dict of training modules."""
  return {
      name: module.train(entropy_fn) for name, module in six.iteritems(all_)
  }


def test():
  """Returns dict of testing modules."""
  return {name: module.test() for name, module in six.iteritems(all_)}


def test_extra():
  """Returns dict of extrapolation testing modules."""
  return {name: module.test_extra() for name, module in six.iteritems(all_)}
