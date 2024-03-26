from pulp import LpProblem, LpVariable, lpSum, LpMaximize

#define variables
gas=['A', 'B', 'C']

#define atributs
TES={'A':6,
     'B':2,
     'C':4
     }
P={  'A':10,
     'B':25,
     'C':15
     }
PC={ 'A':1000,
     'B':2000,
     'C':1500
     }

#define problem
prob = LpProblem('max pouvoir calorifique', LpMaximize)

#variable de decision
x = LpVariable.dicts('Tout les trois gas', [ i for i in gas],0)

#define objective function
prob += lpSum(PC[i]*x[(i)] for i in gas)

#define contraints
prob += lpSum( TES[i]*x[(i)] for i in gas)<= 10
prob += lpSum( P[i]*x[(i)] for i in gas)<= 50


prob.solve()

# Affichage des résultats
if prob.status == 1:
    print("Optimal solution found")
elif prob.status == -1:
    print("No feasible solution exists")
elif prob.status == 0:
    print("Solution is unbounded")
else:
    print("Solution status is undefined")

print("Cout Totale :", round(prob.objective.value(), 2),"Dn")

for i in gas:
    print(f"Produce {x[i].value()} of Gas {i} \n")
