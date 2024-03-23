from pulp import *

#init class
LpProblem('max pouvoir calorifique', LpMaximize)

#define variables
A=LpVariable('Gas A',lowBound=0,cat='Continuous')
B=LpVariable('Gas B',lowBound=0,cat='Continuous')
C=LpVariable('Gas C',lowBound=0,cat='Continuous')

#define objective function
model += 1000*A + 2000*B + 1500*C

#define contraints
model += 6 * A + 2 * B + 4 * C <= 10
model += 10 * A + 25 * B + 15 * C <= 50

#solve model
model.solve()
print("Produce {} Gas A".format(A.varValue))
print("Produce {} Gas A".format(B.varValue))