{!
#import a file
filename = input('Enter a filename: ')

# Sort lines of the file alphabetically
lines = Utils.get_lines_from_file(filename)
lines.sort()
#Randomize lines
random.shuffle(lines)
#Print lines
for line in lines:
    print(line)
!}