import numpy as np
import pandas as pd
import random
import datetime
import names

# Generate synthetic data
start = datetime.datetime(2023, 1, 1)
end = datetime.datetime(2023, 12, 30)
antecedentes = [names.get_full_name() for i in range(0,5000)]
consequentes = [random.randint(1,5000) for i in range(0,10000)]


def random_date(start, end):
  return start + datetime.timedelta(seconds=random.randint(0, int((end - start).total_seconds())))


timestamps = [random_date(start,end) for i in range(0,50000)] 

data = []
for timestamp in timestamps:
    antecedente = np.random.choice(antecedentes)  
    consequente = np.random.choice(consequentes)  
    data.append({'timestamp': timestamp, 'o': antecedente, 'd': consequente})

# # Apply association rule
# count = 0
# for i in range(len(data) - 1):
#     if data[i]['o'] == 'rodrigo' and data[i]['d'] == 'heitor':

#         data[i + 1]['o'] = 'rodrigo' 
#         data[i + 1]['d'] = 'vinicius'

#         data[i + 2]['o'] = 'vinicius' 
#         data[i + 2]['d'] = 'gabriel'

#         data[i + 3]['o'] = 'gabriel' 
#         data[i + 3]['d'] = 'rodrigo'

#         data[i + 4]['o'] = 'rodrigo' 
#         data[i + 4]['d'] = 'gabriel'
#         i += 4
#         count += 1

# Create DataFrame
df = pd.DataFrame(data)
df.to_csv('forged_data.csv')
print(df)