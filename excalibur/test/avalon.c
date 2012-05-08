#include <stdio.h>
#include <unistd.h>
#include <sys/inotify.h>
#include <time.h>
#define MAX_BUF_SIZE 1024

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

int main(int argc, char *argv[])
{
	freopen("/home/heaven/log.txt","w",stdout);
	int inofd,inowd,inolen,inoindex;
	char buffer[1024],temp[128];
	struct inotify_event *inoevent;
	//char *path="/home/heaven/excalibur/test/";
	char *path=argv[1];
	inofd = inotify_init();
	if(inofd < 0)
	{
		printf("Failed to initialize inotify.\n");
		return -1;
	}
	inowd = inotify_add_watch(inofd,path,IN_CLOSE | IN_CREATE | IN_MODIFY | IN_OPEN | IN_DELETE | IN_MOVE | IN_ACCESS);
	if(inowd < 0)
	{
		printf("Can't add watch for %s", path);
		return -1;
	}
	while(inolen = read(inofd, buffer, MAX_BUF_SIZE))
	{
		inoindex = 0;
		while(inoindex < inolen)
		{
			inoevent = (struct inotify_event *)(buffer+inoindex);
			if(inoevent->wd != inowd)
				continue;
			if(inoevent -> mask & IN_CREATE)
			{
				printf("%s%s create ",path,inoevent -> name);
				sprintf(temp,"fuser %s/%s",path,inoevent ->name);
				showpro(temp);
				showtime();
				fflush(stdout);
			}
			if(inoevent -> mask & IN_OPEN)
			{
				printf("%s%s open ",path,inoevent -> name);
				sprintf(temp,"fuser %s/%s",path,inoevent ->name);
				showpro(temp);
				showtime();
				fflush(stdout);
			}
			if(inoevent -> mask & IN_ACCESS)
			{
				printf("%s%s read ",path,inoevent -> name);
				sprintf(temp,"fuser %s/%s",path,inoevent ->name);
				showpro(temp);
				showtime();
				fflush(stdout);
			}
			if(inoevent -> mask & IN_MODIFY)
			{
				printf("%s%s write ",path,inoevent -> name);
				sprintf(temp,"fuser %s/%s",path,inoevent ->name);
				showpro(temp);
				showtime();
				fflush(stdout);
			}
			if(inoevent -> mask & IN_DELETE)
			{
				printf("%s%s delete ",path,inoevent -> name);
				sprintf(temp,"fuser %s/%s",path,inoevent ->name);
				showpro(temp);
				showtime();
				fflush(stdout);
			}
			if(inoevent -> mask & IN_MOVE)
			{
				printf("%s%s move ",path,inoevent -> name);
				sprintf(temp,"fuser %s/%s",path,inoevent ->name);
				showpro(temp);
				showtime();
				fflush(stdout);
			}
			if(inoevent -> mask & IN_CLOSE)
			{
				printf("%s%s close ",path,inoevent -> name);
				sprintf(temp,"fuser %s/%s",path,inoevent ->name);
				showpro(temp);
				showtime();
				fflush(stdout);
			}
			inoindex += sizeof(struct inotify_event)+inoevent->len;
		}
	}
	return 0;
}

