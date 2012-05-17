s=[([0]*5) for i in range(5)]   #表示棋盘
maxdep=2  #搜索深度
choicex=0  #最佳走法横坐标
choicey=0   #最佳走法纵坐标
def shownow(t):  #显示棋盘 
    for i in xrange(0,5):
        print t[i][0],t[i][1],t[i][2],t[i][3],t[i][4]
def isend(t):  #判断是否有人赢了
    for i in xrange(0,5):
        if t[i][0]==1 and t[i][1]==1 and t[i][2]==1 and t[i][3]==1 and t[i][4]==1:
            return 1
        if t[i][0]==2 and t[i][1]==2 and t[i][2]==2 and t[i][3]==2 and t[i][4]==2:
            return 2
    for i in xrange(0,5):
        if t[0][i]==1 and t[1][i]==1 and t[2][i]==1 and t[3][i]==1 and t[4][i]==1:
            return 1
        if t[0][i]==2 and t[1][i]==2 and t[2][i]==2 and t[3][i]==2 and t[4][i]==2:
            return 2
    if t[0][0]==1 and t[1][1]==1 and t[2][2]==1 and t[3][3]==1 and t[4][4]==1:
        return 1
    if t[0][0]==2 and t[1][1]==2 and t[2][2]==2 and t[3][3]==2 and t[4][4]==2:
        return 2
    if t[0][4]==1 and t[1][3]==1 and t[2][2]==1 and t[3][1]==1 and t[4][0]==1:
        return 1
    if t[0][4]==2 and t[1][3]==2 and t[2][2]==2 and t[3][1]==2 and t[4][0]==2:
        return 2
    return 0
def val(t):  #估价函数
    v=isend(t)
    if v==1 :
        return -13
    if v==2 :
        return 13
    for i in xrange(0,5):
        if t[i][0]!=1 and t[i][1]!=1 and t[i][2]!=1 and t[i][3]!=1 and t[i][4]!=1:
            v=v+1
        if t[i][0]!=2 and t[i][1]!=2 and t[i][2]!=2 and t[i][3]!=2 and t[i][4]!=2:
            v=v-1
    for i in xrange(0,5):
        if t[0][i]!=1 and t[1][i]!=1 and t[2][i]!=1 and t[3][i]!=1 and t[4][i]!=1:
            v=v+1
        if t[0][i]!=2 and t[1][i]!=2 and t[2][i]!=2 and t[3][i]!=2 and t[4][i]!=2:
            v=v-1
    if t[0][0]!=1 and t[1][1]!=1 and t[2][2]!=1 and t[3][3]!=1 and t[4][4]!=1:
        v=v+1
    if t[0][0]!=2 and t[1][1]!=2 and t[2][2]!=2 and t[3][3]!=2 and t[4][4]!=2:
        v=v-1
    if t[0][4]!=1 and t[1][3]!=1 and t[2][2]!=1 and t[3][1]!=1 and t[4][0]!=1:
        v=v+1
    if t[0][4]!=2 and t[1][3]!=2 and t[2][2]!=2 and t[3][1]!=2 and t[4][0]!=2:
        v=v-1
    return v
def haszero(t):  #是否平局，true表示没平，false表示平局
    for i in xrange(0,5):
        for j in xrange(0,5):
            if t[i][j]==0:
                return True
    return False
def maxsearch(t,dep):  #极大过程
    if dep == 0 or isend(t):
        return val(t)
    m=-14
    if not haszero(t):
        return val(t)
    chx=-1
    chy=-1
    for i in xrange(0,5):
        for j in xrange(0,5):
            if t[i][j]==0:
                t[i][j]=2
                temp=minsearch(t,dep-1)
                if m<temp:
                    m=temp
                    chx=i
                    chy=j
                t[i][j]=0
    global choicex
    global choicey
    if dep==maxdep:
        choicex=chx
        choicey=chy
    return m
def minsearch(t,dep):   #极小过程
    if dep == 0 or isend(t):
        return val(t)
    m=14
    if not haszero(t):
        return val(t)
    chx=-1
    chy=-1
    for i in xrange(0,5):
        for j in xrange(0,5):
            if t[i][j]==0:
                t[i][j]=1
                temp=maxsearch(t,dep-1)
                if m>temp:
                    m=temp
                    chx=i
                    chy=j
                t[i][j]=0
    global choicex
    global choicey
    if dep==maxdep:
        choicex=chx
        choicey=chy
    return m

print "1 means your point,2 means my point,0 means empty point."                
x=input("Input 1 to be the first player, or input 2 to be the second player:\n")
if x==2 :
    s[2][2]=2
    print "I pick  3 , 3"
shownow(s)
while haszero(s) :  #开始下棋
    x,y=input("Input your choice(1~5,1~5):(for example \"2,2\")\n")
    s[x-1][y-1]=1
    shownow(s)
    res=isend(s)
    if res == 1:
        print "You win!"
        break
    if res == 2:
        print "You lose!"
        break
    if not haszero(s):
        print "Draw game!"
        break
    maxsearch(s,maxdep)
    print "I pick ",choicex+1,",",choicey+1
    s[choicex][choicey]=2
    shownow(s)
    res=isend(s)
    if res == 1:
        print "You win!"
        break
    if res == 2:
        print "You lose!"
        break
    if not haszero(s):
        print "Draw game!"
    
    
    
    
