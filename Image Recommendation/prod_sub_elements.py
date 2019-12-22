import numpy as np
import random
X = np.random.random((500, 20)) #20 dimensions of 500 samples
# X = np.random.random((5, 5)) #20 dimensions of 500 samples
sub_set = None


def arg_part(X, k):
    """

    :param X: input_data to be partitioned
    :param k: element around which partition is created
    :return: returns a partition of data with the partitioned columns and their replacements removed from the data
    """
    l = []
    index = np.argpartition(X, k, axis=1)
    index = index[:, k+1:X.shape[1]]

    for row in index:
        pr = [j for j in row if j not in range(k+1)]
        l.append(pr)

    return X[:, l[0]]

pt = arg_part(X, 2)



def adj_col_part(X, sub_set):
    """
    :param sub_set: number of features each partition should have
    X: input_data to be partitioned

    :return: list of arrays containing (number of features/subset) columns each and all the rows as the parent array. For example the parent data here has 20 columns
    subset is 2. Hence we obtain list of 10 (20/2) arrays each having 500 rows and 2 columns

    returns adjacent column attributes as array subsets
    """

    sub_ele_list = []

    for i in range(0, X.shape[1], sub_set):
        sub = X[:,i:i+sub_set]
        sub_ele_list.append(sub)

    return sub_ele_list

sub_vec_list = adj_col_part(X,2)



def rand_col_part(X, sub_set):
    """

    :param sub_set: number of features each partition should have
    X: input_data to be partitioned
    :return: list of arrays random sub_set array.
    returns random column attributes as array subsets
    """
    ran_sub_ele_list = []

    for i in range(0, X.shape[1],sub_set):
        ran_sub_ele = X[:,list(np.random.choice(range(X.shape[1]),sub_set))]
        #random.shuffle(ran_sub_ele)
        ran_sub_ele_list.append(ran_sub_ele)

    return ran_sub_ele_list

sub_rand_vec_lst = rand_col_part(X,2)





