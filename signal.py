import numpy as np 

def filter(b,a,x):
    '''b is the coefficients of the x(n),type is list
    a is the coefficients of the y(n),type is list
    x is the data,type is np.array
    the type of retval is np.array'''
    xt = [0]*(len(b)-1)+x.ravel().tolist()
    yt = [0]*(len(a)-1)+np.zeros(x.ravel().shape).tolist()
    at = a[1:]
    xt = np.array(xt)
    yt = np.array(yt)
    #使得待求值的系数为1
    at = -1*np.array(at)/a[0]
    bt = np.array(b)/a[0]
    for i in range(at.size,len(x)+at.size):
        ytt = yt[i-at.size:i]#经过各种尝试，还是先提取后反转比较少屁事，不然容易涉及到正数：负数：-1，然后从头跳到尾而失败。
        xtt = xt[i-at.size-bt.size+1:i-at.size+1]
        yt[i] = sum(at*ytt[::-1])+sum(bt*xtt[::-1])
    return yt[at.size:]

def impseq(site,begin,end):
    '''will make a delta(n)	
the length of retval is end-begin so that it's like python rather matlab.
the type of retval is np.array'''
    a = [0]*(end-begin)
    a[site-begin+1]=1
    return np.array(a)
