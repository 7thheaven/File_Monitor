#include <stdio.h>
#include <unistd.h>
#include <sys/inotify.h>
#include <time.h>
#include <dirent.h>
#include <string.h>
#define MAX_BUF_SIZE 1024

int inofd,inolen,inoindex,inonum=0,inowd[1024];
char inopath[1024][128];

void showtime()
{
	time_t xtime;
	char timetemp[64];
	xtime=time(0);
	strftime(timetemp,sizeof(timetemp),"%Y/%m/%d %X %A",localtime(&xtime));
	printf("%s\n",timetemp);
}

void showpro(char * temp)
{
	FILE* fusermem;
	char mem[1024];
	int pidque[128];
	int itpid,i,pnum,inttemp,flag;
	fusermem=popen(temp,"r");
	fread( mem, sizeof(char), sizeof(mem), fusermem);
	inttemp=strlen(mem);
	pnum=itpid=flag=0;
	for(i=0;i<inttemp;++i)
	{
		if(flag && mem[i]>='0' && mem[i]<='9')
			itpid=itpid*10+mem[i]-'0';
		if(mem[i]==' ')
		{
			flag=1;
			if(itpid)
			{
				pidque[++pnum]=itpid;
				itpid=0;
			}
		}
	}
	if(itpid)
		pidque[++pnum]=itpid;
	pclose(fusermem);
	if(!pnum)
		printf("0 system ");
	else
	{
		printf("%d ",pnum);
		for(i=1;i<=pnum;++i)
		{
			sprintf(temp,"/proc/%d/exe",pidque[i]);
			inttemp=readlink(temp,mem,128);
			if(inttemp>=0)
				printf("%s ",mem);
		}
	}
}

int getmywd(int a)
{
	int i;
	for(i=0;i<inonum;++i)
		if(inowd[i]==a)
			return i;
	return -1;
}

void recursivewatch(char * dir)
{
	struct dirent *dent;
	DIR *odir;
	if((odir=opendir(dir))==NULL)
        {
                printf("Error:fail to open %s\n",dir);
                return;
        }
	//printf("%s\n",dir);
	inowd[inonum++]=inotify_add_watch(inofd,dir,IN_CLOSE | IN_CREATE | IN_MODIFY | IN_OPEN | IN_DELETE | IN_MOVE | IN_ACCESS);
	sprintf(inopath[inonum-1],"%s",dir);
	if(inowd[inonum-1] < 0)
	{
		printf("Error : Can't add watch for %s",dir);
		return;
	}
        while((dent=readdir(odir))!=NULL)
        {
                if(strcmp(dent->d_name,".")==0||strcmp(dent->d_name,"..")==0)
                        continue;
                if(dent->d_type==DT_DIR)
                {
			if(dent->d_name[0]=='.')
				continue;
			//printf("%s\n",dent->d_name);
                        sprintf(inopath[inonum],"%s%s/",dir,dent->d_name);
			recursivewatch(inopath[inonum]);
                }
        }
}


int main(int argc, char *argv[])
{
	printf("%d\n",getpid());
	fflush(stdout);
	freopen("/home/log.txt","w",stdout);
	printf("%d\n",getpid());
	fflush(stdout);
	char buffer[1024],temp[128];
	int myindex=-1;
	struct inotify_event *inoevent;
	//char *path="/home/heaven/excalibur/test/";
	char *path=argv[1];
	char *res=argv[2];
	inofd = inotify_init();
	if(inofd < 0)
	{
		printf("Error : Failed to initialize inotify.\n");
		return -1;
	}
	inonum=0;
	if(res[0]=='0')
	{
		inowd[inonum++]=inotify_add_watch(inofd,path,IN_CLOSE | IN_CREATE | IN_MODIFY | IN_OPEN | IN_DELETE | IN_MOVE | IN_ACCESS);
		sprintf(inopath[0],"%s",path);
		if(inowd[0] < 0)
		{
			printf("Error : Can't add watch for %s", path);
			return -1;
		}
	}
	if(res[0]=='1')
	{
		recursivewatch(path);
	}
	while(inolen = read(inofd, buffer, MAX_BUF_SIZE))
	{
		inoindex = 0;
		while(inoindex < inolen)
		{
			inoevent = (struct inotify_event *)(buffer+inoindex);
			myindex=getmywd(inoevent->wd);
			if(myindex==-1)
				continue;
			if(inoevent -> mask & IN_CREATE)
			{
				printf("%s%s create ",inopath[myindex],inoevent -> name);
				sprintf(temp,"fuser %s/%s",inopath[myindex],inoevent ->name);
				showpro(temp);
				showtime();
				fflush(stdout);
			}
			if(inoevent -> mask & IN_OPEN)
			{
				printf("%s%s open ",inopath[myindex],inoevent -> name);
				sprintf(temp,"fuser %s/%s",inopath[myindex],inoevent ->name);
				showpro(temp);
				showtime();
				fflush(stdout);
			}
			if(inoevent -> mask & IN_ACCESS)
			{
				printf("%s%s read ",inopath[myindex],inoevent -> name);
				sprintf(temp,"fuser %s/%s",inopath[myindex],inoevent ->name);
				showpro(temp);
				showtime();
				fflush(stdout);
			}
			if(inoevent -> mask & IN_MODIFY)
			{
				printf("%s%s write ",inopath[myindex],inoevent -> name);
				sprintf(temp,"fuser %s/%s",inopath[myindex],inoevent ->name);
				showpro(temp);
				showtime();
				fflush(stdout);
			}
			if(inoevent -> mask & IN_DELETE)
			{
				printf("%s%s delete ",inopath[myindex],inoevent -> name);
				sprintf(temp,"fuser %s/%s",inopath[myindex],inoevent ->name);
				showpro(temp);
				showtime();
				fflush(stdout);
			}
			if(inoevent -> mask & IN_MOVE)
			{
				printf("%s%s move ",inopath[myindex],inoevent -> name);
				sprintf(temp,"fuser %s/%s",inopath[myindex],inoevent ->name);
				showpro(temp);
				showtime();
				fflush(stdout);
			}
			if(inoevent -> mask & IN_CLOSE)
			{
				printf("%s%s close ",inopath[myindex],inoevent -> name);
				sprintf(temp,"fuser %s/%s",inopath[myindex],inoevent ->name);
				showpro(temp);
				showtime();
				fflush(stdout);
			}
			inoindex += sizeof(struct inotify_event)+inoevent->len;
		}
	}
	return 0;
}

