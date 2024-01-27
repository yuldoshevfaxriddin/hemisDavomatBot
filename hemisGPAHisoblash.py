
def calc(k,u):
    s = 0
    for i in range(len(k)):
        s += (k[i]*u[i])
    return s/sum(k)    

def rev(u):
    t = []    
    for i in range(len(u)):
        a = 0
        if u[i]<70:
            a=3
        if u[i]>=70 and u[i]<90:
            a=4
        if u[i]>=90:
            a=5
        t.append(a)
    return t

def adding(l1,l2,l3,l4,l5,l6,l7):
    t = []
    for i in l1:
        t.append(i)
    
    for i in l2:
        t.append(i)
        
    for i in l3:
        t.append(i)
        
    for i in l4:
        t.append(i)
        
    for i in l5:
        t.append(i)
        
    for i in l6:
        t.append(i)
        
    for i in l7:
        t.append(i)

    return t

'''
k1 = [4,2,4,8,6,6]
u1 = [76,88,78,93,80,84]

k2 = [4,2,4,4,4,6]
u2 = [69,70,74,76,66,81]

k3 = [6,6,6,6,6,6]
u3 = [81,73,85,98,67,82]

k4 = [6,6,6,6,6]
u4 = [91,94,91,92,92]

k5 = [6,6,6,6,6,2,4]
u5 = [92,84,93,91,93,72,90]

k6 = [6,6,6,6,4,0,0,2]
u6 = [81,96,87,95,88,60,90,95]

k7 = [6,6,6,6]
u7 = [75,80,90,82]
'''


k1 = [4,2,4,8,6,6]
u1 = [76,88,78,93,80,84]

k2 = [4,2,4,4,4,6]
u2 = [69,70,74,76,66,81]

k3 = [6,6,6,6,6,6]
u3 = [81,73,85,98,67,82]

k4 = [6,6,6,6,6]
u4 = [91,94,91,92,92]

k5 = [6,6,6,6,6,2,4]
u5 = [92,84,93,91,93,72,90]

k6 = [6,6,6,6,4,0,0,2]
u6 = [81,96,87,95,88,60,90,95]

k7 = [6,6,6,6]
u7 = [75,80,90,82]



u1 = rev(u1)
u2 = rev(u2)
u3 = rev(u3)
u4 = rev(u4)
u5 = rev(u5)
u6 = rev(u6)
u7 = rev(u7)

k = adding(k1,k2,k3,k4,k5,k6,k7)
u = adding(u1,u2,u3,u4,u5,u6,u7)

s1 = calc(k1,u1)
s2 = calc(k2,u2)
s3 = calc(k3,u3)
s4 = calc(k4,u4)
s5 = calc(k5,u5)
s6 = calc(k6,u6)
s7 = calc(k7,u7)

print('1 - ',s1)
print('2 - ',s2)
print('3 - ',s3)
print('4 - ',s4)
print('5 - ',s5)
print('6 - ',s6)
print('7 - ',s7)
print('natija ',s1+s2+s3+s4+s5+s6+s7)

print('natija ',calc(k,u))
#u6 = rev(u6)
#print(u6)
