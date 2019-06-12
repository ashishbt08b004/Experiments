# Calculating SSAG
group_mean=data.groupby('Lot').mean()
group_mean=np.array(group_mean['OD'])
tot_mean=np.array(data['OD'].mean())
group_count=data.groupby('Lot').count()
group_count=np.array(group_count['OD'])
fac1=(group_mean-tot_mean)**2
fac2=fac1*group_count
DF1=(data['Lot'].unique()).size-1
SSAG=(fac2.sum())/DF1
SSAG

#Calculating SSWG
group_var=[]
for i in range((data['Lot'].unique()).size):
    lot_data=np.array(data[data['Lot']==i+1]['OD'])
    lot_data_mean=lot_data.mean()
    group_var_int=((lot_data-lot_data_mean)**2).sum()
    group_var.append(group_var_int)
group_var_sum=(np.array(group_var)).sum()
DF2=data.shape[0]-(data['Lot'].unique()).size-1
SSAW=group_var_sum/DF2
SSAW

F=SSAG/SSAW
F
