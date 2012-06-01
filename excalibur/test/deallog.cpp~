#include <iostream>
#include <cstdio>
#include <string>
#include <map>
using namespace std;
int main()
{
	int i,j,test;
	map<string,int> log;
	string abc;
	freopen("/home/heaven/log.txt","r",stdin);
	freopen("/home/heaven/stdlog.txt","w",stdout);
	while(getline(cin,abc))
	{
		if(abc=="")
		continue;
		if(log.count(abc)==0)
                {
			j=abc.length();
			test=0;
			for(i=0;i<j;++i)
			if(abc[i]<32||abc[i]>128)
			{
				test=1;
				break;
			}
			if(test)
			continue;
			cout<<abc<<endl;
			log[abc]=log.size();
		}
	}
	return 0;
}
