""" Parse and simplify an arithmetic expression and calculate its derivative."""
import operator

class Stack:
     def __init__(self):
         self.items = []

     def isEmpty(self):
         return self.items == []

     def push(self, item):
         self.items.append(item)

     def pop(self):
         return self.items.pop()

     def peek(self):
         return self.items[len(self.items)-1]

     def size(self):
         return len(self.items)


class ArithmeticTree:	
    """Create a binary tree containing an arithmetic expression."""

    def __init__(self,rootObj):
        self.root = rootObj
        self.leftChild = None
        self.rightChild = None

    # Insert a tree as the left node. If given a string, 
    # create a tree and puts it in the root      
    def insertLeft(self,newNode):
    	if isinstance(newNode, basestring):
    		newNode = ArithmeticTree(newNode)

        if self.leftChild == None:
            self.leftChild = newNode
        else:
            newNode.leftChild = self.leftChild
            self.leftChild = newNode

    # Insert a tree as the left node. If given a string, 
    # it create a tree and puts it in the root      
    def insertRight(self,newNode):
    	if isinstance(newNode, basestring):
    		newNode = ArithmeticTree(newNode)

        if self.rightChild == None:
            self.rightChild = newNode
        else:
            newNode.rightChild = self.rightChild
            self.rightChild = newNode

    def replaceTree(self, newTree):
        self.root = newTree.root
        self.leftChild = newTree.leftChild
        self.rightChild = newTree.rightChild

    def isLeafNode(self):
    	return not self.leftChild and not self.rightChild        

	# Simplify the full tree
    def simplifyTree(self):
    	root = self.root
    	left = self.leftChild
    	right = self.rightChild

    	if not self.isLeafNode():

			# Simplify right node
			if not right.isLeafNode():
				right.simplifyTree()

			# Simplify left node
			if not left.isLeafNode():
				left.simplifyTree()

    	# Simplify root
    	self.simplifyOperation()


    # Simplify the operation in the root of the tree
    def simplifyOperation(self):
    	if not self.isLeafNode():
    		op = self.root
    		left = self.leftChild
    		right = self.rightChild

    		if is_number(right.root) and is_number(left.root):
    			ops = { "+": operator.add, "-": operator.sub, "*": operator.mul, "/": operator.div }
    			result = ops[op](float(left.root),float(right.root))
    			self.replaceTree(ArithmeticTree(str(result)))

    		elif right.root in '0.0':
    			if op in '+-':
    				self.replaceTree(left)
    			elif op == '*':
    				self.replaceTree(ArithmeticTree('0'))
    			elif op == '/':
    				raise ZeroDivisionError('Division by zero')
    			else:
    				raise TypeError('Wrong operation')

    		elif left.root in '0.0':
				if op == '+':
					self.replaceTree(right)
				if op == '-':
					right.root = '-'+right.root
					self.replaceTree(right)
				elif op in '*/':
					self.replaceTree(ArithmeticTree('0'))

    		elif right.root in '1.0' and op == '*':
				self.replaceTree(left)

    		elif left.root in '1.0' and op == '*':
				self.replaceTree(right)    		

		

def printexp(tree):
	"""Return the string representation of an ArithmeticTree."""

	if not tree:
		return None
	else:
		currVal = tree.root
		leftChild = tree.leftChild
		rightChild = tree.rightChild
  
  		if leftChild and rightChild:
	   		sVal = '( %s %s %s )' % (printexp(leftChild), currVal, printexp(rightChild))
	   	else:
	   		sVal = currVal
  
	  	return sVal    

def buildParseTree(fpexp):
    """Create an ArithmeticTree from a string."""

    fplist = fpexp.split()
    pStack = Stack()
    eTree = ArithmeticTree('')
    pStack.push(eTree)
    currentTree = eTree
    for i in fplist:
        if i == '(':
            currentTree.insertLeft('')
            pStack.push(currentTree)
            currentTree = currentTree.leftChild

        elif i not in ['+', '-', '*', '/', ')']:
            currentTree.root = i
    	    parent = pStack.pop()
            currentTree = parent

        elif i in ['+', '-', '*', '/']:
            currentTree.root = i 
            currentTree.insertRight('')
            pStack.push(currentTree)
            currentTree = currentTree.rightChild

        elif i == ')':
        	if currentTree.root not in '+-*/':
        		raise SyntaxError('Expression has wrong syntax')

	    	currentTree = pStack.pop()

        else:
            raise ValueError

    eTree.simplifyTree()
    return eTree

