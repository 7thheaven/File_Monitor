#include <iostream>
#include <cstdio>
#include <string>
using namespace std;
int main()
{
	char abc;
	int i,j=1,n;
	freopen("/home/heaven/excalibur/test/testin.txt","r",stdin);
	freopen("/home/heaven/excalibur/test/testout.txt","w",stdout);
	n=5;
	while(n--)
	{
	while((abc=getchar())!=EOF)
	cout<<abc;
	for(i=1;i<2000000000;++i)
	j*=i;
	cout<<j<<endl;
	}
	return 0;
}
