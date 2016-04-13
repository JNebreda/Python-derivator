# Writes a function that takes a parse tree for a mathematical expression
# and calculates the derivative of the expression with respect to some variable.

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


class BinaryTree:
    def __init__(self,rootObj):
        self.root = rootObj
        self.leftChild = None
        self.rightChild = None

    # Inserts a tree as the left node. If given a string, 
    # it creates a tree and puts it in the root      
    def insertLeft(self,newNode):
    	if isinstance(newNode, basestring):
    		newNode = BinaryTree(newNode)

        if self.leftChild == None:
            self.leftChild = newNode
        else:
            newNode.leftChild = self.leftChild
            self.leftChild = newNode

    # Inserts a tree as the left node. If given a string, 
    # it creates a tree and puts it in the root      
    def insertRight(self,newNode):
    	if isinstance(newNode, basestring):
    		newNode = BinaryTree(newNode)

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

	# Simplifies the full tree
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


    # Simplifies the operation in the root of the tree
    def simplifyOperation(self):

    	if not self.isLeafNode():
    		op = self.root
    		left = self.leftChild
    		right = self.rightChild

    		if right.root == '0':
    			if op in '+-':
    				self.replaceTree(left)
    			elif op == '*':
    				self.replaceTree(BinaryTree('0'))
    			elif op == '/':
    				raise ValueError('Division by zero')
    			else:
    				raise TypeError('Wrong operation')

    		elif left.root == '0':
				if op == '+':
					self.replaceTree(right)
				elif op in '*/':
					self.replaceTree(BinaryTree('0'))

    		elif right.root == '1' and op == '*':
				self.replaceTree(left)

    		elif left.root == '1' and op == '*':
				self.replaceTree(right)    		

		

def printexp(tree):
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
    fplist = fpexp.split()
    pStack = Stack()
    eTree = BinaryTree('')
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

	if not isinstance(tree,BinaryTree):
	 	raise TypeError('Derivative takes as first argument an object of the BinaryTree class')

	if type(variable) is not str:
	 	raise TypeError('Derivative takes as second argument a string')

	currVal = tree.root
	leftChild = tree.leftChild
	rightChild = tree.rightChild

	if leftChild and rightChild:
		leftDer = derivative(leftChild, variable)
		rightDer = derivative(rightChild, variable)

		if currVal == '+' or currVal == '-':
			derTree = BinaryTree(currVal)
			derTree.insertLeft(leftDer)
			derTree.insertRight(rightDer)

		elif currVal == '*':
			derTree = BinaryTree('+')

			firstTerm = BinaryTree('*')
			firstTerm.insertLeft(leftDer)
			firstTerm.insertRight(rightChild)

			secondTerm = BinaryTree('*')
			secondTerm.insertLeft(leftChild)
			secondTerm.insertRight(rightDer)

			derTree.insertLeft(firstTerm)
			derTree.insertRight(secondTerm)


		elif currVal == '/':
			if rightChild.root != '0':
				derTree = BinaryTree('/')

				numerator = BinaryTree('-')
				numFirstTerm = BinaryTree('*')
				numFirstTerm.insertLeft(leftDer)
				numFirstTerm.insertRight(rightChild)
				numSecTerm = BinaryTree('*')				
				numSecTerm.insertLeft(leftChild)
				numSecTerm.insertRight(rightDer)
				numerator.insertLeft(numFirstTerm)
				numerator.insertRight(numSecTerm)
								
				denominator = BinaryTree('*')
				denominator.insertLeft(rightChild)
				denominator.insertRight(rightChild)

				derTree.insertLeft(numerator)
				derTree.insertRight(denominator)

		 	else:
		 		raise ValueError("Division by zero")

	elif currVal == variable:
		derTree = BinaryTree('1')

	else: 
		derTree = BinaryTree('0')

	derTree.simplifyTree()
	return derTree


# Tests
fun = '( 2 * x )'
var = 'x'
tree = buildParseTree(fun)
der = derivative(tree, var)
print("The derivative of:\n\t%s\nwith respect to %s is:\n\t%s\n" % (fun, var, printexp(der)))

fun = "( ( x + y ) * x )"
var = 'x'
tree = buildParseTree(fun)
der = derivative(tree, var)
print("The derivative of:\n\t%s\nwith respect to %s is:\n\t%s\n" % (fun, var, printexp(der)))

fun = "( ( x + y ) * x )"
var = 'y'
tree = buildParseTree(fun)
der = derivative(tree, var)
print("The derivative of:\n\t%s\nwith respect to %s is:\n\t%s\n" % (fun, var, printexp(der)))

fun = "( ( x + y ) / x )"
var = 'x'
tree = buildParseTree(fun)
der = derivative(tree, var)
print("The derivative of:\n\t%s\nwith respect to %s is:\n\t%s\n" % (fun, var, printexp(der)))

fun = "( 2 + 2 )"
tree = buildParseTree(fun)
print(printexp(tree))


