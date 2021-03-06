#!/usr/bin/env python
import wx,commands,os,subprocess
import wx.grid
import wx.lib.dialogs
filepath=""
pid=0
rownum=0
dirfile=0
watchpro=""
colLabels=("Filename","Event","Relates","Processname","Time")

def refresh(event):
	global filepath
	global pid
	global dirfile
	global colLabels
	global rownum
	global watchpro
	pos=face.GetSize()
	for col in xrange(5):
		reslog.SetColLabelValue(col,colLabels[col])
		reslog.SetColSize(col,(pos.x-85)/5)
	if pathname.GetValue()=="":
		if proname.GetValue()=="":
			face.Refresh()
			return
		if watchpro!=proname.GetValue():
			watchpro=proname.GetValue()
			if pid!=0:
				y=os.system("kill %s"%pid)
				if y!=0:
					print "kill %s unsuccessfully!"%pid
				else:
					print "kill %s Done."%pid
					pid=0
					filepath=""
			x="/home/heaven/excalibur/ava /home/heaven/excalibur/ 1 &"
			recur.SetValue(True)
			watchclass.SetStringSelection('Dir')
			dirfile=0
			y=os.system(x)
			if y!=0:
				print "Error during run ava."
	if pathname.GetValue()!="" and filepath!=pathname.GetValue():
		print "New watch."
		filepath=pathname.GetValue()
		if filepath[-1]=='/':
			watchclass.SetStringSelection('Dir')
			dirfile=0
		else:
			watchclass.SetStringSelection('File')
			dirfile=1
			recur.SetValue(False)
		if pid!=0:
			y=os.system("kill %s"%pid)
			if y!=0:
				print "kill %s unsuccessfully!"%pid
			else:
				print "kill %s Done."%pid
				pid=0
				filepath=""
		if dirfile==0:
			if recur.GetValue():
				x="/home/heaven/excalibur/ava %s 1 &"%(filepath)
			else:
				x="/home/heaven/excalibur/ava %s 0 &"%(filepath)
		else:
			pathlen=len(filepath)
			for i in xrange(pathlen):
				if filepath[i]=='/':
					index=i
			x="/home/heaven/excalibur/ava %s 0 &"%(filepath[:index+1])
		y=os.system(x)
		if y!=0:
			print "Error during run ava."
		#z=os.popen(x).readlines();
		#z = subprocess.Popen(["/home/heaven/excalibur/test/ava","%s"%filepath,"&"],stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
		#y,z=commands.getstatusoutput(x)
		#print "here"
	y=os.system("/home/heaven/excalibur/deallog")
	if y!=0:
		print "Error during run deallog."
	logfile=open("/home/stdlog.txt","r")
	logtemp=logfile.readlines()
	#if logtemp:
	#	pid=logtemp[0]
	#	print "ava pid is",pid
	#	logtext.SetValue("".join(logtemp[1:]))
	if logtemp:
		pid=logtemp[0]
		print "ava pid is",pid
		rownum=len(logtemp)-1
		ignorenum=0
		watchpro=proname.GetValue()
		for row in xrange(rownum):
			if watchpro!="":
				if logtemp[row+1].split()[3]!=watchpro:
					ignorenum=ignorenum+1
					continue
			if dirfile==1:
				if logtemp[row+1].split()[0]!=filepath:
					ignorenum=ignorenum+1
					continue
			for col in xrange(5):
				if col==4:
					reslog.SetCellValue(row-ignorenum, col, "%s" % " ".join(logtemp[row+1].split()[col:]))
				else:
					reslog.SetCellValue(row-ignorenum, col, "%s" % (logtemp[row+1].split()[col]))
	face.Refresh()
	logfile.close()

def clear(event):
	global pid
	global rownum
	global filepath
	if pid!=0:
		y=os.system("kill %s"%pid)
		if y!=0:
			print "kill %s unsuccessfully!"%pid
		else:
			print "kill %s Done."%pid
			pid=0
			filepath=""
			for row in xrange(rownum):
				for col in xrange(5):
					reslog.SetCellValue(row, col,"")	

