
# coding: utf-8

# In[1]:


import numpy as np
import numpy as np
from sklearn.cluster import MiniBatchKMeans
import dask
import dask_ml
import dask.array as da
from sklearn.cluster import KMeans
from math import sqrt
import pandas as pd


# In[41]:


#Creating query database
X_db = np.around(np.random.random((10000,50)),decimals=2)
X_query = np.around(np.random.random((1,50)),decimals=2)


# In[42]:


from sklearn.metrics.pairwise import euclidean_distances
def nearest_db_item(query,db):
    return np.min(euclidean_distances(X_query,X_db)), np.argmin(euclidean_distances(X_query,X_db))


# In[37]:


def batch_clust_part(prts, n_clust,batch_sz):
    
    """
    Parameters
    ----------
    prts - list of numpy arrays
    Contains the partitions of the data. Each partition as an array. Output of adj_col_part should be fed in this parameter.
    number of elements in list - number of overall feature/number of features in each partition
    shape of each array - (number of data points X number of features in each partition)
    
    n_clus - integer
    number of clusters for each k-Means clustering to be run on the data partitions
    
    batch_sz - integer
    Number of batches from one training dataset
    
    Returns
    -------
    dictionary 
    5 keys in the dictionary
    models - list of trained kMeans model trained on respective partition. As many models as there are partitions.
    clust_member - array containing the cluster memberships of each datapoints. As many memberships for a datapoint as there are partitions.
    part_num_feat - number of features in each partition
    model_num - number of models or number of partitions or number of cluster memberships for each data point
    cluster_center - cluster centres for each of 100 clusters for each kMeans model
    """
    
    if(prts[0].shape[0]/batch_sz <= 100):
        raise ValueError('Batch size is too small. Enter a smaller number for batch_sz parameter. The value you entered for batch_zs is {}'.format(batch_sz))
    
    clust_arr = np.zeros((prts[0].shape[0],len(prts)))
    models = []
    cluster_centers = []
    for i, part in enumerate(prts):
        kmeans = MiniBatchKMeans(n_clusters=n_clust, random_state=0, batch_size=int((prts[0].shape[0])/batch_sz),  max_iter=10)
        kmeans = kmeans.fit(part)
        models.append(kmeans)
        cluster_centers.append(kmeans.cluster_centers_)
        label = kmeans.predict(part)
        clust_arr[:,i] = label
    results = {"models" : models, "clust_member" : clust_arr, "part_num_feat" : prts[0].shape[1], "clust_num" : len(prts), "cluster_centers" : cluster_centers}
    return results


# In[38]:


def adj_col_part(X, sub_set):
    """
    Parameters
    -----------
    sub_set - integer 
    number of features each partition should have
    
    X - numpy array 
    input_data to be partitioned
    shape of array - (number of data points X number of overall features) 
    
    Returns
    -------
    list of numpy arrays 
    number of elements in list - number of overall feature/number of features in each partition
    shape of each array - (number of data points X number of features in each partition)

    """

    sub_ele_list = []

    if(X.shape[1] % sub_set != 0):
        raise ValueError('sub_set should be a factor of number of features in input array. The value of sub_set you entered was: {}. {} is not a factor of {}.'.format(sub_set, sub_set, X.shape[1]))

    for i in range(0, X.shape[1], sub_set):
        sub = X[:,i:i+sub_set]
        sub_ele_list.append(sub)

    return sub_ele_list

#sub_vec_list = adj_col_part(X,2)


# In[44]:


from datetime import datetime
#X = np.random.random((10000, 50))
sub_vec_list = adj_col_part(X_db,5)
start=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
clust_batch_mod = batch_clust_part(sub_vec_list,100,10)
end = datetime.now().strftime("%Y-%m-%d %H:%M:%S")


# In[69]:


def query_clust_predict(query,model):
    
    """
    Parameters
    ----------
    query - numpy array
    query row for which the nearest neighbor is being found
    shape - (1 X number of features in database data)
    
    model - dictionary
    model object containing model details like trained models, cluster memberships, # partitions, # clusters, cluster centers
    
    Returns
    -------
    clust_arr - numpy array
    contains the cluster memberships of the query data point according to corresponding partition kMeans model
    
    
    """
    
    X_query_part = adj_col_part(query,model["part_num_feat"]) 
    clust_arr = np.zeros((X_query_part[0].shape[0],len(X_query_part)))
    for i, part in enumerate(X_query_part):
        label = model["models"][i].predict(part)
        clust_arr[:,i] = label
    return clust_arr  


# In[75]:


def db_clust_predict(query,db,model):
    
    """
    Parameters
    ----------
    query - numpy array
    query row for which the nearest neighbor is being found
    shape - (1 X number of features in database data)
    
    db - numpy array
    database of all the data points
    shape - (number of rows in database data X number of features in database data)
    
    model - dictionary
    model object containing model details like trained models, cluster memberships, # partitions, # clusters, cluster centers
    
    
    Returns
    -------
    clust_arr - numpy array
    contains the cluster memberships of the db data point nearest to query data point according to corresponding partition kMeans model
    
    
    """
    nearest = nearest_db_item(query,db)
    X_db_part = adj_col_part(X_db[nearest[1],:].reshape(1,query.shape[1]),model["part_num_feat"])
    clust_db_arr = np.zeros((X_db_part[0].shape[0],len(X_db_part)))
    for i, part in enumerate(X_db_part):
        label = clust_batch_mod["models"][i].predict(part)
        clust_db_arr[:,i] = label
    return clust_db_arr


