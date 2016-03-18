#include "ShmMap.h"
#include <iostream>
#include "ProcessInfo.h"

int main ()
{
   using namespace boost::interprocess;
   //ShmMapHelper<int,float> helper("MySharedMemory");
   //ShmMapHelper<int,float>::MapType* mymap2 = helper.GetMap("MyMap");

 
   ShmMapHelper<int,ProcessInfo> helper("MySharedMemory");
   ShmMapHelper<int,ProcessInfo>::MapType* mymap2 = helper.GetMap("MyMap");
   if(mymap2==NULL) 
   {
       std::cout<<"not find MyMap in MySharedMemory!"<<std::endl;
       return 1;
   }
   std::cout<<"MapType::"<<mymap2<<std::endl;

   //helper.UnLock();
   //helper.Lock();
   //for(ShmMapHelper<int,float>::MapType::iterator i = mymap2->begin();
   for(ShmMapHelper<int,ProcessInfo>::MapType::iterator i = mymap2->begin();
       i != mymap2->end(); ++i)
   {
      //std::cout<<i->first<<"==>"<<i->second<<std::endl;
      ProcessInfo p=i->second;
      std::cout<<i->first<<"==>"<<p.m_pid<<std::endl;
   }
   //helper.UnLock();

   return 0;
}