def browser(event):
	global filepath
	wclass=watchclass.GetStringSelection()
	if wclass=="Dir":
		dlg=wx.DirDialog(bkg,u"select",style=wx.DD_DEFAULT_STYLE | wx.DD_DIR_MUST_EXIST)
		if dlg.ShowModal() == wx.ID_OK:
			path=dlg.GetPath()
			pathname.SetValue(path+"/")
	if wclass=="File":
		dlg=wx.FileDialog(bkg,u"select",style=wx.DD_DEFAULT_STYLE | wx.DD_DIR_MUST_EXIST)
		if dlg.ShowModal() == wx.ID_OK:
			path=dlg.GetPath()
			pathname.SetValue(path)
	if wclass=="Process":
		dlg=wx.FileDialog(bkg,u"select",style=wx.DD_DEFAULT_STYLE | wx.DD_DIR_MUST_EXIST)
		if dlg.ShowModal() == wx.ID_OK:
			path=dlg.GetPath()
			proname.SetValue(path)

def help(event):
	helpfile=open("/home/heaven/excalibur/help.txt","r")
	helptemp=helpfile.read()
	helpfile.close()
	mpos=face.GetPosition()
	msize=face.GetSize()
	mpos.x=mpos.x+msize.x/4
	mpos.y=mpos.y+msize.y/4
	msize.x=msize.x/2
	msize.y=msize.y/2
	about=wx.lib.dialogs.ScrolledMessageDialog(bkg,helptemp,'Help&About',pos=mpos,size=msize)
	#about=wx.MessageDialog(bkg,helptemp,'Help&About',wx.OK|wx.ICON_QUESTION) 
	about.ShowModal()

fm=wx.App()
face=wx.Frame(None,title="File_Monitor",size=(800,600))
bkg=wx.Panel(face)
filelabel=wx.StaticText(bkg,wx.NewId(),'Path:')
prolabel=wx.StaticText(bkg,wx.NewId(),'Process:')
watchclass=wx.RadioBox(bkg,-1,"WatchClass:",(0,0),(100,40),['Dir','File','Process'],0,wx.RA_SPECIFY_COLS)
browserbutton=wx.Button(bkg,label='Browser')
browserbutton.Bind(wx.EVT_BUTTON,browser)
refreshbutton=wx.Button(bkg,label='Refresh')
refreshbutton.Bind(wx.EVT_BUTTON,refresh)
recur=wx.CheckBox(bkg,-1,"Recursive")
clearbutton=wx.Button(bkg,label='Clear')
clearbutton.Bind(wx.EVT_BUTTON,clear)
helpbutton=wx.Button(bkg,label='Help')
helpbutton.Bind(wx.EVT_BUTTON,help)
pathname=wx.TextCtrl(bkg)
proname=wx.TextCtrl(bkg)
#logtext=wx.TextCtrl(bkg,style=wx.TE_MULTILINE|wx.HSCROLL)             
reslog=wx.grid.Grid(bkg)
pos=face.GetSize()
reslog.CreateGrid(1000,5)
for col in xrange(5):
	reslog.SetColLabelValue(col,colLabels[col])
	reslog.SetColSize(col,(pos.x-85)/5)
hbox1=wx.BoxSizer()
hbox2=wx.BoxSizer()
hbox1.Add(filelabel,proportion=1,flag=wx.EXPAND)
hbox1.Add(pathname,proportion=6,flag=wx.EXPAND)
hbox1.Add(watchclass,proportion=4,flag=wx.EXPAND)
hbox2.Add(prolabel,proportion=1,flag=wx.EXPAND)
hbox2.Add(proname,proportion=6,flag=wx.EXPAND)
hbox1.Add(browserbutton,proportion=2,flag=wx.EXPAND)
hbox1.Add(refreshbutton,proportion=2,flag=wx.EXPAND)
hbox2.Add(recur,proportion=4,flag=wx.EXPAND)
hbox2.Add(clearbutton,proportion=2,flag=wx.EXPAND)
hbox2.Add(helpbutton,proportion=2,flag=wx.EXPAND)
vbox=wx.BoxSizer(wx.VERTICAL)
vbox.Add(hbox1,proportion=0,flag=wx.EXPAND|wx.ALL,border=5)
vbox.Add(hbox2,proportion=0,flag=wx.EXPAND|wx.ALL,border=5)
#vbox.Add(logtext,proportion=1,flag=wx.EXPAND|wx.LEFT|wx.BOTTOM|wx.RIGHT,border=5)
vbox.Add(reslog,proportion=1,flag=wx.EXPAND|wx.ALL,border=5)
bkg.SetSizer(vbox)
face.Show()
fm.MainLoop()
