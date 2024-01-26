import itertools
import random
import numpy as np


from class_types import ProblemType, Answer
from class_types import Utils
from source_and_representations import FileData

class MultipleChoice(ProblemType):
    """
    Each line of code which is not marked as omitted
    will have a multiple choice problem created
    """
    def __init__(self, lines) -> None:
        self.lines = lines
        self.clean_lines = super().remove_custom_syntax(self.lines)
        #print(self.clean_lines)
        self.no_order_lines = None
        self.no_order_lines = Utils.identify_no_order_lines(self.lines)
        self.answer_list = []

    def generate(self, n_problems):
        n_lines = len(self.clean_lines)
        i = 0
        while i < n_problems:
            selected = np.random.randint(n_lines)
            before_lines = self.clean_lines[:selected]
            #print("Before lines: ", before_lines)
            after_lines = self.clean_lines[selected:]
            #print("After lines: ", after_lines)
            answer = self.generate_mc_intraline(self.clean_lines[selected])
            if answer is not None:  
                answer_options_str = "A. " + answer.answer_list[0] + "B. " + answer.answer_list[1] + "C. " + answer.answer_list[2] + "D. " + answer.answer_list[3]
                answer_list = []
                for l in before_lines:
                    answer_list.append(l)
                answer_list.append(answer_options_str)
                for l in after_lines:
                    answer_list.append(l)
                # print("Answer options string ", answer_options_str)    
                #print(before_lines.append(answer_options_str))
                #print("Before l)
                # tmp.append(after_lines)
                # answer.solution_list = []
                answer.solution_list = self.clean_lines
                # answer.answer_list = []
                answer.answer_list = answer_list
                self.answer_list.append(answer)
                i += 1

        print(n_problems, " problem of type MultipleChoice")
        print()
        print("________________________________________________")

    def generate_mc_intraline(self, line):
        #print("Generating for line: ", line)
        # Create a single answer object
        a = Answer()
        a.solution_list = []
        a.answer_list = []
        a.solution_list.append(line)

        # $TODO$ This is not robust to if the line only has one space
        # Possible solution is to brea further at say ','
        split_space = line.split(' ') # Currently only support split at space and comma
        n_items = len(split_space)
        if n_items > 2:
            split_space_idx = list(range(n_items)) # 0 1 2 3 4 5 6 7 ...
            for i in range(3):
                to_remove_sz = len(split_space_idx)
                to_remove = np.random.randint(to_remove_sz)
                cnt = 0
                str_tmp = ''
                for item in split_space:
                    if cnt != to_remove:
                        str_tmp += " " + item
                    cnt += 1
                split_space_idx.pop(to_remove)
                a.answer_list.append(str_tmp)
            a.answer_list.append(line)
            random.shuffle(a.answer_list)
            return a
        else:
            return None

    def get_custom_syntax_identifier(self):
        """
        Any additional syntax can be added here as well.
        """
        return ['<<<', '>>>', '{$', '$}']

    def print_generated_questions(self):
        cnt = 1
        for q in self.answer_list:
            with open('output.txt', 'a') as f:
                f.write('\nQuestion '+ str(cnt))
                print("\nPossible Answers:", file=f)
                for qq in q.answer_list:
                    print(qq, file=f)
                print('________________________________________________', file=f)
            cnt += 1