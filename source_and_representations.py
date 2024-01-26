# Sources&Representations from our class diagram in the design document. Only part of this subsystem was
# implemented for version v0.1 (see the design document for more details). 

import random


# Class for storing file data
class FileData:
    def __init__(self, filename):
        self.filename = filename
        self.filetype = None
        self.get_file_type()
        self.lines = None
        self.read_file_as_lines()
        self.remove_comment_lines()
        self.remove_empty_lines()
        self.question_lines = []
        self.question_lines_type = []
        self.identify_question_lines()


    # Get file type
    def get_file_type(self):
        self.filetype = self.filename.split('.')[-1]  # Get last part of filename after the last period    

    # Read in a file as a list of lines
    def read_file_as_lines(self):
        with open(self.filename, 'r') as file:
            self.lines = file.readlines()

    # Remove any lines which are comments from a list of lines, based on filetype
    def remove_comment_lines(self):
        if self.filetype == 'py':    # Python
            self.lines = [line for line in self.lines if not line.strip().startswith('#')]
        elif self.filetype == 'java':    # Java
            self.lines = [line for line in self.lines if not line.strip().startswith('//')]
        elif self.filetype == 'js':  # JavaScript
            self.lines = [line for line in self.lines if not line.strip().startswith('//')]
        elif self.filetype == 'html':    # HTML
            self.lines = [line for line in self.lines if not line.strip().startswith('<!--')]
        elif self.filetype == 'css': # CSS
            self.lines = [line for line in self.lines if not line.strip().startswith('//')]
        elif self.filetype == 'txt': # Text
            self.lines = [line for line in self.lines if not line.strip().startswith('//')]
        elif self.filetype == 'cpp': # C++
            self.lines = [line for line in self.lines if not line.strip().startswith('//')]
        else:
            self.lines = self.lines

    # Remove any lines which are empty from a list of lines
    def remove_empty_lines(self):
        self.lines =  [line for line in self.lines if line.strip()]
    
    # Identify lines which are between {* and *} in a list of lines, and return all groupings
    # This {* and *} syntax is used to identify groupings of questions for files where multiple questions will be
    # generated.
    def identify_question_lines(self):
        in_rq_lines = False
        new_lines = []
        for line in self.lines:
            if line.strip() == '{*':
                in_rq_lines = True
            elif line.strip() == '*}':
                in_rq_lines = False
                self.question_lines.append(new_lines)
                self.question_lines_type.append('rq')
                new_lines = []
            elif in_rq_lines:
                new_lines.append(line)

        
        in_mc_lines = False
        new_lines = []
        for line in self.lines:
            if line.strip() == '{$':
                in_mc_lines = True
            elif line.strip() == '$}':
                in_mc_lines = False
                self.question_lines.append(new_lines)
                self.question_lines_type.append('mc')
                new_lines = []
            elif in_mc_lines:
                new_lines.append(line)


        in_fb_lines = False
        new_lines = []
        for line in self.lines:
            if line.strip() == '{!':
                in_fb_lines = True
            elif line.strip() == '!}':
                in_fb_lines = False
                self.question_lines.append(new_lines)
                self.question_lines_type.append('fb')
                new_lines = []
            elif in_fb_lines:
                new_lines.append(line)
   
        
# Create a class for storing generated questions. Questions include the correct order of lines, groupings where order does not matter, and the randomized order of lines
        # Lines should be stored without custom syntax
class ReorderQuestion:
    def __init__(self, lines):
        self.lines = lines
        self.clean_lines = None
        self.remove_custom_syntax()
        self.no_order_lines = None
        self.identify_no_order_lines()
        self.randomized_lines = self.clean_lines.copy()
        random.shuffle(self.randomized_lines)
    
        
    def remove_custom_syntax(self):
        self.clean_lines = [line for line in self.lines if line.strip() not in ['<<<', '>>>', '{*', '*}']]

    # Return all lines between <<< and >>> in a list of lines. May be empty, or may contain multiple groupings of lines.
    # This <<< >>> syntax is used to identify lines where order does not matter. Should start empty, and end empty.
    def identify_no_order_lines(self):
        groupings = []
        current_grouping = []
        for line in self.lines:
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
        self.no_order_lines = groupings
