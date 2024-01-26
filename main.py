# This file is not a part of the design document, but is included here for debugging purposes.
# For actual testing, (i.e. unit testing), the program will be run from testing.py.
import source_and_representations as sar
from multiple_choice import MultipleChoice
import class_types as ct

# filename = "./test_files/" + "testCodeFile.py"
# Prompt user for filename
filename = input("Enter the name of the file to be used for generating questions: ")
filename = "./test_files/" + filename
fileData = sar.FileData(filename)
# Find amount of question groupings in the file
questionGroups = len(fileData.question_lines_type)
# Print the amount of question groupings
print("There is " + str(questionGroups) + " question grouping(s) detected in the file.")
# Print the amount of questions of each grouping type
print("There is " + str(fileData.question_lines_type.count('rq')) + " reordering question grouping(s).")
print("There is " + str(fileData.question_lines_type.count('fb')) + " fill in the blank question grouping(s).")
print("There is " + str(fileData.question_lines_type.count('mc')) + " multiple choice question grouping(s).")
# Prompt the user for how many questions they want to generate for each grouping
numQuestionsReorder = int(input("Enter the number of questions you want to generate for each reordering grouping: "))
numQuestionsFillInBlank = int(input("Enter the number of questions you want to generate for each fill in the blank grouping: "))
numQuestionsMultChoice = int(input("Enter the number of questions you want to generate for each multiple choice grouping: "))

with open('output.txt', 'w') as f:
    f.write("There is " + str(questionGroups) + " question grouping(s) detected in the file.\n")
    f.write("There is " + str(fileData.question_lines_type.count('rq')) + " reordering question grouping(s).\n")
    f.write("There is " + str(fileData.question_lines_type.count('fb')) + " fill in the blank question grouping(s).\n")
    f.write("There is " + str(fileData.question_lines_type.count('mc')) + " multiple choice question grouping(s).\n")
    f.write("There will be " + str(numQuestionsReorder) + " questions generated for each reordering grouping.\n")
    f.write("There will be " + str(numQuestionsFillInBlank) + " questions generated for each fill in the blank grouping.\n")
    f.write("There will be " + str(numQuestionsMultChoice) + " questions generated for each multiple choice grouping.\n")
    ("________________________________________________\n")
for a in range(len(fileData.question_lines_type)):
    with open('output.txt', 'a') as f:
        f.write("________________________________________________\n",)
        f.write("Question Generation for Grouping Number " + str(a+1) + " of type " + fileData.question_lines_type[a] + ":" + "\n")
        f.write("\n")
    if fileData.question_lines_type[a] == 'rq':
        rq = ct.ReorderQuestion(fileData.question_lines[a])
        rq.generate(numQuestionsReorder)
        rq.print_generated_questions()
    elif fileData.question_lines_type[a] == 'fb':
        fb = ct.FillInBlank(fileData.question_lines[a])
        fb.generate(numQuestionsFillInBlank)
        fb.print_generated_questions()
    elif fileData.question_lines_type[a] == 'mc':
        mc = MultipleChoice(fileData.question_lines[a])
        mc.generate(numQuestionsMultChoice)
        mc.print_generated_questions()