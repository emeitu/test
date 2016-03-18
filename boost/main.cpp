/*************************************************************************
  > File Name: main.cpp
  > Author: 
  > Mail: 
  > Created Time: Mon 20 Apr 2015 06:06:04 PM CST
 ************************************************************************/

#include<iostream>
using namespace std;

#include <boost/program_options.h>

#include <string>

#include <iostream>

#pragma hdrstop

int main(int argc, char* argv[]){

    using std::string;

    using std::cout;

    using std::endl;

    namespace po = boost::program_options;

    po::options_description desc("My Commnad Line");

    desc.add_options()

        ("help,h", "help message")

        ("author,a", "Author")

        ("string,s", po::value<string>(),"run as client and connect to the specified IP")

        ("int,i", po::value<int>(), "the number of concurrent connections")

        ;

    po::variables_map vm;

    try{

        po::store( po::command_line_parser(argc, argv).options(desc).allow_unregistered().run(), vm);

        po::notify(vm);

        if (vm.count("author")) {

            cout << "Author: Chui-Wen Chiu" << endl;

            cout << "Blog: http://chuiwenchiu.spaces.live.com" << endl;

        }

        f (vm.count("help")) {

            cout << desc << endl;

            return 1;

        }
        if(vm.count("string")) {

            string sip = vm["string"].as<string>();

            cout << "string: " << sip << endl;

            // connect to server...

        }
        f(vm.count("int")) {

            int t = vm["int"].as<int>();

            cout << "int: " << t << endl;
        }

    }catch(boost::program_options::invalid_command_line_syntax&){

        cout << "參數語法錯誤" << endl;

        cout << desc << endl;

    }catch(boost::bad_lexical_cast&){

        cout << "參數型別錯誤" << endl;

        cout << desc << endl;

    }catch(...){

        cout << "ERROR" << endl;

    }

    return 0;

}
