### Data Preprocessing

import pandas as pd
from IPython.display import display
data=pd.read_csv('WA_Fn-UseC_-Telco-Customer-Churn.csv')
pd.options.display.max_columns = None
data.head()
data.info()
data.describe(include='all')

#Handle NaN values in the TotalCharges column
data['TotalCharges']=pd.to_numeric(data['TotalCharges'], errors='coerce')
fill_total=data['tenure']*data['MonthlyCharges']
data['TotalCharges']=data['TotalCharges'].fillna(fill_total)

three_items_list=['MultipleLines','InternetService','OnlineSecurity','OnlineBackup','DeviceProtection','TechSupport','StreamingTV','StreamingMovies','Contract','PaymentMethod']
for column in three_items_list:
    print(column)
    print(data[column].unique())
#remove the 'no internet service' and 'no phone service' information => replace with 'no'
no_internet_list=[x for x in three_items_list if x not in ['MultipleLines','InternetService','Contract','PaymentMethod']]
for column in no_internet_list:
    data[column]=data[column].replace('No internet service','No')
data.MultipleLines=data.MultipleLines.replace('No phone service','No')

#Replace 0/1 in the seniorcitizen column Yes/No
data.SeniorCitizen=data.SeniorCitizen.replace(0,'No')
data.SeniorCitizen=data.SeniorCitizen.replace(1,'Yes')

#Group tenure into 5 blocks
tenure_groups=['0–12 Month','12–24 Month','24–48 Months','48–60 Month','> 60 Month']
tenure_months=[12,24,48,60,500]
def group_tenure(month):
    for ceiling in tenure_months:
        if month<=ceiling:
            return tenure_groups[tenure_months.index(ceiling)]
data['tenure_group']=data.tenure.transform(group_tenure)

#drop useless columns
data=data.drop(['customerID','tenure'],axis='columns')

### Exploratory data analysis and feature selection
#Correlation between numeric variables
import numpy as np
np.corrcoef(data.MonthlyCharges,data.TotalCharges)
#drop one of the columns if high correlation
data=data.drop(['TotalCharges'],axis='columns')