# This file is for housing our unit tests. As well as our end-to-end test scenario.

import pytest
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from source_and_representations import FileData

# Unit tests

## test for get_file_type
def test_get_file_type():
    assert FileData("test_files/test.txt").filetype == "txt"
    assert FileData("test_files/test.py").filetype == "py"
    assert FileData("test_files/test.cpp").filetype == "cpp"
    assert FileData("test_files/test.rb").filetype == "rb"
    assert FileData("test_files/test.java").filetype == "java"


## test for read_file_as_lines
def test_read_file_as_lines():
    assert FileData("test_files/test.txt").lines == [
        "This is a test file.\n",
        "It has two lines.",
    ]
    assert FileData("test_files/test_empty.txt").lines == []
    assert (
        FileData("test_files/test_100lines.txt").lines
        == [
            "this is test file for 100 lines.\n",
        ]
        * 99
        + ["this is test file for 100 lines."]
    )
    assert FileData("test_files/test_no_newlines.txt").lines == [
        "This is a test file that has no newlines. It is a single line."
    ]


## test for remove_comment_lines
def test_remove_comment_lines():
    assert FileData("test_files/test_comment.txt").lines == [
        "This is a test file.\n",
        "It has two lines.\n",
    ]
    assert FileData("test_files/test.py").lines == []


## test for remove_empty_lines
def test_remove_empty_lines():
    assert FileData("test_files/test.cpp").lines == [
        "This is test for empty lines.\n",
        "This is test for empty lines.",
    ]
    assert FileData("test_files/test_empty.txt").lines == []


## test for identify_question_lines
def test_identify_question_lines():
    assert FileData("test_files/testCodeFile.py").question_lines == [
        [
            "def convert_to_binary(num):\n",
            "    if num == 0:\n",
            "        return '0'\n",
            "    binary = ''\n",
            "    while num > 0:\n",
            "        binary = str(num % 2) + binary\n",
            "        num = num // 2\n",
            "    return binary\n",
            "num = int(input('Enter a number: '))\n",
            "binary = convert_to_binary(num)\n",
            'print("The binary representation of", num, "is", binary)\n',
        ],
        [
            "num = int(input('Enter a number: '))\n",
            "binary = convert_to_binary(num)\n",
            "<<<\n",
            "binary = binary + '0'\n",
            "binary = binary + '00'\n",
            ">>>\n",
            'print("The binary representation of", num, "multiplied by 8 is", binary)\n',
        ],
        [
            "{!\n",
            "num = int(input('Enter a number: '))\n",
            "binary = convert_to_binary(num)\n",
            "{@\n",
            "binary = binary + '000'\n",
            "@}\n",
            "hexidecimal = hex(int(binary, 2))\n",
            "!}\n",
            "{$\n",
            'print("The hexidecimal representation of", num, "is", hexidecimal)\n',
            "$}",
        ],
    ]
