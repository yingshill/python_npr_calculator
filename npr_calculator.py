"""
CS3B, stack implementation
"""
import numpy


class MyStack:
    # Constants
    MAX_CAPACITY = 100000
    DEFAULT_CAPACITY = 10

    # Initializer method
    def __init__(self, default_item, capacity=DEFAULT_CAPACITY):
        # If the capacity is bad, fail right away
        if not self.validate_capacity(capacity):
            raise ValueError("Capacity " + str(capacity) + " is invalid")
        self.capacity = capacity
        self.default_item = default_item

        # Make room in the stack and make sure it's empty to begin with
        self.clear()

    def clear(self):
        # Allocate storage the storage and initialize top of stack
        self.stack = numpy.array([self.default_item for _ in range(self.capacity)])
        self.top_of_stack = 0

    @classmethod
    def validate_capacity(cls, capacity):
        return 0 <= capacity <= cls.MAX_CAPACITY

    def push(self, item_to_push):
        if self.is_full():
            raise OverflowError("Push failed - capacity reached")

        self.stack[self.top_of_stack] = item_to_push
        self.top_of_stack += 1

    def pop(self):
        if self.is_empty():
            raise IndexError("Pop failed - stack is empty")

        self.top_of_stack -= 1
        return self.stack[self.top_of_stack]

    def is_empty(self):
        return self.top_of_stack == 0

    def is_full(self):
        return self.top_of_stack == self.capacity

    def get_capacity(self):
        return self.capacity

    def get_numpy_array(self):
        return self.stack


def mystack_test():
    # Instantiate two empty stacks, one of 50 ints, another of 10 strings
    s1 = MyStack(-1, 50)
    s2 = MyStack("undefined")
    # and one more with bad argument
    try:
        s3 = MyStack(None, -100)
        print("Failed test: expected __init()__ to reject negative capcity but it didn't")
    except Exception as e:
        print("Successful test: handled negative capacity: " + str(e))

    # Confirm the stack capacities
    print("------ Stack Sizes -------\n  s1: {}   s2: {}\n".
          format(s1.get_capacity(), s2.get_capacity()))

    # Pop empty stack
    print("------ Test stack ------\n")
    try:
        s1.pop()
        print("Failed test: expected pop() to raise empty-stack exception but it didn't")
    except Exception as e:
        print("Successful test: handled popping empty s1: " + str(e))

    # Push some items
    s1.push(44)
    s1.push(123)
    s1.push(99)
    s1.push(10)
    s1.push(1000)
    # try to put a square peg into a round hole
    try:
        s1.push("should not be allowed into an int stack")
        print("Failed test: expected push() to reject due to type incompatibility but it didn't")
    except Exception as e:
        print("Successful test: rejected due to type incompatibility: " + str(e))
    try:
        s2.push(444)
        print("Failed test: expected push() to reject due to type incompatibility but it didn't")
    except Exception as e:
        print("Successful test: rejected due to type incompatibility: " + str(e))
    try:
        s1.push(44.4)
        print("Failed test: expected push() to reject due to type incompatibility but it didn't")
    except Exception as e:
        print("Successful test: rejected due to type incompatibility: " + str(e))
    # Push to s2
    s2.push("bank")
    s2.push("-34")
    s2.push("should be okay")
    s2.push("a penny earned")
    s2.push("item #9277")
    s2.push("where am i?")
    s2.push("4")
    s2.push("4")
    s2.push("4")
    s2.push("4")
    try:
        s2.push("This is when stack is full")
        print("Failed test: expected push() to throw exception but it didn't")
    except Exception as e:
        print("Successful test: handled pushing when stack is full: " + str(e))
    print("\n--------- First Stack ---------\n")

    # Pop and inspect the items
    for k in range(0, 10):
        try:
            print("[" + str(s1.pop()) + "]")
        except Exception as e:
            print("Successful test: handled popping empty stack s1: " + str(e))
    print("\n--------- Second Stack ---------\n")
    for k in range(0, 10):
        print("[" + str(s2.pop()) + "]")


class RpnCalculator:

    @staticmethod
    def parse(str):
        token_List = str.split()
        return token_List

    @staticmethod
    def eval_tokens(list_Token):
        capacity_token_list = len(list_Token)
        waiting_stack = MyStack("0", capacity_token_list)
        for char in list_Token:
            if char == "":
                raise ValueError(f"Empty string can't be processed")
            if char == "+" or char == "//" or char == "-" or char == "*":
                if waiting_stack.is_empty():
                    raise ValueError(f"Too many operators")
                else:
                    operand1 = int(waiting_stack.pop())
                    try:
                        operand2 = int(waiting_stack.pop())
                    except IndexError:
                        print(f"Not enough operands in the stack to be operated")
                    # here start to operate based on +, -, //, *
                    if char == "+":
                        new_member = operand1 + operand2
                    elif char == "-":
                        new_member = operand2 - operand1
                    elif char == "//":
                        new_member = operand2 // operand1
                    else:
                        new_member = RpnCalculator.multiply(operand1, operand2)
                    waiting_stack.push(new_member)
            elif char:
                try:
                    waiting_stack.push(int(char))
                except ValueError:
                    print(f"Undefined operators or operands")
        if waiting_stack.is_full():
            raise ValueError("Too many operands waiting to operate while don't have enough operators")
        else:
            return waiting_stack.get_numpy_array()[0]

    @staticmethod
    def multiply(a, b):
        if a == 0 or b == 0:
            return 0
        pos = False
        neg = False
        if (a >= 0 and b >= 0) or (a >= 0 and b >= 0):
            pos = True
        else:
            neg = True
        if neg:
            return -(abs(a) + RpnCalculator.multiply(abs(a), abs(b) - 1))
        else:
            return abs(a) + RpnCalculator.multiply(abs(a), abs(b) - 1)

    @staticmethod
    def eval(rpn_expression):
        # rpn_expression parameter is a string to be evaluated, such as "2 3 +"
        token_List = RpnCalculator.parse(rpn_expression)
        return RpnCalculator.eval_tokens(token_List)


def test_rpn():
  rpn_expressions = ["", "1 1", "1 1 + +", "1 1 fly", "random junk", "1",
                     "1 1 +", "15 5 +", "15 -5 *", "1 1 1 + -",
                     "15 7 1 1 + - // 3 * 2 1 1 + + -", "2 3 4 + *", "1 +"]
  for rpn_expression in rpn_expressions:
    try:
      print("(", rpn_expression, ") = ", RpnCalculator.eval(rpn_expression))
    except Exception as e:
      print("\"", rpn_expression, "\" fails to be evaluated: ", e)

def demo_lost_functionalities():
    """ Since numpy array has the character of Homogeneous elements and fixed length,
    element has to be the same time, and same length, if it's not consistent, the longer element would
    be trimmed to be shorter, so 111 and 11 in numppy array would be trimmed to be 1,
    """
    result = RpnCalculator.eval("1 111 + 11 -")
    print(f"In numpy array, the result is: {result}, while in List, the")
    print(f"result should be 1 + 111 = 112, 112 - 11 = 101")


if __name__ == "__main__":
    # mystack_test()
    # test_rpn()
    demo_lost_functionalities()