/*************************************************************************
  > File Name: main.cpp
  > Author: 
  > Mail: 
  > Created Time: Tue 05 May 2015 11:14:55 AM CST
 ************************************************************************/

#include<iostream>
#include <string>
#include <boost/lexical_cast.hpp>

using namespace std;


template<class T> bool GetValue(const string & fvalue, T & tvalue) {
    try {
        tvalue = boost::lexical_cast<T>(fvalue);
        cout<<"tvalue:"<<tvalue<<endl;
    }
    catch (boost::bad_lexical_cast &) {
        return false;
    }
    return true;
}


int main(int argc, char *argv[])
{
    const char *first="";
    const char *second="56";
    string str(first,second);

    cout<<str.c_str()<<endl;


    string sss="2";
    string src="4";
    bool bl1 = 1;
    bool ret = GetValue(sss, bl1);

    cout<<"sss:"<<sss<<"bl1:"<<bl1<<"ret:"<<ret<<endl;

    string s("AAAAAAA");
    string slp("BBB");
    string sb("AAAAAAA");

    string a=s.replace(1,3,slp);
    string b=sb.replace(5,3,slp);

    cout<<"s:"<<s<<"\ta:"<<a<<endl;
    cout<<"sb:"<<sb<<"\tb:"<<b<<endl;
    string i= boost::lexical_cast<bool>(true);

cout<<"I:"<<i<<endl;

    return 0;
}

