import subprocess as sp
import os, shutil, re
import numpy as np

def analyze(variables = None, options = None, transform = None):
	if options is None: options = {}
	if variables is None: variables = ['PROFIT', 'OPT']

	try:
		os.mkdir('temp')
	except FileExistsError:
		pass

	shutil.copyfile('diesel.run', 'temp/diesel.run')
	shutil.copyfile('diesel.mod', 'temp/diesel.mod')
	shutil.copyfile('diesel.dat', 'temp/diesel.dat')

	data = ''
	with open('temp/diesel.dat', 'r') as f:
		data = f.read()

	stats = {}

	if transform:
		newdata = transform(data)
	else:
		newdata = data
		for variable in options.keys():
			newdata = re.sub('%s := [0-9.]+' % variable, '%s := %f' % (variable, options[variable]), newdata)

	with open('temp/diesel.dat', 'w+') as f:
		f.write(newdata)

	os.environ['PATH'] += ":/home/sebastian/.ampl"
	args = ('/home/sebastian/.ampl/ampl', 'diesel.run')
	output = str(sp.check_output(args, env=os.environ, cwd='temp'))
	stats = {}

	for variable in variables:
		if variable[-1] != '*':
			result = re.search('%s = ([0-9.]*)' % variable, output)
			if result:
				value = float(result.group(1))
			else:
				value = np.nan
		else:
			result = re.search('%s [*] = (.*);' % variable[0:-1], output, re.DOTALL | re.MULTILINE)
			if result:
				value = result.group(1)
			else:
				value = np.nan
		stats[variable] = value

	if 'OPT' in variables and re.search('optimal solution.', output):
		stats['OPT'] = True
	else:
		stats['OPT'] = False

	shutil.rmtree('temp')
	return stats

def analyze_variable(variable, values, variables = None, options = None):
	if options is None: options = {}
	if variables is None: variables = ['PROFIT', 'OPT']

	variables.append(variable)
	variables = list(set(variables))
	stats = {k : [] for k in variables}

	for value in values:
		options[variable] = value
		res = analyze(variables, options = options)

		for k in variables:
			stats[k].append(res[k])

	return stats

def analyze_feasibility(variable, a, b, options = None, eps = 1e-3, hide = False):
	if options is None: options = {}

	options[variable] = a
	sa = analyze(['OPT'], options)

	options[variable] = b
	sb = analyze(['OPT'], options)

	if sa['OPT'] == sb['OPT']:
		if not hide:
			print('Start values should be in feasible/non-feasible region!')
			print('  a: ', 'feasible' if sa['OPT'] else 'not feasible')
			print('  b: ', 'feasible' if sb['OPT'] else 'not feasible')
		return np.nan

	while abs(b - a) > eps: 
		c = 0.5 * (b - a) + a 
		options[variable] = c
		sc = analyze(['OPT'], options)

		if sc['OPT'] == sa['OPT']:
			a = c
		elif sc['OPT'] == sb['OPT']:
			b = c

	return 0.5 * (b - a) + a
