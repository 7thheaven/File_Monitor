#include <iostream>
#include <fstream>
#include <stdlib.h>
using namespace std;
int main()
{
	ifstream fin("./test/testin.txt");
	ofstream fout("./test/recurtest/007.txt");
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
	return 0;
}