def derivative(tree,variable):
	"""Derivate an arithmetic expression stored in an ArithmeticTree."""

	if not isinstance(tree,ArithmeticTree):
	 	raise TypeError('Derivative takes as first argument an object of the ArithmeticTree class')

	if type(variable) is not str:
	 	raise TypeError('Derivative takes as second argument a string')

	currVal = tree.root
	leftChild = tree.leftChild
	rightChild = tree.rightChild

	if leftChild and rightChild:
		leftDer = derivative(leftChild, variable)
		rightDer = derivative(rightChild, variable)

		if currVal == '+' or currVal == '-':
			derTree = ArithmeticTree(currVal)
			derTree.insertLeft(leftDer)
			derTree.insertRight(rightDer)

		elif currVal == '*':
			derTree = ArithmeticTree('+')

			firstTerm = ArithmeticTree('*')
			firstTerm.insertLeft(leftDer)
			firstTerm.insertRight(rightChild)

			secondTerm = ArithmeticTree('*')
			secondTerm.insertLeft(leftChild)
			secondTerm.insertRight(rightDer)

			derTree.insertLeft(firstTerm)
			derTree.insertRight(secondTerm)


		elif currVal == '/':
			if rightChild.root != '0':
				derTree = ArithmeticTree('/')

				numerator = ArithmeticTree('-')
				numFirstTerm = ArithmeticTree('*')
				numFirstTerm.insertLeft(leftDer)
				numFirstTerm.insertRight(rightChild)
				numSecTerm = ArithmeticTree('*')				
				numSecTerm.insertLeft(leftChild)
				numSecTerm.insertRight(rightDer)
				numerator.insertLeft(numFirstTerm)
				numerator.insertRight(numSecTerm)
								
				denominator = ArithmeticTree('*')
				denominator.insertLeft(rightChild)
				denominator.insertRight(rightChild)

				derTree.insertLeft(numerator)
				derTree.insertRight(denominator)

		 	else:
		 		raise ZeroDivisionError("Division by zero")

	elif currVal == variable:
		derTree = ArithmeticTree('1')

	else: 
		derTree = ArithmeticTree('0')

	derTree.simplifyTree()
	return derTree

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False	


if __name__ == "__main__":
	# Tests
	print("Simplification tests")

	fun = '( x + 0 )'
	tree = buildParseTree(fun)
	print("The function: %s gets simplified to: %s" % (fun, printexp(tree)))

	fun = '( x - 0 )'
	tree = buildParseTree(fun)
	print("The function: %s gets simplified to: %s" % (fun, printexp(tree)))

	fun = '( x * 0 )'
	tree = buildParseTree(fun)
	print("The function: %s gets simplified to: %s" % (fun, printexp(tree)))

	fun = '( x / 0 )'
	try:
		tree = buildParseTree(fun)
	except ZeroDivisionError:
		print("The function: %s throws a ZeroDivisionError message" % fun)

	fun = '( 0 + x )'
	tree = buildParseTree(fun)
	print("The function: %s gets simplified to: %s" % (fun, printexp(tree)))
	
	fun = '( 0 - x )'
	tree = buildParseTree(fun)
	print("The function: %s gets simplified to: %s" % (fun, printexp(tree)))

	fun = '( 0 * x )'
	tree = buildParseTree(fun)
	print("The function: %s gets simplified to: %s" % (fun, printexp(tree)))

	fun = '( 0 / x )'
	tree = buildParseTree(fun)
	print("The function: %s gets simplified to: %s" % (fun, printexp(tree)))

	fun = '( 1 + 2 )'
	tree = buildParseTree(fun)
	print("The function: %s gets simplified to: %s" % (fun, printexp(tree)))

	fun = '( 3 / 2 )'
	tree = buildParseTree(fun)
	print("The function: %s gets simplified to: %s" % (fun, printexp(tree)))

	fun = '( 3 / 0 )'
	try:
		tree = buildParseTree(fun)
	except ZeroDivisionError:
		print("The function: %s throws a ZeroDivisionError message" % fun)

	fun = '( ( x + y ) * ( 3 - 3 ) )'
	tree = buildParseTree(fun)
	print("The function: %s gets simplified to: %s" % (fun, printexp(tree)))

	fun = '( ( x + y ) * ( z + ( w * 1 ) ) )'
	tree = buildParseTree(fun)
	print("The function: %s gets simplified to: %s" % (fun, printexp(tree)))


	print("\nDerivation tests")

	fun = '( 2 * x )'
	var = 'x'
	tree = buildParseTree(fun)
	der = derivative(tree, var)
	print("The derivative of:%s with respect to %s is: %s\n" % (fun, var, printexp(der)))

	fun = "( ( x + y ) * x )"
	var = 'x'
	tree = buildParseTree(fun)
	der = derivative(tree, var)
	print("The derivative of: %s with respect to %s is: %s\n" % (fun, var, printexp(der)))

	fun = "( ( x + y ) * x )"
	var = 'y'
	tree = buildParseTree(fun)
	der = derivative(tree, var)
	print("The derivative of: %s with respect to %s is: %s\n" % (fun, var, printexp(der)))

	fun = "( ( x + y ) / x )"
	var = 'x'
	tree = buildParseTree(fun)
	der = derivative(tree, var)
	print("The derivative of: %s with respect to %s is: %s\n" % (fun, var, printexp(der)))

	fun = "( ( 2 * x ) + ( 3 + x ) )"
	var = 'x'
	tree = buildParseTree(fun)
	der = derivative(tree,var)
	print("The derivative of: %s with respect to %s is: %s\n" % (fun, var, printexp(der)))

