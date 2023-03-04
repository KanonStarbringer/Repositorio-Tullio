from gurobipy import *

import pandas as pd

# Read excel sheets and turn them into lists
basic_info = pd.read_excel('IP_dataset.xlsx', 'Basic Information')
cities = range(len(basic_info['City']))
markets = range(len(basic_info['Market']))

city_info = pd.read_excel('IP_dataset.xlsx', 'City\'s Information')
operating_costs = city_info['Operating Cost']
capacities = city_info['Capacity']

market_info = pd.read_excel('IP_dataset.xlsx', 'Market\'s Information')
demands = market_info['Demand']

shipping_info = pd.read_excel('IP_dataset.xlsx', 'Shipping Cost', index_col=0)
shipping_costs = []
for i in shipping_info.index:
    shipping_costs.append(list(shipping_info.loc[i]))
    
eg2 = Model("eg2")    # build a new model

# add variables as a list
x = []
for j in cities:
    x.append(eg2.addVar(lb = 0, vtype = GRB.BINARY, name = "x" + str(j+1)))
    
y = []
for i in markets:
    y.append([])
    for j in cities:
        y[i].append(eg2.addVar(lb = 0, vtype = GRB.CONTINUOUS, name = "y" + str(i+1) + str(j+1)))
    
# setting the objective function
eg2.setObjective(
    quicksum(operating_costs[j] * x[j] for j in cities)
    + quicksum(quicksum(shipping_costs[i][j] * y[i][j] for j in cities) for i in markets)
    , GRB.MINIMIZE)

# add constraints and name them
eg2.addConstrs((quicksum(y[i][j] for i in markets) <= capacities[j] * x[j]
               for j in cities), "productCapacity")

eg2.addConstrs((quicksum(y[i][j] for j in cities) >= demands[i]
               for i in markets), "demand_fulfillment")

eg2.optimize()

print("Result:")

for j in cities:
    print(x[j].varName, '=', x[j].x)
#head of the result table
print("\tMarket1\tMarket2\tMarket3\tMarket4\tMarket5")

for j in cities:
    # mark which product is printed now
    print("City" + str(j+1), "\t", end="")
    for i in markets:
        #print values of each kind of product
        if len(str(y[i][j].x)) < 7:
            print(y[i][j].x, "\t", end="")
        else:
            print(y[i][j].x, "", end="")
    print("")   #use for change line
    
print("z* =", eg2.objVal)    #print objective value


    


