#include <iostream>  
#include <algorithm>  
#include <vector>  
#include <iterator>  

using namespace std;  

int main ()   
{  
  int x = 1;  
  vector<int> myvector(5, x);    

  //这里打印仅仅是元素的个数不是内存大小  
  cout << "myvector size:"  
      << myvector.size()  
      << endl;  
  for (int i=0; i<myvector.size(); i++) {
      cout<<"before i:"<<i<<"  "<<myvector[i]<<endl;
  
  }

  //swap交换函数释放内存：vector<T>().swap(X);  
  //T:int ; myvertor代表X  
  //vector<int>().swap(myvector);  
  vector<int> swapVec(10, 2);    
  swapVec.swap(myvector);

  //两个输出仅用来表示swap前后的变化  
  cout << "after swap :"  
      << myvector.size()  <<"swapVec:"<<swapVec.size()
      << endl;  

  return 0;  
}  
