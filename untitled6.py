from pulp import *
#list
FOODS=['CHICKEN', 'MILK', 'EGGS', 'MEAT']

CUSTOMER = ['antoine', 'fred', 'seb', 'romain', 'adrien']
FACILITY = ['Fac1','Fac2','Fac3']

#dictionnairy
demande = {'antoine': 80,
           'fred': 270,
           'deb': 250,
           'romain' : 160,
           'adrien' : 180
           }
actcoast={ 'Fac1': 1000,
           'Fac2': 1000,
           'Fac2': 1000
           }
maximum ={ 'Fac1': 500,
           'Fac2': 500,
           'Fac2': 500
           }

transp = {'Fac1': {'antoine' : 4, 'fred':5, 'seb':6, 'romain':8, 'adrien':10},
          'Fac2': {'antoine' : 6, 'fred':4, 'seb':3, 'romain':5, 'adrien':8},
          'Fac3': {'antoine' : 9, 'fred':7, 'seb':4, 'romain':3, 'adrien':4}
          }
##init class
prob = LpProblem("facilityLocation", LpMinimize)

##define variables
x=LpVariable.dicts("use location", FACILITY, 0,1, LpBinary)
y=LpVariable.dicts("Service", [(i,j) for i in CUSTOMER
                                     for j in FACILITY],
                   0)

food = LpVariable("FOOD", FOODS,0)



prob += lpSum(actcoast[j]*x[j] for j in FACILITY)
prob += lpSum(transp[j][i]*y[(i,j)] for j in FACILITY for i in CUSTOMER)