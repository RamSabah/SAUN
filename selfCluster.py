import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
import seaborn as sns
import matplotlib.pyplot as plt

sns.set()

data = pd.read_excel('excel/testdata.xlsx')
print(data)

plt.scatter(data['namespaces'], data['index'])
plt.xlim(-180, 180)
plt.ylim(-90, 90)
plt.show()

kmenas = KMeans(3)
#kmenas.fit(data)



########################################################################################################################
# For 100% Dynamic Solution self ontology recognition required.
#
########################################################################################################################