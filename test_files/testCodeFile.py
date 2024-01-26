# Path: testCodeFile.py
# Includes two reordering question groupings, one with a section where order does not matter, one without.
# Includes one fill in the blank question grouping, with lines included that should be omitted from the question.
# Includes one multiple choice question grouping.
{*
# Python code for converting any number to a binary string and prints it
def convert_to_binary(num):
    if num == 0:
        return '0'
    binary = ''
    while num > 0:
        binary = str(num % 2) + binary
        num = num // 2
    return binary

# Prompt the user for a number
num = int(input('Enter a number: '))
# Convert the number to binary
binary = convert_to_binary(num)
# Print the binary string
print("The binary representation of", num, "is", binary)
*}
{*
# Multiply the binary number by 8
num = int(input('Enter a number: '))
binary = convert_to_binary(num)
<<<
binary = binary + '0'
binary = binary + '00'
>>>
print("The binary representation of", num, "multiplied by 8 is", binary)
*}

{!
# Convert a binary number to hexidecimal
num = int(input('Enter a number: '))
binary = convert_to_binary(num)

{@
# Multiply the binary number by 8
binary = binary + '000'
@}

# Convert binary to hexidecimal
hexidecimal = hex(int(binary, 2))
!}

{$
print("The hexidecimal representation of", num, "is", hexidecimal)
$}