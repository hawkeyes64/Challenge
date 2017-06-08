##################################################################################################################
# Author:   Jesmigel A. Cantos
# Date Created: 11/04/17
#
# Application Name: IR_MineSweeper
# Purpose: To provide a glimpse of coding and software engineering expertise,
#   application structure is based upon the object oriented design-pattern/method called
#   MVC, short for Model - View - Controller. This is commonly used in modern web development
#   framework such as Django (python web framework), Java Enterprise Beans and Phalcon PHP web framework
##################################################################################################################
import re  # Regular expressions
import sys  # sys.exit() to gracefully exit the app if recognized error occurs


##################################################################################################################
# Model Class: model_MineField
# Purpose: Define the structure of a minefield object
##################################################################################################################
class model_MineField:
    # NM[0] - line index
    # NM[1] - column index
    NM = []
    NM_FIELD = []
    MineField = {}

    # In case initialization of array size is not called upon
    #   declaration of MineField object, default size would be 1x1 2d array
    def __init__(self):
        self.NM = [0, 0]
        self.NM_FIELD = ['.']
        self.MineField = {len(self.NM_FIELD): self.NM_FIELD[self.NM[1]]}

    # Set the field line by line
    def setField(self, inputN, inputValueList):
        # self.NM_FIELD = self.convertToList(inputValueList)
        self.MineField.update({inputN: inputValueList})

    # Extract the contents of the MineField Object
    def printField(self):
        print("NM = " + str(self.NM))

        # Display a proper table
        for ctr in range(0, int(len(self.MineField))):
            print(self.MineField[ctr])


##################################################################################################################
# Controller Class: controller_OperateData
# Purpose:
#   This class is responsible for interrogating the standard input to promote quality assurance
#   After passing quality assurance, stored data will then be interrogated and analysed
#   in order to achieve desired output as stated by the assignment requirements
##################################################################################################################
class controller_OperateData:
    # Implement input validation as well as regex character replace to standard 0 for character '.'
    @staticmethod
    def processInputRow(inputRow, inputCol):
        if not bool(re.compile(r'^[.|*]+$').match(inputRow)):
            sys.exit(-1)
        newList = str(inputRow).replace('.', '0')
        if len(newList) != inputCol:
            sys.exit(-1)
        return newList

    # Implement regex replace to above and below rows with respect to character '*' at position [0, 0]
    @staticmethod
    def processTopBottomRow(inputMineField, inputN, span, lookupM):
        # [-1,-1],  [0,-1], [1,-1]
        # [-1,0 ],  [0,0 ], [1,0 ] # not needed
        # [-1,1 ],  [0,1 ], [1,1 ]

        newField = model_MineField.MineField = inputMineField

        for ctr_row in [-1, 1]:
            for ctr_col in lookupM:
                try:
                    row_str = newField[inputN + ctr_row]
                    row_chr = row_str[span[0] + lookupM[ctr_col]: span[1] + lookupM[ctr_col]]
                    if str(row_chr).isdigit():
                        newField[inputN + ctr_row] = row_str[:span[0] + lookupM[ctr_col]] + str(int(row_chr) + 1) + \
                                                     row_str[span[1] + lookupM[ctr_col]:]
                except KeyError:
                    continue
        return newField


##################################################################################################################
# View Class: view_initializeObjects
# Purpose: Normally the "Front end" for user interaction. With respect to the task at hand,
#   This will call objects meant for input, storage, and processing of data
##################################################################################################################
class view_initializeObjects:
    mineField = model_MineField
    processData = controller_OperateData

    def __init__(self):
        self.setMineField()
        self.analyzeData()

    def setMineField(self):

        try:
            self.mineField.NM = str(input()).split(' ')
            self.mineField.NM[0] = int(self.mineField.NM[0])
            self.mineField.NM[1] = int(self.mineField.NM[1])

            if len(self.mineField.NM) != 2 or self.mineField.NM[0] < 1 or \
                    self.mineField.NM[0] > 99 or self.mineField.NM[1] < 1 or self.mineField.NM[1] > 99:
                # Uncomment below to return error message and exit
                sys.exit("Input error: Does not follow 0<N,M<100")

                # Uncomment below to return generic exit error code
                # sys.exit(-1)

            for line_ctr in range(0, int(self.mineField.NM[0])):
                self.mineField.MineField.update(
                    {line_ctr: self.processData.processInputRow(input(), self.mineField.NM[1])})

        except (ValueError, IndexError, SyntaxError) as e:
            # Uncomment below to return error message and exit
            sys.exit("Input error: " + str(e))

            # Uncomment below to return generic error code and exit
            # sys.exit(-1)
        # print(self.mineField.MineField)

    def analyzeData(self):
        lookup_array = [-1, 0, 1]

        # lambda function to increment integers surrounding char '*'
        l = lambda x: str(int(x.group(0)) + 1)
        p = re.compile("\*")

        for keys in self.mineField.MineField:
            # Look ahead regex char replace
            t = re.sub("(?<=\*)[0-8]", l, self.mineField.MineField[keys])

            # Look behind regex char replace
            t = re.sub("[0-8](?=\*)", l, t)

            # Horizontal analysis
            self.mineField.MineField.update({keys: t})

            # Vertical + horizontal analysis
            for m in p.finditer(self.mineField.MineField[keys]):
                self.mineField.MineField = self.processData.processTopBottomRow(
                    self.mineField.MineField, keys, m.span(), lookup_array)

        for key in self.mineField.MineField.keys():
            print(self.mineField.MineField[key])
            # return self.mineField


##################################################################################################################
# Function: Main
#   Responsible for calling different type of "views"
#   This acts as the singleton design pattern where in theory, other design views are going to be
#   called upon based on the input. This can be combined with other design patterns such as either of the
#   following:
#       factory, abstract factory, and command handler
###################################################################################################################
def Main():
    view_initializeObjects()


##################################################################################################################
# Function: testClass
# 	This will act as the "Test class"
#   In theory, the minesweeper field can be analyzed by means of regular expressions
#   If data is joined into a single string, 4 regex lines can be made for look ahead and look behind logic
##################################################################################################################
def testClass():
    # Method 1
    InitMine = model_MineField
    InitMine.NM = [3, 5]
    InitMine.MineField = {0: '**...', 1: '.....', 2: '*....'}
    model_MineField.printField(InitMine)

    # Method 2
    str = '**1000000000000'
    pattern = '(?<=\*).'
    regexp = re.compile(pattern)
    print(str)
    for m in regexp.finditer(str):
        print(m.span())
        print(str[m.span()[0]: m.span()[1]])
        # print(sys.version)

##################################################################################################################
# Function: call
#   Immediately invoke functions either Main() or testClass() or both
##################################################################################################################
def call():
    # testClass()
    Main()


call()