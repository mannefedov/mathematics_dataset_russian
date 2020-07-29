"""Example of how to write generated questions to text files.

Given an output directory, this will create the following subdirectories:

*   train-easy
*   train-medium
*   train-hard
*   interpolate
*   extrapolate

and populate each of these directories with a text file for each of the module,
where the text file contains lines alternating between the question and the
answer.

Passing --train_split=False will create a single output directory 'train' for
training data.
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os

# Dependency imports
from absl import app
from absl import flags
from absl import logging
from mathematics_dataset import generate
import six
from six.moves import range

FLAGS = flags.FLAGS

flags.DEFINE_string('output_dir', None, 'Where to write output text')
flags.DEFINE_boolean('train_split', False,
                     'Whether to split training data by difficulty')
flags.mark_flag_as_required('output_dir')


def main(unused_argv):
  generate.init_modules(FLAGS.train_split)

  output_dir = os.path.expanduser(FLAGS.output_dir)
  if os.path.exists(output_dir):
    logging.fatal('output dir %s already exists', output_dir)
  logging.info('Writing to %s', output_dir)
  os.makedirs(output_dir)

  for regime, flat_modules in six.iteritems(generate.filtered_modules):
    regime_dir = os.path.join(output_dir, regime)
    os.mkdir(regime_dir)
    per_module = generate.counts[regime]
    for module_name, module in six.iteritems(flat_modules):
      path = os.path.join(regime_dir, module_name + '.txt')
      with open(path, 'w') as text_file:
        for _ in range(per_module):
          try:
            problem, _ = generate.sample_from_module(module)
          except Exception as e:
            print(e)
            continue
          text_file.write(str(problem.question) + '\n')
          text_file.write(str(problem.answer) + '\n')
      logging.info('Written %s', path)


if __name__ == '__main__':
  app.run(main)
