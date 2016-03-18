#include <iostream>

using namespace std;

class Tmp
{
 public:
  Tmp(){
    cout<<"Tmp"<<endl;
  }

  ~Tmp() {
    cout<<"~~Tmp"<<endl;
  }

  virtual void init() {
    cout<<"~~Tmp init"<<endl;
  }

};

int main(int argc, char *argv[])
{
  Tmp::init() ; 


   return 0;
}
