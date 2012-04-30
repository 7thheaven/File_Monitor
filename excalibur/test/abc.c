//#define   __LIBRARY__
#include <stdio.h>
#include <unistd.h>
#include <fcntl.h>

int main(int argc,char *argv[])
{
	printf("%d\n",argc);
	//printf("%d\n",O_CREAT|O_TRUNC|O_RDWR);
	return 0;
}
