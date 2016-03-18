#include <iostream>
#include <memory>

using namespace std;

class Stu{
public:
  Stu()
  {
    cout<<"gou zao"<<endl;
  }    

  ~Stu()
  {
    cout<<"xi gou"<<endl;
  }
};


void func()
{
  auto_ptr<Stu> p(new Stu());
}
int main()
{
  func();
  while(true) {
    sleep(3);
  }


  return 0;
}
