from abc import ABC, abstractmethod
import random
import numpy as np
import itertools

class Utils:
    @staticmethod
    def identify_no_order_lines(lines):
        """
        This takes a list of lines and identifies the lines
        contained between the identifiers '<<<' and '>>>' as 
        lines that have no order
        """
        groupings = []
        current_grouping = []
        for line in lines:
            if line.strip() == '<<<':
                if current_grouping:
                    groupings.append(current_grouping)
                    current_grouping = []
            elif line.strip() == '>>>':
                groupings.append(current_grouping)
                current_grouping = []
            else:
                current_grouping.append(line)
        if current_grouping:
            groupings.append(current_grouping)
        # Remove first and last groupings
        if groupings:
            groupings = groupings[1:-1]
        no_order_lines = groupings
        return no_order_lines

class ProblemType(ABC):
    """
    Defines the abstract interface for the concept of a Parson problem
    For example, the user might request a reordering of lines in a file or
    multiple choice questions and answers
    """

    @abstractmethod
    def get_custom_syntax_identifier(self):
        """
        Each implementing class must define 
        the syntax required to identify the question type
        """
        pass

    @abstractmethod
    def generate(self, n_problem):
        """
        Generates n_problems of this type
        """
        pass

    def remove_custom_syntax(self, lines):
        """
        Removes from a list of lines the custom syntax for the lines. Also removes omitted lines through call to method.
        Basically the same for every class
        """
        lines = ProblemType.remove_omitted_lines(lines)
        return [line for line in lines if line.strip() not in self.get_custom_syntax_identifier()]

    def remove_omitted_lines(lines):
        """
        Removes from a list of lines the lines that are omitted
        """
        in_omitted_lines = False
        new_lines = []
        for line in lines:
            if line.strip() == '{@':
                in_omitted_lines = True
            elif not in_omitted_lines:
                new_lines.append(line)
            elif line.strip() == '@}':
                in_omitted_lines = False
        return new_lines


class Generator:
    """
    Agnostic to ProblemType. Just cares that there is some ProblemType, and it
    has a self-defined method called "generate"

    User calls syntax g = Generator(request in ["RQ", "MC", "FB"], lines_from_file)
                      g.Generate(n_problems)
    """
    def __init__(self, request, lines) -> None:
        self.lines = lines
        self.problem_type = ProblemTypeFactory.get_problem_type_from_request(request, self.lines)

    def Generate(self, n_problems=100):
        self.problem_type.generate(n_problems)


class ProblemTypeFactory:
    """
    Return the requested problem type from the 
    """
    @staticmethod
    def get_problem_type_from_request(problem_type, lines):
        if problem_type == 'RQ':
            return ReorderQuestion(lines)
        elif problem_type == 'MC':
            return MultipleChoice(lines)
        elif problem_type == 'FB':
            return FillInBlank(lines)
        else:
            print('Invalid problem type requested. Valid ProblemType(s) are: ', ProblemTypeFactory.get_valid_types())
            quit()
    @staticmethod 
    def get_valid_types():
        return "RQ, MC, or FB"

class ReorderQuestion(ProblemType):
    """
    Each line of code which is not marked as omitted will be
    randomly reorganized
    """
    def __init__(self, lines):
        self.lines = lines
        self.clean_lines = None
        self.no_order_lines = None
        self.answer_list = []
        self.n_problems = None

    def generate(self, n_problems):
        self.n_problems =  n_problems
        self.clean_lines = super().remove_custom_syntax(self.lines)
        self.no_order_lines = Utils.identify_no_order_lines(self.lines)
        self.randomized_lines = self.clean_lines.copy()
        self.solution_list = self.clean_lines.copy()
        for a in range(n_problems):
            random.shuffle(self.randomized_lines)
            self.answer_list.append(self.randomized_lines.copy())
        random.shuffle(self.randomized_lines)
        print(n_problems, " problem of type ReorderQuestion")
        print()
        print("________________________________________________")

    def get_custom_syntax_identifier(self):
        """
        Any additional syntax can be added here as well.
        """
        return ['<<<', '>>>', '{*', '*}']
    
    def print_generated_questions(self):
        for i in range(len(self.answer_list)):
            with open('output.txt', 'a') as f:
                f.write('\nQuestion '+ str(i+1))
                f.write('\nSolution:\n')
                f.write(''.join(self.solution_list))
                f.write('\n\nReordered Lines:\n')
                f.write(''.join(self.answer_list[i]))
                f.write('\nNo Order Lines:\n')
                # Write list line by line
                for lines in self.no_order_lines:
                    for line in lines:
                        f.write(line)
                f.write("\n________________________________________________\n")

class Answer:
    """
    Returned by ProblemType.generate()
    # NOTE: suppose we have an input line randomly selected
    #   (GROUND TRUTH) int main(int argc, char *argv)
    #   (RANDOMLY GENERATED)
    #   Answer.answer_list[0] = int main(argc char *argv ) 
    #   Answer.answer_list[1] = int main(int argc char *argv )
    #   Answer.answer_list[2] = main(int argc, char *argv)
    #   Answer.answer_list[3] = int main(int argc   
    #   Answer.solution_list[0] = int main(int argc, char *argv)
    #
    """
    def __init__(self) -> None:
        self.answer_list = []
        self.solution_list = []


class FillInBlank(ProblemType):
    """
    Each line of code which is not marked as omitted
    will have a fill-in-the-blank question created
    """
    def __init__(self, lines) -> None:
        self.lines = lines
        self.clean_lines = super().remove_custom_syntax(self.lines)
        self.n_problem = len(self.clean_lines)
        self.solution_list = []
        self.answer_list = []
        self.context_before = []
        self.context_after = []

    def generate(self, n_problems):
        for a in range(n_problems):
            b = a % len(self.clean_lines)
            self.solution_list.append(self.clean_lines[b])
            self.answer_list.append(FillInBlank.fill_in_blank_intraline(self.clean_lines[b]))
            # Save all the lines before and after the blank
            self.context_before.append(self.clean_lines[:b])
            self.context_after.append(self.clean_lines[b+1:])
        print(n_problems, " problem of type FillInBlank")
        print()
        print("________________________________________________")


    def fill_in_blank_intraline(line):
        """
        Given a line of code, randomly select a token and replace it with a blank
        """
        tokens = line.split()
        n_tokens = len(tokens)
        selected = np.random.randint(n_tokens)
        tokens[selected] = '[BLANK]'
        return ' '.join(tokens)

    def get_custom_syntax_identifier(self):
        """
        Any additional syntax can be added here as well.
        """
        return ['<<<', '>>>', '{!', '!}']

    def print_generated_questions(self):
        cnt = 1
        for q in range(len(self.answer_list)):
            with open('output.txt', 'a') as f:
                f.write('\nQuestion '+ str(cnt))
                f.write("\nSolution: \n")
                f.write(self.solution_list[q] + "\n")
                # Print context before line by line
                f.write("Context before: \n")
                for line in self.context_before[q]:
                    f.write(line)
                # Print the blank line
                f.write("Blank line: \n")
                f.write(self.answer_list[q] + "\n")
                # Print context after line by line
                f.write("Context after: \n")
                for line in self.context_after[q]:
                    f.write(line)
                f.write("\n________________________________________________\n")
            cnt+=1
