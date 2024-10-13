# Author: maxanthem
# Created on: 24.11.2023
# Updated on: 25.09.2024
#
# Premium / Deductible Simulator (Swiss Health Insurance)
# Plots the actual health expenses vs health cost
#
# Language: English and German plots included
# --------------------------------------------------------

# %% IMPORTING MODULES
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colormaps
from matplotlib import rc
rc('font',**{'family':'Helvetica Light', 'size': 12}) # Just for a nice font
# ignore if you don't have the font

# %%
#  PARAMETERS
# Feel free to add the values of your insurance there:
# - names (string)
# - deductibles (numpy array)
# - premiums (numpy array, corresponding order with deductibles)


# # Swisscare HMIE
# name = 'Swisscare HMIE'
# deductibles = np.array((300,500,1000,1500,2000,2500))
# premiums = np.array((115,88,70,59,49,38))

# Visana
name = 'Visana'
deductibles = np.array((300,500,1000,1500,2000,2500))
premiums = np.array((473.65,462.75,435.45,408.25,380.95,353.75))

# COMPLETE YOUR INSURANCE PREMIUMS HERE
# name = "..."
# deductibles = np.array((300,500,1000,1500,2000,2500))
# premiums = np.array((...))




# Co-payment parameters (shouldn't change)
co_payment_rate = 0.1   # Co-payment rate
co_payment_max = 700        # Maximum co-payment

# SIMULATION
max_cost = 10000 # Maximum cost to display
n_points = 1000
costs = np.linspace(0, max_cost, n_points)
expenses = np.zeros((len(premiums),len(costs)))

# When the cost is higher than the deductible, the expense only increases
# by 10% of the cost until 700 CHF is reached with these 10%.
# After this, the expense doesn't increase anymore.

for i in range(len(premiums)):
    for j in range(len(costs)):
        if costs[j] < deductibles[i]:
            expense = costs[j] + premiums[i] * 12 # months/year
        else:
            expense = deductibles[i] + premiums[i] * 12
            addedCost = co_payment_rate * (costs[j] - deductibles[i]) 
            if addedCost < co_payment_max:
                expense += addedCost
            else:
                expense += co_payment_max
        expenses[i,j] = expense

break_even_point = None
best_plan_1 = np.argmin(expenses[:,0]) # Best plan for 0 cost
best_plan_2 = None
for i in range(len(costs)):
    # if expenseArray[0, i] <= expenseArray[-1, i]:
    best_plan_current = np.argmin(expenses[:,i])
    if best_plan_current != best_plan_1:
        break_even_point = i
        best_plan_2 = best_plan_current
        break

# PLOTTING
cmap = colormaps.get_cmap('coolwarm')
colors = cmap(np.linspace(0, 1, len(premiums)))
linestyles = ['-', '--', '-.', ':', (0, (3, 1, 1, 1)), (0, (5, 5)), (0, (1, 1))]

# English version (German version below)
plt.figure(1)
for i in range(len(premiums)):
    label = f'Deductible {deductibles[i]}'
    if i == best_plan_1:
        label += ' (Best for 0 cost)'
    if i == best_plan_2:
        label += ' (Best for more cost)'
    plt.plot(costs, expenses[i], color=colors[i],
             linestyle=linestyles[i % len(linestyles)],label=label)
    
if break_even_point is not None:
    plt.plot(costs[break_even_point], expenses[best_plan_1, break_even_point], 'ko',
             label= f'Break-even point: {costs[break_even_point]:.0f} CHF')
    plt.plot([costs[break_even_point], costs[break_even_point]], 
             [0, expenses[best_plan_1, break_even_point]], 'k--')

plt.title('Comparing different basic health insurance plans'+
          "\nInsurance name: "+name)
plt.xlabel('Health Cost [CHF]')
plt.ylabel('Actual Expenses [CHF]')
plt.xlim([0, max_cost])
plt.ylim(0)
plt.legend()
plt.grid()

plt.savefig('out/health_cost_EN_'+name+'.png') # Saving the figure

# %% 
# German version
plt.figure(2)
for i in range(len(premiums)):
    label = f'Franchise {deductibles[i]}'
    if i == best_plan_1:
        label += ' (Beste für 0 Kosten)'
    if i == best_plan_2:
        label += ' (Beste für mehr Kosten)'
    plt.plot(costs, expenses[i], color=colors[i],
             linestyle=linestyles[i % len(linestyles)],label=label)
    
if break_even_point is not None:
    plt.plot(costs[break_even_point], expenses[best_plan_1, break_even_point], 'ko',
             label= f'Break-even Punkt: {costs[break_even_point]:.0f} CHF')
    plt.plot([costs[break_even_point], costs[break_even_point]], 
             [0, expenses[best_plan_1, break_even_point]], 'k--')

plt.title('Vergleich verschiedener Versicherungspolice'+
            "\nVersicherungsname: "+name)
plt.xlabel('Gesundheitskosten [CHF]')
plt.ylabel('Effektive Kosten [CHF]')
plt.xlim([0, max_cost])
plt.ylim(0)
plt.legend()
plt.grid()

plt.savefig('out/health_cost_DE_'+name+'.png') # Saving the figure
plt.show()
