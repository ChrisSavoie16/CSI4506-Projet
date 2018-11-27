# IMPLEMENTATION OF AC3 ALGORITHM

import queue
from CSP import *

#THE MAIN AC-3 ALGORITHM
def AC3(csp):
	q = queue.Queue()

	for arc in csp.constraints:
		q.put(arc)

	i = 0
	while not q.empty():
		(Xi, Xj) = q.get()

		i = i + 1 

		if Revise(csp, Xi, Xj):
			if len(csp.values[Xi]) == 0:
				return False

			for Xk in (csp.peers[Xi] - set(Xj)):
				q.put((Xk, Xi))

	#display(csp.values)
	return True 



#WORKING OF THE REVISE ALGORITHM
def Revise(csp, Xi, Xj):
	revised = False
	values = set(csp.values[Xi])

	for x in values:
		if not isconsistent(csp, x, Xi, Xj):
			csp.values[Xi] = csp.values[Xi].replace(x, '')
			revised = True 

	return revised 



#CHECKS IF THE GIVEN ASSIGNMENT IS CONSISTENT
def isconsistent(csp, x, Xi, Xj):
	for y in csp.values[Xj]:
		if Xj in csp.peers[Xi] and y!=x:
			return True

	return False


