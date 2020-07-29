"""Containers for "[example] problems" (i.e., question/answer) pairs."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import collections

from mathematics_dataset.util import composition


def question(context, template, **kwargs):
  """Makes a question, using the given context and template.

  The format is similar to that for python's `format` function, for example:

  ```
  question(context, 'What is {} plus {p} over {q}?', 2, p=3, q=4)
  ```

  The main difference between this and the standard python formatting is that
  this understands `Entity`s in the arguments, and will do appropriate expansion
  of text and prefixing of their descriptions.

  Arguments:
    context: Instance of `composition.Context`, for extracting entities needed
        for describing the problem.
    template: A string, like "Calculate the value of {exp}.".
    **kwargs: A dictionary mapping arguments to values, e.g.,
        `{'exp': sympy.Add(2, 3, evaluate=False)}`.

  Returns:
    String.
  """
  assert isinstance(context, composition.Context)
  assert isinstance(template, str)
  prefix, kwargs = composition.expand_entities(context, **kwargs)
  if prefix:
    prefix += ' '
  return prefix + template.format(**kwargs)


Problem = collections.namedtuple('Problem', ('question', 'answer'))


