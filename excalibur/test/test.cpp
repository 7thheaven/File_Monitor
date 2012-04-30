#include <iostream>
#include <cstdio>
#include <string>
using namespace std;
int main()
{
	char abc;
	freopen("testin.txt","r",stdin);
	freopen("testout.txt","w",stdout);
	while((abc=getchar())!=EOF)
	cout<<abc;
	while(1);
	return 0;
}
