"""Tests for mathematics_dataset.sample.linear_system."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import random

# Dependency imports
from absl.testing import absltest
from absl.testing import parameterized
from sample import linear_system
from six.moves import range
import sympy


class ExpressionWithValueTest(parameterized.TestCase):

  def testIsTrivialIn(self):
    self.assertEqual(linear_system._is_trivial_in([[1]], 0), False)
    self.assertEqual(linear_system._is_trivial_in([[1, 2], [3, 4]], 0), False)
    self.assertEqual(linear_system._is_trivial_in([[1, 2], [3, 0]], 0), True)
    self.assertEqual(linear_system._is_trivial_in([[1, 2], [3, 0]], 1), False)
    self.assertEqual(linear_system._is_trivial_in([[1, 2], [0, 3]], 0), False)
    self.assertEqual(linear_system._is_trivial_in([[1, 2], [0, 3]], 1), True)

  @parameterized.parameters([1, 2, 3])
  def testLinearSystem(self, degree):
    for _ in range(100):  # test a few times
      target = [random.randint(-100, 100) for _ in range(degree)]
      variables = [sympy.Symbol(chr(ord('a') + i)) for i in range(degree)]
      system = linear_system.linear_system(
          variables=variables,
          solutions=target,
          entropy=10.0)
      solved = sympy.solve(system, variables)
      solved = [solved[symbol] for symbol in variables]
      self.assertEqual(target, solved)


if __name__ == '__main__':
  absltest.main()
