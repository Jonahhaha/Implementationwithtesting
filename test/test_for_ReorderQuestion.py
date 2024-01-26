import pytest
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from source_and_representations import ReorderQuestion
from source_and_representations import FileData


def test_remove_custom_syntax():
    assert ReorderQuestion(["<<<", "test"]).clean_lines == ["test"]
    assert ReorderQuestion([">>>", "test"]).clean_lines == ["test"]
    assert ReorderQuestion(["{*", "test"]).clean_lines == ["test"]
    assert ReorderQuestion(["*}", "test"]).clean_lines == ["test"]


def test_identify_question_lines():

    assert ReorderQuestion(
        [
            "<<<",
            ">>>",
            "test/n",
            "<<<",
            "binary = binary + '0'/n",
            "binary = binary + '00'/n",
            ">>>/n",
            "test",
            "<<<",
            ">>>",
        ]
    ).no_order_lines == [
        ["test/n"],
        ["binary = binary + '0'/n", "binary = binary + '00'/n", ">>>/n", "test"],
    ]
