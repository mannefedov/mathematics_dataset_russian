"""Tests for mathematics_dataset.modules.calculus."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

# Dependency imports
from mathematics_dataset.modules import calculus
import tensorflow as tf


class CalculusTest(tf.test.TestCase):

  def testSampleIntegrand(self):
    # y + 2*x + 3*x**2
    coefficients = [[0, 1], [2, 0], [3, 0]]
    derivative_order = 1
    derivative_axis = 0
    # const + x*y + x**2 + x**3
    expected = [[0, 1], [1, 0], [1, 0]]
    entropy = 4
    result = calculus._sample_integrand(
        coefficients, derivative_order, derivative_axis, entropy)
    result = result[1:, :]  # ignore random constant terms
    self.assertAllEqual(result, expected)


if __name__ == '__main__':
  tf.test.main()
