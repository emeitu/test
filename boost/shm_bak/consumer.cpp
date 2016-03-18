#include "ShmMap.h"
#include <iostream>

int main ()
{
   using namespace boost::interprocess;
 
   ShmMapHelper<int,float> helper("MySharedMemory");
   ShmMapHelper<int,float>::MapType* mymap2 = helper.GetMap("MyMap");
   if(mymap2==NULL) 
   {
       std::cout<<"not find MyMap in MySharedMemory!"<<std::endl;
       return 1;
   }


   //helper.UnLock();
   //helper.Lock();
   for(ShmMapHelper<int,float>::MapType::iterator i = mymap2->begin();
       i != mymap2->end(); ++i)
   {
      std::cout<<i->first<<"==>"<<i->second<<std::endl;
   }
   //helper.UnLock();

   return 0;
}
