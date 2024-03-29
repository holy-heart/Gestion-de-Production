from pulp import LpProblem, LpVariable, lpSum, LpMaximize, LpMinimize
from flask import Flask, redirect, url_for, render_template, request

app= Flask(__name__)

@app.route('/', methods=['POST','GET'])
def home():
    if request.method== 'POST':
        variables=[]
        for i in range(request.form['compteur1']):
            var=request.form[i] 
            variables.append(var)
            attributs={}
        return redirect(url_for("home2", variables, attributs, att=0))    

    else :
        return render_template('home.html', i=0)




#define atributs#define variables#define variables#define variables#define variables#define variables#define variables#define variables#define variables
@app.route('/home2/<att>', methods=['POST','GET'])
def home2(variables, attributs, att):
    if request.method== 'POST':
        for i in range(request.form['compteur2']):
            var=request.form[i] 
            attributs.append(var)
            att={}
            for j in len(variables):
                att[j]=float(request.form['compteur2'])
            attributs[var]=att
            n+=1

        #define problem#define problem  #define problem  #define problem  #define problem  #define problem  #define problem  #define problem  #define problem  #define problem      
        var=input(f"veuillez choisir entre une solution de 'minimisation' ou de 'maximisation' (Maximisation par defalt) : ")
        if var=="minimisation" :
            prob = LpProblem("Probleme", LpMinimize) 
        else:    
            prob = LpProblem("Probleme", LpMaximize)
        ######################################################################################################################
        #variable de decision
        x = LpVariable.dicts('variables', [ i for i in variables],0)
        return redirect(url_for("choice", variables, attributs, x, prob))  
    else :
        return render_template('home2.html', variables, i=0)
    










#define variables#define variables#define variables#define variables#define variables#define variables#define variables#define variables#define variables
    
    



@app.route('/choice', methods=['POST','GET'])
def choice(variables, attributs, x, prob):
    #choisir quelle attribut est en decision
    j=input('quelle atribut voulez vous traiter (tapez le correctement) : ')
    #define objective function
    prob += lpSum(attributs[j][i]*x[i] for i in variables), "Objective Function"
    #define contraints
    print('maintenant vous devez definir les contraintes : \n')
    t=False
    while t==False:
        j=input("veuillez entrer le nom de l'attribut (tapez le correctement) ('stop' pour arreter) : ")
        
        if j == "stop":
            t=True
        else:
            op=input(f" choisissez entr | <= | = | >= | : ")
            var=float(input(f"veuillez entrer la valuer corespondante : "))
            if op == '<=':
                prob += lpSum( attributs[j][i]*x[i] for i in variables)<= var
            elif op =='=':
                prob += lpSum( attributs[j][i]*x[i] for i in variables) == var
            elif op == '>=' :
                prob += lpSum( attributs[j][i]*x[i] for i in variables)>= var
                

@app.route('/solution', methods=['POST','GET'])
def sol(prob, variables, x):
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

    for i in variables:
        print(f"Produce {x[i].value()} of Gas {i} \n")