import urllib,cookielib,urllib2,re,time,MySQLdb

conn = MySQLdb.connect(host="localhost",  
                       user="root",  
                       passwd="root",  
                       db="miniOnlineJudge")
cursor = conn.cursor()

class ojweb:
  def __init__(self,loginurl,loginheaders,loginbody,submiturl,submitheaders,submitbody,searchurl,searchre,searchresult,other):
    self.loginurl=loginurl
    self.loginheaders=loginheaders
    self.loginbody=loginbody
    self.submiturl=submiturl
    self.submitheaders=submitheaders
    self.submitbody=submitbody
    self.searchurl=searchurl
    self.searchre=searchre
    self.searchresult=searchresult
    self.other=other
  def updatesubmitbody(self,submitbody):
    self.submitbody=submitbody
  def updatesearchre(self,searchre):
    self.searchre=searchre

poj=ojweb('http://poj.org/login',[('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64)')],({'user_id1':'minitestcoder','password1':'0903106test',
                       'B1':'login','url':'/'}),'http://poj.org/submit',[('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64)')],({'problem_id':'','language':'','source':'',
             'submit':'Submit'}),'http://poj.org/status?problem_id=&user_id=minitestcoder&result=&language=','waitre',[4,6,7,8,9],'poj')

hoj=ojweb('http://acm.hit.edu.cn/hoj/system/login',[('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64)')],({'user':'minitestcoder','password':'0903106test',
                       'submit':'Login'}),'http://acm.hit.edu.cn/hoj/problem/submit',[('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64)')],({'Proid':'','Language':'','Source':''}),
          'http://acm.hit.edu.cn/hoj/problem/status?author=minitestcoder','waitre',[2,3,5,8,11],'hoj')

zoj=ojweb('http://acm.zju.edu.cn/onlinejudge/login.do',[('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64)')],({'handle':'minitestcoder','password':'0903106test'}),
          'http://acm.zju.edu.cn/onlinejudge/submit.do',[('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64)')],({'problemId':'','languageId':'','source':''}),
          'http://acm.zju.edu.cn/onlinejudge/showRuns.do?contestId=1','waitre',[3,6,9,12],'zoj')

hduoj=ojweb('http://acm.hdu.edu.cn/userloginex.php?action=login',[('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64)')],({'username':'minitestcoder','userpass':'0903106test','login':'Sign In'}),'http://acm.hdu.edu.cn/submit.php?action=submit',[('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64)')],({'check':'','problemid':'','language':'','usercode':''}),'http://acm.hdu.edu.cn/status.php?first=&pid=&user=MINItestcoder&lang=0&status=0','waitre',[4,8,7,12,11],'hduoj')

def main():
  while True:
    conn.commit()
    cursor.execute('select * from VJudgeQueue')
    mission=cursor.fetchone()
    #print mission
    if mission == None:
      time.sleep(2)
      #print 'a'
      continue
    #print 'b'
    submissionid=mission
    cursor.execute('select * from VSubmission where SubmissionID = %d'%(submissionid))
    vj=cursor.fetchone()
    #print submissionid,vj
    code=open('./%d.c'%(submissionid),'r')
    submitcode=code.read()
    code.close()
    #print submitcode
    proid=vj[1]
    lanid=vj[-3]
    ojid=vj[2]
    date=vj[3]
    usrname=vj[-1]
    #print proid,lanid,ojid,date,usrname
    pojlan=['G++','GCC','Java','Pascal','C++','C','Fortran']
    hduojlan=['G++','GCC','C++','C','Pascal','Java']
    zojlan=['C','C++','FPC','Java','Python','Perl','Scheme','PHP']
    if ojid == 'poj':
      vjojweb=poj
      for i in xrange(0,len(pojlan)) :
       if pojlan[i]==lanid :
         vjojweb.updatesubmitbody({'problem_id':proid,'language':i,'source':submitcode,'submit':'Submit'})
         break
    if ojid == 'zoj':
      vjojweb=zoj
      for i in xrange(0,len(zojlan)) :
       if zojlan[i]==lanid :
         vjojweb.updatesubmitbody({'problemId':str(int(proid)-1000),'languageId':i+1,'source':submitcode})
         break
    if ojid == 'hduoj':
      vjojweb=hduoj
      for i in xrange(0,len(hduojlan)) :
       if hduojlan[i]==lanid :
         vjojweb.updatesubmitbody({'check':'0','problemid':proid,'language':i,'usercode':submitcode})
         break
    #print vjojweb.submitbody
    #print vjojweb.other
    judgeresult=vjudge(vjojweb)
    print judgeresult
    cursor.execute('update VSubmission set Status = "%s" , Runtime = "%s" , Runmem = "%s" where SubmissionID = %s'%(judgeresult[0],judgeresult[2],judgeresult[1],submissionid[0]))
    conn.commit()
    cursor.execute('delete from VJudgeQueue where SubmissionID = %s'%(submissionid) )       
    conn.commit()


