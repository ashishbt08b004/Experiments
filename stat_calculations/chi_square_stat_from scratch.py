# Function to calculate the chi-square statistic
def chi_sq_stat(data_ob):
    col_tot=data_ob.sum(axis=0)
    row_tot=data_ob.sum(axis=1)
    tot=col_tot.sum(axis=0)
    row_tot.shape=(2,1)
    data_ex=(col_tot/tot)*row_tot
    num,den=(data_ob-data_ex)**2,data_ex
    chi=num/den
    return chi.sum()

 #Function to calculate the degrees of freedom   
def degree_of_freedom(data_ob):
    dof=(data_ob.shape[0]-1)*(data_ex.shape[1]-1)
    return dof

# Calculting these for the observed data
data_ob=np.array([(20,6,30,44),(180,34,50,36)])
chi_sq_stat(data_ob)
degree_of_freedom(data_ob)
