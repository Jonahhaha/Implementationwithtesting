# This file is for housing our unit tests. As well as our end-to-end test scenario.

import pytest
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from multiple_choice import MultipleChoice

# Unit tests

lines = [
    "int main(int argc, char *argv)",
    'print("hello, world! Find me in Perelandra")',
    "for i in range(12, 15::4):",
]

# test for genarate
def test_generate():
    mc = MultipleChoice(lines)
    mc.generate(4)
    assert len(mc.answer_list) == 4

    mc = MultipleChoice(lines)
    mc.generate(1000)
    assert len(mc.answer_list) == 1000

    mc = MultipleChoice(lines)
    mc.generate(0)
    assert mc.answer_list == []

    # TODO: Add test for answer_list to check if the answer is in the list
