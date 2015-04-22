import numpy as np
import matplotlib.pyplot as plt
import sensitivity

if False:
	vals = np.linspace(1600, 10000, 20)
	result = sensitivity.analyze_variable('max_area', vals, ['PROFIT', 'AREA'])

	plt.figure()

	plt.subplot(2, 1, 1)
	plt.plot(vals, result['PROFIT'])
	plt.grid()
	plt.xlabel('Maximum Area')
	plt.ylabel('Profit')

	plt.subplot(2, 1, 2)
	plt.plot(vals, result['AREA'])
	plt.grid()
	plt.xlabel('Maximum Area')
	plt.ylabel('Dual Variable')

	plt.show()

if False:
	vals = np.linspace(5000, 10000, 20)
	result = sensitivity.analyze_variable('max_water', vals, ['PROFIT', 'WATER'])

	plt.figure()

	plt.subplot(2, 1, 1)
	plt.plot(vals, result['PROFIT'])
	plt.grid()
	plt.xlabel('Maximum Water')
	plt.ylabel('Profit')

	plt.subplot(2, 1, 2)
	plt.plot(vals, result['WATER'])
	plt.grid()
	plt.xlabel('Maximum Water')
	plt.ylabel('Dual Variable')

	plt.show()

if True:
	vals = np.linspace(150000, 20000000, 20)
	result = sensitivity.analyze_variable('max_petrol', vals, ['PROFIT', 'PETROL'])

	plt.figure()

	plt.subplot(2, 1, 1)
	plt.plot(vals, result['PROFIT'])
	plt.grid()
	plt.xlabel('Maximum Petrol')
	plt.ylabel('Profit')

	plt.subplot(2, 1, 2)
	plt.plot(vals, result['PETROL'])
	plt.grid()
	plt.xlabel('Maximum Petrol')
	plt.ylabel('Dual Variable')

	plt.show()