# In[ ]:


def db_clust_predict1(query,db,model):
    
     """
    Parameters
    ----------
    query - numpy array
    query row for which the nearest neighbor is being found
    shape - (1 X number of features in database data)
    
    db - numpy array
    database of all the data points
    shape - (number of rows in database data X number of features in database data)
    
    model - dictionary
    model object containing model details like trained models, cluster memberships, # partitions, # clusters, cluster centers
    
    
    Returns
    -------
    clust_arr - numpy array
    contains the cluster memberships of the db data point nearest to query data point according to corresponding partition kMeans model
    
    Does no new prediction. Just fetches the right row from the cluster membership array from the model object. db_clust_predict 
    db_clust_predict1 should give the same result.
    
    """
    nearest = nearest_db_item(query,db)
    return model["clust_member"][nearest[1],:]


# In[83]:


query_clust = query_clust_predict(X_query,clust_batch_mod)


# In[110]:


query_clust


# In[84]:


db_near_clust = db_clust_predict(X_query,X_db,clust_batch_mod)


# In[111]:


db_near_clust


# In[109]:


def accuracy1(model, db, query):
    """
    Parameters
    ----------

    query - numpy array
    query row for which the nearest neighbor is being found
    shape - (1 X number of features in database data)
    
    db - numpy array
    database of all the data points
    shape - (number of rows in database data X number of features in database data)
    
    model - dictionary
    model object containing model details like trained models, cluster memberships, # partitions, # clusters, cluster centers
    
    
    Returns
    -------
    sum of Euclidean distances between the cluster centers of the corresponding clusters of the query and nearest db point
    
    """
    query_clust = query_clust_predict(query,model)
    db_near_clust = db_clust_predict(query,db,model)
    tot_err = 0
    for i in range(len(models["models"])):
        tot_err += euclidean_distances(clust_batch_mod["cluster_centers"][i][int(db_near_clust[:,i]),:].reshape(1,5),clust_batch_mod["cluster_centers"][i][int(query_clust[:,i]),:].reshape(1,5))
    return tot_err      


# In[107]:


def accuracy2(db, query,model):
    
    """
    Parameters
    ----------

    query - numpy array
    query row for which the nearest neighbor is being found
    shape - (1 X number of features in database data)
    
    db - numpy array
    database of all the data points
    shape - (number of rows in database data X number of features in database data)
    
    model - dictionary
    model object containing model details like trained models, cluster memberships, # partitions, # clusters, cluster centers
    
    Returns
    -------
    ratio of number of commom membership clusters (among all the memberships) between query and database
    
    """
    
    
    query_clust = query_clust_predict(query,model)
    db_near_clust = db_clust_predict(query,db,model)
    return len(set(list(query_clust[0])).intersection(set(list(db_near_clust[0]))))/query_clust.shape[1]


# In[132]:


def accuracy3(query,db,model):
  """
    Parameters
    ----------

    query - numpy array
    query row for which the nearest neighbor is being found
    shape - (1 X number of features in database data)
    
    db - numpy array
    database of all the data points
    shape - (number of rows in database data X number of features in database data)
    
    model - dictionary
    model object containing model details like trained models, cluster memberships, # partitions, # clusters, cluster centers
    
    Returns
    -------
    binary 0 0r 1
    1 means - either mode of both (query and database) the cluster arrays are same or mode of one array is present in the other
    
    """   
    
    query_clust = query_clust_predict(query,model)
    db_near_clust = db_clust_predict(query,db,model)
    db_near_clust_pmode = np.asscalar(pd.Series(db_near_clust[0]).value_counts().head(1).index)
    query_clust_pmode = np.asscalar(pd.Series(query_clust[0]).value_counts().head(1).index)
    if (db_near_clust_pmode == query_clust_pmode) or (query_clust_pmode in db_near_clust) or (db_near_clust_pmode in query_clust): 
        p = 1
    else:
        p = 0
    return p


# In[ ]:


# Rough Work 
X_db_part = adj_col_part(X_db[9235,:].reshape(1,50),5)
clust_db_arr = np.zeros((X_db_part[0].shape[0],len(X_db_part)))
for i, part in enumerate(X_db_part):
        label = clust_batch_mod["models"][i].predict(part)
        clust_db_arr[:,i] = label
clust_db_arr  

X_query_part = adj_col_part(X_query,5)
clust_arr = np.zeros((X_query_part[0].shape[0],len(X_query_part)))
for i, part in enumerate(X_query_part):
        label = clust_batch_mod["models"][i].predict(part)
        clust_arr[:,i] = label
clust_arr 

clust_batch_mod["clust_member"][nearest[1],:]

