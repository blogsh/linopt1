import numpy as np
import matplotlib.pyplot as plt
import sensitivity
import re

vals = np.linspace(0.2, 0.4, 100)
profit = []
area = {'Soy':[], 'Cotton':[], 'Sunflower':[]}

for vi in vals:
	options = {'oil_yield*' : {
		'Soy' : 0.178,# * vi,
		'Sunflower' : vi,
		'Cotton' : 0.433,# * vi
	}}
	result = sensitivity.analyze(['PROFIT', 'area*'], options)
	profit.append(result['PROFIT'])
	area['Soy'].append(result['area*']['Soy'])
	area['Cotton'].append(result['area*']['Cotton'])
	area['Sunflower'].append(result['area*']['Sunflower'])

plt.figure()

plt.subplot(2, 1, 1)
plt.plot(vals, profit)
plt.grid(True)
plt.title('Varying oil yield for Sunflower')

plt.subplot(2, 1, 2)
plt.plot(vals, area['Soy'])
plt.plot(vals, area['Cotton'])
plt.plot(vals, area['Sunflower'])
plt.legend(['Soy', 'Cotton', 'Sunflower'])
plt.grid(True)

plt.show()
