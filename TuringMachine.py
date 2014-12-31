from collections import deque
import csv

class TuringMachine:
    def __init__(self, initTape = (0,), initHead = 0, radix = 1):
        """Initializes a Turing machine

        initalTape -- Any iterable object containing values less than the radix
        radix -- The base of the numeral system being used
        """
        self._cells = deque(initTape);
        self._head = initHead

    def right(self, num = 1):
        """Moves the head right the specified number of cells"""
        self._move(num)

    def left(self, num = 1):
        """Moves the head left the specified number of cells"""
        self._move(-num)

    def _move(self, num):
        """Moves the head generically. Extends the tape if needed"""
        self._head += num
        if self._head < 0:
            self._cells.extendleft([0]*abs(self._head))
            self._head = 0
        elif self._head >= len(self._cells):
            self._cells.extend([0]*(self._head-len(self._cells)+1))

    def read(self):
        """Reads the number on the current cell"""
        return self._cells[self._head]

    def write(self, val):
        """Writes a number to the current cell"""
        self._cells[self._head] = val

    def runProgram(self, program, step_limit = 3000, debug = False):
        """Runs a program, given in the form of a dictionary.

        The program defines actions (as dict values) to take in particular
        circumstances (as dict keys). Keys should be 2-tuples where the first
        member is the current state, and the second member is the value on the
        current cell. Dict values should be 3-tuples where the first member
        specifies the action to take by "L" (for left) or "R" (for right) or "W"
        (for write), the second member is the parameter given to that action,
        and the third member is the new program state.
        """
        state = 1
        step = 0
        if debug: log = [{"state":state,
                          "head":self._head,
                          "tape":tuple(self._cells)}]
        while (state, self.read()) in program and step < step_limit:
            tup = program[state, self.read()]
            if tup[0] == "R":
                self.right(tup[1])
            elif tup[0] == "L":
                self.left(tup[1])
            elif tup[0] == "W":
                self.write(tup[1])
            state = tup[2]
            if debug: log.append({"state":state,
                                  "head":self._head,
                                  "tape":tuple(self._cells)})
            step += 1
        if debug: return log

    def __str__(self):
        return ' '.join(str(s) for s in self._cells) + '\n' \
               + ' ' \
               * (sum( #add up the length of values at or left of head
                   len(str(self._cells[i]))
                   for i in range(0,self._head+1))
                  + self._head - 1) \ #add tape spaces, move back onto head val
               + 'H'

def readMinimalProgram(filename):
    """Reads a text file defining a program with minimal operations.

    Each instruction is a space-delimited 4-tuple on its own line. The first
    member is the current state. The second member is the current cell's value.
    The third member is L (to move left one cell), R (to move right one cell),
    1 (to write 1 in the cell), or 0 (to write 0 in the cell). The fourth
    member is the new program state.

    Output is compatible with the TuringMachine.runProgram method.
    """
    prog = dict()
    with open(filename) as txt:
        rdr = csv.reader(txt, delimiter = ' ')
        for r in rdr:
            if len(r) == 0: continue
            prog[int(r[0]),
                 int(r[1])] = (r[2] if r[2] in ("R","L") else "W",
                               0 if r[2]=='0' else 1,
                               int(r[3]))
    return prog

def generateUnaryMachine(iterable):
    """Produces a machine with given inputs as unary values.

    A unary input of value n is represented as a string of n+1 ones. Inputs are
    separated by a single zero.
    """
    tape = list()
    for val in iterable:
        tape.extend([1]*(val+1))
        tape.append(0)
    return TuringMachine(tape)
