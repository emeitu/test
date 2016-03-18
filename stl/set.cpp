/*************************************************************************
	> File Name: set.cpp
	> Author: 
	> Mail: 
	> Created Time: Mon 20 Apr 2015 03:54:38 PM CST
 ************************************************************************/

#include<iostream>
#include <set>
#include <string>
using namespace std;


int main()
{
    set<int> set1;
    set1.insert(5);
    set1.insert(4);
    if (set1.insert(6).second) {
        cout<<"insert 6 success"<<endl;
    }

    if (!set1.insert(6).second) {
        cout<<"insert 6 fail"<<endl;
    }

    for (set<int>::iterator p = set1.begin(); p!=set1.end(); ++p) {
        cout<<*p<<"  ";
    }
}
