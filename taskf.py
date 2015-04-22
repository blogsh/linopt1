import numpy as np
import matplotlib.pyplot as plt
import sensitivity
import re

vals = np.linspace(0.1, 5, 20)
profit = []
area = {'Soy':[], 'Cotton':[], 'Sunflower':[]}
diesel = {'B5':[], 'B30':[], 'B100':[]}

for vi in vals:
	options = {'water_demand*' : {
		'Soy' : 5 * vi,
		'Sunflower' : 4.2 * vi,
		'Cotton' : 1 * vi
	}}
	result = sensitivity.analyze(['PROFIT', 'area*', 'diesel*'], options)
	profit.append(result['PROFIT'])
	area['Soy'].append(result['area*']['Soy'])
	area['Cotton'].append(result['area*']['Cotton'])
	area['Sunflower'].append(result['area*']['Sunflower'])
	diesel['B5'].append(result['diesel*']['B5'])
	diesel['B30'].append(result['diesel*']['B30'])
	diesel['B100'].append(result['diesel*']['B100'])

plt.figure()

plt.subplot(3, 1, 1)
plt.plot(vals, profit)
plt.grid(True)

plt.subplot(3, 1, 2)
plt.plot(vals, area['Soy'])
plt.plot(vals, area['Cotton'])
plt.plot(vals, area['Sunflower'])
plt.legend(['Soy', 'Cotton', 'Sunflower'])
plt.grid(True)

plt.subplot(3, 1, 3)
plt.plot(vals, diesel['B5'])
plt.plot(vals, diesel['B30'])
plt.plot(vals, diesel['B100'])
plt.legend(['B5', 'B30', 'B100'])
plt.grid(True)

plt.show()
