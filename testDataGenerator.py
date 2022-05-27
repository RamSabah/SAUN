import pandas as pd
import random
from random import randrange



print(random.randint(0,100) / 100)
coinName = []
hasMint = []
hasUncertainty = []

for i in range(1000000):
    coinName.append("coin_"+str(i))
    hasMint.append("http://nomisma.org/id/comama")
    hasUncertainty.append(random.randint(50,100) / 100)
    print(i)
hasUncertainty[0] = 0
dataframe = pd.DataFrame([coinName, hasMint, hasUncertainty]).T
dataframe.to_excel(excel_writer="excel/testData_1M.xlsx", header=["Subject","http://nomisma.org/ontology#hasMint", "hasMint*hasUncertainty"], index=None)

print(coinName)
print(hasMint)
print(hasUncertainty)
