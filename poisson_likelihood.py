


Step 1: A function to calculate the Poisson probability for each point
import numpy as np
import math as mh
np.seterr(divide='ignore', invalid='ignore') #ignore division by zero and invalid numbers
def poissonpdf(x,lbd):
    val = (np.power(lbd,x)*np.exp(-lbd))/(mh.factorial(x))
    return val
    
    
Step 2: A function to calculate the Log likelihood over the data given a value of arrival rate
def loglikelihood(data,lbd):
    lkhd=1
    for i in range(len(data)):
        lkhd=lkhd*poissonpdf(data[i],lbd)
    if lkhd!=0:
        val=np.log(lkhd)
    else:
        val=0
    return val
    
    
Step 3: A function to calculate the derivative of log likelihood wrt to arrival rate λ.
def diffllhd(data,lbd):
    diff = -len(data) + sum(data)/lbd
    return diff
    
    
Step 4: Generating test data with 100 data points - random number of arrivals/unit time between 3 and 12
data=[randint(3, 12) for p in range(100)]

Step 5: Calculating log-likelihood for different values of arrival rates (1 to 9) and plotting them to find the arrival rate which maximises 
y=[loglikelihood(data,i) for i in range(1,10)]
y=[num for num in y if num ]
x=[i for i in range(1,10) if loglikelihood(data,i)]
plt.plot(x,y)
plt.axvline(x=6,color='k')
plt.title('Log-Likelihoods for different lambdas')
plt.xlabel('Log Likelihood')
plt.ylabel('Lambda')

Step 6 (Substitute of Step 5): Newton Raphson method
def newtonRaphson(data,lbd): 
    h = loglikelihood(data,lbd) / diffllhd(data,lbd) 
    while abs(h) >= 0.0001: 
        if diffllhd!=0:
            h = loglikelihood(data,lbd) / diffllhd(data,lbd) 
          
        # x(i+1) = x(i) - f(x) / f'(x) 
            lbd = lbd - h
        else:
            lbd=lbd
    return lbd 

