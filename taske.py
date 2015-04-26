import numpy as np
import matplotlib.pyplot as plt
import sensitivity
import re

vals = np.linspace(0.0, 0.05, 20)
profit = []
diesel = {'B5':[], 'B30':[], 'B100':[]}

for vi in vals:
	options = {'tax*' : {
		'B5' : 0.2,
		'B30' : 0.05,
		'B100' : vi
	}}
	result = sensitivity.analyze(['PROFIT', 'diesel*'], options)
	profit.append(result['PROFIT'])
	diesel['B5'].append(result['diesel*']['B5'])
	diesel['B30'].append(result['diesel*']['B30'])
	diesel['B100'].append(result['diesel*']['B100'])

plt.figure()

plt.subplot(2, 1, 1)
plt.plot(vals, profit)
plt.title('Variation of B100')
plt.grid(True)

plt.subplot(2, 1, 2)
plt.plot(vals, diesel['B5'])
plt.plot(vals, diesel['B30'])
plt.plot(vals, diesel['B100'])
plt.legend(['B5', 'B30', 'B100'])
plt.grid(True)

plt.show()
