from pulp import LpProblem, LpVariable, lpSum, LpMaximize, LpMinimize
from flask import Flask, redirect, url_for, render_template, request, session

app= Flask(__name__)
app.secret_key = "jafar" 
@app.route('/', methods=['POST','GET'])
def home():
    if request.method== 'POST':
        variables=[] 
        variables.append(request.form["one"])  
        variables.append(request.form["two"]) 
        variables.append(request.form["three"]) 
        session['variables']=variables
        return redirect(url_for("attribut"))    

    else :
        return render_template('home.html')




#define atributs#define variables#define variables#define variables#define variables#define variables#define variables#define variables#define variables
@app.route('/attribut/', methods=['POST','GET'])
def attribut():
    if request.method== 'POST':
        
        table_attributs=[]
        table_attributs.append(request.form["one"])  
        table_attributs.append(request.form["two"]) 
        table_attributs.append(request.form["three"])

        session['table_attributs']=table_attributs
        return redirect(url_for("valeurs"))  
    else :
        return render_template('attributs.html')        


@app.route('/valeurs/', methods=['POST','GET'])
def valeurs():
    if request.method== 'POST': 
        variables=session.get('variables')  
        table_attributs=session.get('table_attributs')
        attributs={}
        for index, i in enumerate(table_attributs):
            att={}
            for jndex, j in enumerate(variables):
                att[j]=float(request.form[f"var_{index}_{jndex}"])
            attributs[i]=att
        session['attributs']=attributs

        return redirect(url_for("choice"))  
    else :
        variables=session.get('variables')  
        table_attributs=session.get('table_attributs')
        v=len(variables)
        a=len(table_attributs)
        return render_template('valeurs.html', variables=variables, table_attributs=table_attributs, v=v, a=a)
    










#define variables#define variables#define variables#define variables#define variables#define variables#define variables#define variables#define variables
    
    



@app.route('/choice', methods=['POST','GET'])
def choice():
    if request.method== 'POST':
        variables=session.get('variables')  
        attributs=session.get('attributs')
        obj = request.form.get('objectif')
        if obj=="Minimisation" :
            prob = LpProblem("Probleme", LpMinimize) 
        else:    
            prob = LpProblem("Probleme", LpMaximize)
        ######################################################################################################################
        #variable de decision
        x = LpVariable.dicts('variables', [ i for i in variables],0)
        #choisir quelle attribut est en decision
        j=request.form['decision']
        #define objective function
        prob += lpSum(attributs[j][i]*x[i] for i in variables), "Objective Function"
        #define contraints
        op=request.form['operation']
        val1=float(request.form['val_1'])
        val2=float(request.form['val_2'])
        j=request.form['contrainte']
        if op == '<=':
            prob += lpSum( attributs[j][i]*x[i] for i in variables)<= val1
            prob += lpSum( attributs["Prix"][i]*x[i] for i in variables)<= val2
        elif op =='=':
            prob += lpSum( attributs[j][i]*x[i] for i in variables) == val1
            prob += lpSum( attributs['Prix'][i]*x[i] for i in variables) == val2
        elif op == '>=' :
            prob += lpSum( attributs[j][i]*x[i] for i in variables)>= val1
            prob += lpSum( attributs['Prix'][i]*x[i] for i in variables)>= val2

        prob.solve()
        # Affichage des résultats
        # Nouvelle partie pour afficher les résultats
        if prob.status == 1:
            print("Solution optimale trouvée")
        elif prob.status == -1:
            print("Aucune solution réalisable n'existe")
        elif prob.status == 0:
            print("La solution est non bornée")
        else:
            print("Le statut de la solution est indéfini")

        print("Coût Total :", round(prob.objective.value(), 2), "Dn")

        for i in variables:
            print(f"Produire {x[i].value()} de Gaz {i}")


        return redirect(url_for('solution'))
    else :
        table_attributs=session.get('table_attributs')

        return render_template('choice.html', table_attributs=table_attributs)
                

@app.route('/solution', methods=['POST','GET'])
def solution():
    return f"<h1> JE SUIS LE GOAT </h1>"
    


if __name__=="__main__":
    app.run(debug=True)