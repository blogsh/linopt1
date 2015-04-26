import subprocess as sp
import os, shutil, re
import numpy as np

def analyze(variables = None, options = None, transform = None):
	""" 
		Runs the linear optimization problem once. 

		variables - List of the names of variables that should be
					tracked (according to the display commands in
					the run file)
		options - Map of variables and the values they should be set
				  to (according to the names in the dat file)
		transform - An optional transform function that will be used
		            instead of the options map to do more complicated
		            changes

		Set variables can be obtained/set by using e.g.

			diesel*

		as the variable/parameter name.
	"""
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
			if variable[-1] != '*':
				newdata = re.sub('%s := [0-9.]+' % variable, '%s := %f' % (variable, options[variable]), newdata)
			else:
				temp = '\n'.join(['%s %f' % (k, options[variable][k]) for k in options[variable].keys()])
				m = re.search('%s :=(.*?);' % variable[0:-1], newdata, re.DOTALL | re.MULTILINE)
				if m:
					newdata = newdata.replace(m.group(0), variable[0:-1] + ' :=\n' + temp + ';')
			
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
			result = re.search('%s \[\*\] :=(.*?);' % variable[0:-1], output, re.DOTALL | re.MULTILINE)
			if result:
				value = result.group(1)
				value = [line.strip() for line in value.split('\\n')]
				valuet = value[1:-1]
				value = {}
				for valueti in valuet:
					res = re.split('\s+', valueti)
					value[res[0].strip()] = float(res[1].strip())
			else:
				value = np.nan
		stats[variable] = value

	if 'OPT' in variables:
		if re.search('optimal solution.', output):
			stats['OPT'] = True
		else:
			stats['OPT'] = False

	shutil.rmtree('temp')
	return stats

def analyze_variable(variable, values, variables = None, options = None):
	"""
		Analyzes the results while changing one variable.

		variable - Variable that should be changed
		values - Values it should be set to
		variables - The variables that should be tracked
		options - The parameters that should be set as well
	"""
	if options is None: options = {}
	if variables is None: variables = ['PROFIT', 'OPT']

	variables.append(variable)
	variables = list(set(variables))
	stats = {k : [] for k in variables}

	for k in variables:
		if k[-1] == '*':
			stats[k] = {}

	for value in values:
		options[variable] = value
		res = analyze(variables, options = options)

		for k in variables:
			if k[-1] != '*':
				stats[k].append(res[k])
			else:
				for k2 in res[k].keys():
					if not k2 in stats[k]:
						stats[k][k2] = []
					stats[k][k2].append(res[k][k2])

	return stats

def analyze_feasibility(variable, a, b, options = None, eps = 1e-3, hide = False):
	"""
		Checks the feasibility of the problem in dependency on one variable.
		Bisection is used to find the feasibility border.

		variable - The variable that should 
		a, b - One feasible, one unfeasible value
		eps - precision
		hide - hide error messages
	"""
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