def vjudge(vjojweb):    
  #print vjojweb.other
  cj=cookielib.CookieJar()
  opener=urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
  opener.addheaders=vjojweb.loginheaders
  urllib2.install_opener(opener)
  req=urllib2.Request(vjojweb.loginurl,urllib.urlencode(vjojweb.loginbody))
  rehtml=urllib2.urlopen(req)
  #print rehtml.read()
  submitopener=urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
  submitopener.addheaders=vjojweb.submitheaders
  urllib2.install_opener(submitopener)
  submitreq=urllib2.Request(vjojweb.submiturl,urllib.urlencode(vjojweb.submitbody))
  #print submitreq
  if vjojweb.other == 'hduoj':
    statushtml=urllib2.urlopen(submitreq)
    status=statushtml.read()
    status=getfullstr(status)
    rem=re.search(r'<tdheight=22px>([0-9]+)</td><td>(.*)>MINItest</a></td>',status)
    runid=rem.group(1)
  if vjojweb.other == 'poj':
    statushtml=urllib2.urlopen(submitreq)
    status=statushtml.read()
    status=getfullstr(status)
    rem=re.search(r'<td>([0-9]+)</td>(.*?)user_id=minitestcoder>minitestcoder</a></td><td>',status)
    runid=rem.group(1)
  if vjojweb.other == 'hoj':
    statushtml=urllib2.urlopen('http://acm.hit.edu.cn/hoj/problem/status')
    status=statushtml.read()
    status=getfullstr(status)
    rem=re.search(r'<tdalign=(.*)http://acm.hit.edu.cn/hoj/status/run?id=([0-9]+)(.*)minitestcoder</a></td>',status)
  if vjojweb.other == 'zoj':
    statushtml=urllib2.urlopen(submitreq)
    status=statushtml.read()
    status=getfullstr(status)
    rem=re.search(r'Yoursourcehasbeensubmitted.Thesubmissionidis<fontcolor=(.*)>([0-9]+)</font>.Pleasecheck',status)
    runid=rem.group(2)
  #print status
  print runid
  while True :
    time.sleep(2)
    if vjojweb.other == 'zoj':
      res=urllib2.urlopen('http://acm.zju.edu.cn/onlinejudge/showRuns.do?contestId=1&search=true&firstId=-1&lastId=-1&problemCode=&handle=&idStart='+runid+'&idEnd='+runid)
    else:
      res=urllib2.urlopen(vjojweb.searchurl)
    resu=res.read()
    #print resu
    if vjojweb.other == 'poj':
      vjojweb.updatesearchre(r'<td>'+runid+r'</td>(.*?)user_id=minitestcoder>minitestcoder</a>(.*?)color=(.*?)>(.*?)</font>(.*?)</td><td>(.*?)</td><td>(.*?)</td><td>(.*?)</td><td>(.*?)</td><td>')
    if vjojweb.other == 'hduoj':
      vjojweb.updatesearchre(r'<tdheight=22px>'+runid+r'</td><td>(.*?)</td><td>(.*?)<fontcolor=(.*?)>(.*?)</font>(.*?)</td><td>(.*?)</a></td><td>(.*?)</td><td>(.*?)</td><td>(.*?)target=(.*?)>(.*?)</td><td>(.*?)</td>(.*?)MINItest</a></td>')
    if vjojweb.other == 'hoj':
      vjojweb.updatesearchre(r'http://acm.hit.edu.cn/hoj/status/log?id='+runid+r'(.*)>(.*)</a></td>(.*)<td align=(.*)>(.*)</td>(.*)<td align=(.*)>(.*)</td>(.*)<td align=(.*)>(.*)</td>(.*)<td align=')
    if vjojweb.other == 'zoj':
      vjojweb.updatesearchre(runid+r'</td>(.*?)<spanclass=(.*?)judge(.{7,90})>(.*?)<(.*?)/span></td>(.*?)target(.*?)>(.*?)</a></td>(.*?)class=(.*?)>(.*?)</td>(.*?)class=(.*?)>(.*?)</td>(.*?)minivjoj')
    resu=getfullstr(resu)
    #print resu
    resum=re.search(vjojweb.searchre,resu)
    #print resum
    if vjojweb.other == 'zoj':
        result=[resum.group(4).split()[0],resum.group(14),resum.group(11),resum.group(8)]
    else:
        result=[resum.group(vjojweb.searchresult[0]),resum.group(vjojweb.searchresult[1]),resum.group(vjojweb.searchresult[2]),resum.group(vjojweb.searchresult[3]),resum.group(vjojweb.searchresult[4])]
    if result[0] not in ('Waiting','Compiling','Running','Running & Judging','Running&Judging','Queuing') :
      return result
    print result

def getfullstr(ss):
  rs=ss.split()
  rr=''
  for i in xrange(0,len(rs)):
    rr=rr+rs[i]
  return rr

main()

#zojce http://acm.zju.edu.cn/onlinejudge/showJudgeComment.do?submissionId=2959853


