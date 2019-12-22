
# coding: utf-8

# In[1]:


import numpy as np
import numpy as np
from sklearn.cluster import MiniBatchKMeans
import dask
import dask_ml
import dask.array as da
from sklearn.cluster import KMeans
#X = np.random.random((1000000, 100))


# In[2]:


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


# In[3]:


def clust_part(prts, n_clus):
    
    """
    Parameters
    ----------
    prts - list of numpy arrays
    Contains the partitions of the data. Each partition as an array. Output of adj_col_part should be fed in this parameter.
    number of elements in list - number of overall feature/number of features in each partition
    shape of each array - (number of data points X number of features in each partition)
    
    n_clus - integer
    number of clusters for each k-Means clustering to be run on the data partitions
    
    
    Returns
    -------
    dictionary 
    5 keys in the dictionary
    models - list of trained kMeans model trained on respective partition. As many models as there are partitions.
    clust_member - array containing the cluster memberships of each datapoints. As many memberships for a datapoint as there are partitions.
    part_num_feat - number of features in each partition
    model_num - number of models or number of partitions or number of cluster memberships for each data point
    cluster_centers - cluster centres for each of 100 clusters for each kMeans model
    
    """
    
    clust_arr = np.zeros((prts[0].shape[0],len(prts)))
    models = []
    for i, part in enumerate(prts):
        kmeans = KMeans(n_clusters=n_clus)
        kmeans = kmeans.fit(part)
        models.append(kmeans)
        cluster_centers.append(kmeans.cluster_centers_)
        label = kmeans.predict(part)
        clust_arr[:,i] = label
    results = {"models" : models, "clust_member" : clust_arr, "part_num_feat" : prts[0].shape[1], "clust_num" : len(prts), "cluster_centers" : cluster_centers}
    return kmeans, clust_arr


# In[36]:


# Time benchmarking for running clust_part
from datetime import datetime
X = np.random.random((10000, 100))
sub_vec_list = adj_col_part(X,5) 
start=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
clust_mod = clust_part(sub_vec_list,100)
end = datetime.now().strftime("%Y-%m-%d %H:%M:%S")


# In[ ]:


def dask_clust_part(prts,n_clust,dask_chunk):
    
    """
    Parameters
    ----------
    prts - list of numpy arrays
    Contains the partitions of the data. Each partition as an array. Output of adj_col_part should be fed in this parameter.
    number of elements in list - number of overall feature/number of features in each partition
    shape of each array - (number of data points X number of features in each partition)
    
    n_clus - integer
    number of clusters for each k-Means clustering to be run on the data partitions
    
    dask_chunk - integer
    number of chunks to be made of training data in dask arrays 
    
    Returns
    -------
    numpy array
    contains the array of cluster indices for each row in data
    shape of array - (number of data points X number of partition or number of elements in prts)
    """
        
    clust_arr = np.zeros((prts[0].shape[0],len(prts)))
    for i, part in enumerate(prts):
        X = da.from_array(part, chunks = (int((part.shape[0])/dask_chunk),part.shape[1]))
        kmeans = cluster.KMeans(n_clusters=n_clust)
        kmeans = kmeans.fit(X)
        label = kmeans.predict(X).compute()
        clust_arr[:,i] = label
    return kmeans, clust_arr


# In[ ]:


#Running clust_part
X = np.random.random((1000000, 100))
sub_vec_list = adj_col_part(X,5)
prts = sub_vec_list
clust_dask_mod = dask_clust_part(prts,100,10)


# In[16]:


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
    clust_num - number of models or number of partitions or number of cluster memberships for each data point
    cluster_centers - cluster centres for each of 100 clusters for each kMeans model
    
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


# In[17]:


# Time benchmarking for the batch_clust_part function

from datetime import datetime
X = np.random.random((10000, 20))
sub_vec_list = adj_col_part(X,5)
start=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
clust_batch_mod = batch_clust_part(sub_vec_list,100,10)
end = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

