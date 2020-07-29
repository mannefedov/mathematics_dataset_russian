"""Settings for generation."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import string

MAX_QUESTION_LENGTH = 300
MAX_ANSWER_LENGTH = 30
QUESTION_CHARS = (
    ['', ' '] + list(string.ascii_letters + string.digits + string.punctuation + "ЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮйцукенгшщзхъфывапролджэячсмитьбю"))
EMPTY_INDEX = QUESTION_CHARS.index('')
NUM_INDICES = len(QUESTION_CHARS)
CHAR_TO_INDEX = {char: index for index, char in enumerate(QUESTION_CHARS)}
INDEX_TO_CHAR = {index: char for index, char in enumerate(QUESTION_CHARS)}

