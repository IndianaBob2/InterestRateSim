from random import *
import matplotlib.pyplot as plt
def optimal_money_borrowed(r,e_cash):
    profit = 0
    money_borrowed = 100
    for t in range(1000):
        value = randint(0,1)
        if value:
            new_money_borrowed = money_borrowed*1.01
        else:
            new_money_borrowed = money_borrowed*0.99
        new_profit = production(new_money_borrowed+e_cash)+e_cash-new_money_borrowed*(r)
        if new_profit > profit:
            profit = new_profit
            money_borrowed = new_money_borrowed
    return money_borrowed
def gradient_search(r,e_cash):
    money_borrowed = 100
    while True:
        g_1 = profit_f(money_borrowed+1,e_cash,r)
        if g_1 < 0:
            g_1 = 0
        g_2 = profit_f(money_borrowed-1,e_cash,r)
        if g_2 < 0:
            g_2 = 0
        gradient = (g_1-g_2)/2
        if gradient > 100:
            gradient = 100
        elif gradient < -100:
            gradient = -100        
        money_borrowed += gradient*10
        if gradient < 0:
            gradient = gradient*(-1)
        if gradient < 0.001:
            break
    return money_borrowed
def production(cash):
    return (cash)**0.5
def profit_f(borrowed,e_cash,r):
    return production(borrowed+e_cash)+e_cash-borrowed*r
def equilibrium(e_cash,i_cash):
    r = 0.1
    t = 0
    while True:
        demand = optimal_money_borrowed(r,e_cash)
        supply = i_cash
        if supply > demand:
            r = r*0.99
        elif supply < demand:
            r = r*1.01
        t += 1
        diff = supply-demand
        if diff < 0:
            diff = diff*(-1)
        if diff < 10:
            break
    return r
def evolution(e_cash,i_cash,investment):
    e_cash_list = []
    i_cash_list = []
    r_list = []
    mrk_list = []
    # Avec ré-investissement de l'entrepreneur
    if investment:
        for t in range(30):
            #Calcul retour marginal capital
            mrk = (production(i_cash+e_cash+0.1)-production(i_cash+e_cash-0.1))/0.2
            # Calcul taux d'intérêt
            r = equilibrium2(i_cash,e_cash)
            # Calcul profit (avant intérêt)
            e_cash = production(i_cash+e_cash)+i_cash+e_cash
            # Deduction taux d'intérêt
            interest = i_cash*(1+r)
            i_cash = interest
            e_cash -= interest
            # Retourne informations
            e_cash_list.append(e_cash)
            i_cash_list.append(i_cash)
            r_list.append(r)
            mrk_list.append(mrk)
    # Sans ré-investissement de l'entrepreneur
    else:
        for t in range(30):
            #Calcul retour marginal capital
            mrk = (production(i_cash+0.1)-production(i_cash-0.1))/0.2
            # Calcul taux d'intérêt
            r = equilibrium2(i_cash,0)
            # Calcul profit (avant intérêt)
            e_cash += production(i_cash)+i_cash
            # Deduction taux d'intérêt
            interest = i_cash*(1+r)
            i_cash = interest
            e_cash -= interest
            # Retourne informations
            e_cash_list.append(e_cash)
            i_cash_list.append(i_cash)
            r_list.append(r)
            mrk_list.append(mrk)
    return [e_cash_list,i_cash_list]
def equilibrium2(i_cash,e_cash):
    a = 0.01
    r = 0.1
    while True:
        supply_demand = i_cash-gradient_search(r,e_cash)
        if ((supply_demand > 0) and (a > 0)) or ((supply_demand < 0) and (a < 0)):
            a = a*(-0.5)
        r += a
        if supply_demand < 0:
            supply_demand = supply_demand*(-1)
        if supply_demand < 0.1:
            break
    return r
        
def printing(lists,increment,a=0):
    x_list = []
    for x in range(len(lists[0])):
        x_list.append(increment*x+a)
    fig, ax = plt.subplots()
    for liste in lists:
        ax.plot(x_list,liste)
    plt.show()
def supply_curve(i_cash,e_cash):
    r = 0.001
    liste = []
    for x in range(500):
        supply_demand = i_cash-gradient_search(r,e_cash)
        if supply_demand < 0:
            supply_demand = supply_demand*(-1)
        liste.append(supply_demand)
        r += 0.001
    return liste
a = evolution(0,100,1)
b = evolution(250,500,1)
printing(a+b,1)
