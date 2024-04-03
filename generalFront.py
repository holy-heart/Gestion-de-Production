from pulp import LpProblem, LpVariable, lpSum, LpMaximize, LpMinimize
from flask import Flask, redirect, url_for, render_template, request, session

app= Flask(__name__)
app.secret_key = "jafar" 
@app.route('/', methods=['POST','GET'])
def home():
    if request.method== 'POST':
        variables=[] 
        i=0
        while f"var-{i}" in request.form:
            variables.append(request.form[f"var-{i}"])
            i += 1
        session['variables']=variables
        return redirect(url_for("attribut"))    

    else :
        return render_template('home.html')




#define atributs#define variables#define variables#define variables#define variables#define variables#define variables#define variables#define variables
@app.route('/attribut/', methods=['POST','GET'])
def attribut():
    if request.method== 'POST':
        
        table_attributs=[]
        i=0
        while f"att-{i}" in request.form:
            table_attributs.append(request.form[f"att-{i}"])
            i += 1

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
        op1=request.form['operation_1']
        op2=request.form['operation_2']
        val1=float(request.form['val_1'])
        val2=float(request.form['val_2'])
        j=request.form['contrainte_1']
        if op1 == '<=':
            prob += lpSum( attributs[j][i]*x[i] for i in variables)<= val1
            
        elif op1 =='=':
            prob += lpSum( attributs[j][i]*x[i] for i in variables) == val1
            
        elif op1 == '>=' :
            prob += lpSum( attributs[j][i]*x[i] for i in variables)>= val1
            
        z=request.form['contrainte_2']
        if op2 == '<=':
            prob += lpSum( attributs[z][i]*x[i] for i in variables)<= val2
        elif op2 =='=':
            prob += lpSum( attributs[z][i]*x[i] for i in variables) == val2
        elif op2 == '>=' :
            prob += lpSum( attributs[z][i]*x[i] for i in variables)>= val2

        prob.solve()
        # Affichage des résultats
        # Nouvelle partie pour afficher les résultats
        if prob.status == 1:
            statue="Solution optimale trouvée"
        elif prob.status == -1:
            statue="Aucune solution réalisable n'existe"
        elif prob.status == 0:
            statue="La solution est non bornée"
        else:
            statue="Le statut de la solution est indéfini"
        session["statue"]=statue
        session['cout']="Coût Total :", round(prob.objective.value(), 2), "Dn"
        for i in variables:
            session[f"var {i}"]=f"La variable '{i} : {x[i].value()} "


        return redirect(url_for('solution'))
    else :
        table_attributs=session.get('table_attributs')

        return render_template('choice.html', table_attributs=table_attributs)
                

@app.route('/solution', methods=['POST','GET'])
def solution():
    statue=session.get('statue')
    cout=session.get('cout')
    variables=session.get('variables') 
    result=[]
    for i in variables:
        result.append(session.get(f"var {i}"))
    return render_template('sol.html',result=result,statue=statue,cout=cout)
    


if __name__=="__main__":
    app.run(debug=True)