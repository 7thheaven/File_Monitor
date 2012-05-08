#include <iostream>
#include <fstream>
#include <stdlib.h>
using namespace std;
int main()
{
	ifstream fin("./test/testin.txt");
	ofstream fout("./test/001.txt");
	string abc;
	int n;
	n=5;
	while(n--)
	{
		while(fin>>abc)
		{
			fout<<abc<<endl;
		}
		sleep(3);
	}
	fin.close();
	fout.close();
	ifstream finn("./test/001.txt");
	ofstream foutt("./test/002.txt");
	n=5;
	while(n--)
	{
		while(finn>>abc)
		{
			foutt<<abc<<endl;
		}
		sleep(3);
	}
	finn.close();
	foutt.close();
	system("rm /home/heaven/excalibur/test/002.txt");
	return 0;
}
