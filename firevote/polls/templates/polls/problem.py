t=int(input())
for i in range(t):
    n=int(input())
    a=list(map(int,input().split()))
    for j in range(len(a)):
        key=a[j]
        c=0
        for k in a[j+1:]:
            if(k>key):
                break
            else:
                c+=1
        print(c,end=" ")




