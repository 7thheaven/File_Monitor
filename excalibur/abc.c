#include <stdio.h>
#include <unistd.h>
#include <sys/inotify.h>
#include <time.h>
#include <dirent.h>
#include <string.h>

char inopath[1024][128];
int inonum=0;

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
        while((dent=readdir(odir))!=NULL)
        {
                if(strcmp(dent->d_name,".")==0||strcmp(dent->d_name,"..")==0)
                        continue;
                if(dent->d_type==DT_DIR)
                {
			if(dent->d_name[0]=='.')
				continue;
			//printf("%s\n",dent->d_name);
                        sprintf(inopath[inonum++],"%s%s/",dir,dent->d_name);
			recursivewatch(inopath[inonum-1]);
                }
        }
}

int main()
{
	char * dir="/home/heaven/";
	inonum=0;
	recursivewatch(dir);
	int i;	
	for(i=0;i<inonum;++i)
	{
		printf("%d %s\n",i,inopath[i]);
	}
	return 0;
}
