from pulp import LpProblem, LpVariable, lpSum, LpMinimize

PDV=['A','B','C','D']
Usine=['1','2','3']
Cout={ '1': {'A':5,'B':6,'C':6,'D':8},
       '2': {'A':11,'B':9,'C':4,'D':7},
       '3': {'A':12,'B':7,'C':8,'D':5}
           }
PA={   '1': 15000,
       '2': 12000,
       '3': 23000
           }
DA={   'A': 10000,
       'B': 5000,
       'C': 20000,
       'D': 15000
           }

#define problem
prob = LpProblem("Minimisation du cout", LpMinimize)

#decision variable

y = LpVariable.dicts("Usine", [(i,j) for i in PDV for j in Usine], 0)

#define objectif function
prob += lpSum(Cout[j][i] * y[(i,j)] for i in PDV for j in Usine),"Cout totale"

#define contraint
for j in Usine :
    prob += lpSum(y[(i,j)] for i in PDV ) <= PA[j], f"Contrainte_Production_annuelle_{j}"

for i in PDV:
    prob += lpSum(y[(i,j)] for j in Usine) >= DA[i] , f"Contrainte_Demande_annuelle_{i}"

# Résolution du problème
prob.solve()

# Affichage des résultats
if prob.status == 1:
    print("Solution status: Optimal solution found")
elif prob.status == -1:
    print("Solution status: No feasible solution exists")
elif prob.status == 0:
    print("Solution status: Solution is unbounded")
else:
    print("Solution status: Solution status is undefined")

print("Cout Totale :", round(prob.objective.value(), 2),"Dn")

for i in PDV:
    for j in Usine:
        print(f"le cout de transport pour le point de vente {i} Pour l'usine {j}  : {round(y[(i,j)].value(), 2)} ")
