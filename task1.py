import numpy as np
import matplotlib.pyplot as plt
import sensitivity

res = sensitivity.analyze(['area*'], {
	'max_area' : 350,
	'max_water' : 1600
})

print(res)

exit()

if False:
	feas_area = sensitivity.analyze_feasibility('max_area', 0, 1600)
	feas_water = sensitivity.analyze_feasibility('max_water', 0, 5000)
	feas_petrol = sensitivity.analyze_feasibility('max_petrol', 0, 150000, hide = True)

	print()
	print('Minimum area:', feas_area)
	print('Minimum water:', feas_water)
	print('Minimum petrol:', feas_petrol)
	print()

if False:
	plt.figure()

	petrol_vals = np.linspace(0, 400000, 50)
	area_vals = []

	for petrol in petrol_vals:
		options = dict(max_petrol = petrol)
		feas_area = sensitivity.analyze_feasibility('max_area', 0, 1600, options=options)
		area_vals.append(feas_area)

	plt.plot(petrol_vals, area_vals)
	plt.xlabel('Minimum Petrol')
	plt.ylabel('Minimum Area')
	plt.grid()
	plt.show()

if False:
	plt.figure()

	petrol_vals = np.linspace(0, 400000, 50)
	water_vals = []

	for petrol in petrol_vals:
		options = dict(max_petrol = petrol)
		feas_water = sensitivity.analyze_feasibility('max_water', 0, 5000, options=options)
		water_vals.append(feas_water)

	plt.plot(petrol_vals, water_vals)
	plt.xlabel('Minimum Petrol')
	plt.ylabel('Minimum Water')
	plt.grid()
	plt.show()

if True:
	plt.figure()

	feas_area = sensitivity.analyze_feasibility('max_area', 0, 1600)

	area_vals = np.linspace(feas_area, 1000, 50)
	water_vals = []

	for area in area_vals:
		options = dict(max_area = area)
		feas_water = sensitivity.analyze_feasibility('max_water', 0, 5000, options=options)
		water_vals.append(feas_water)

	plt.plot(area_vals, water_vals)
	plt.xlabel('Minimum Area')
	plt.ylabel('Minimum Water')
	plt.grid()
	plt.show()

if False:
	plt.figure()

	petrol_vals = np.linspace(0, 400000, 1)
	for petrol in petrol_vals:
		options = dict(max_petrol = petrol)
		feas_area = sensitivity.analyze_feasibility('max_area', 0, 1600, options=options)

		area_vals = np.linspace(feas_area, 1000, 50)
		water_vals = []

		for area in area_vals:
			options['max_area'] = area
			#options = dict(max_area = area)
			feas_water = sensitivity.analyze_feasibility('max_water', 0, 5000, options=options)
			water_vals.append(feas_water)

		plt.plot(area_vals, water_vals)

	plt.xlabel('Minimum Area')
	plt.ylabel('Minimum Water')
	plt.grid()
	plt.show()

