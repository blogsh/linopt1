import numpy as np
import matplotlib.pyplot as plt
import sensitivity

vals = np.linspace(1, 1.25, 20)
result = sensitivity.analyze_variable('petrol_price', vals, ['PROFIT', 'diesel*', 'area*'])
print('Old profit:', result['PROFIT'][0])
print('New profit:', result['PROFIT'][-1])
plt.figure()

plt.plot(vals, result['PROFIT'])
plt.grid()
plt.xlabel('Petrol Price')
plt.ylabel('Profit')

#plt.subplot(2, 1, 2)
#plt.plot(vals, result['diesel*']['B5'])
#plt.plot(vals, result['diesel*']['B30'])
#plt.plot(vals, result['diesel*']['B100'])
#plt.plot(vals, result['area*']['Cotton'])
#plt.plot(vals, result['area*']['Soy'])
#plt.plot(vals, result['area*']['Sunflower'])
#plt.grid()
#plt.xlabel('Petrol Price')
#plt.legend(['B5', 'B30', 'B100'])
#plt.legend(['Cotton', 'Soy', 'Sunflower'])
#plt.ylabel('Profit')

plt.show()
