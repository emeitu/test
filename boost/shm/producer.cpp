#include "ShmMap.h"
#include <iostream>
#include <unistd.h>
#include <memory>
#include "ProcessInfo.h"

   using namespace boost::interprocess;
 struct shm_remove
 {
    shm_remove() { 
      std::cout<<"gou zao==>"<<std::endl;
      shared_memory_object::remove("MySharedMemory"); 
    }
    ~shm_remove(){ 
      std::cout<<"xi gou==>"<<std::endl;
      shared_memory_object::remove("MySharedMemory"); }
 } ;


int main ()
{

 //Remove shared memory on construction and destruction

   //remover;
   //std::auto_ptr<shm_remove> remove(new shm_remove);


  std::cout<<"get char to remove shareM"<<std::endl;
  getchar();
      shared_memory_object::remove("MySharedMemory"); 
  getchar();
  std::cout<<"get char to create shareM"<<std::endl;

   //ShmMapHelper<int,float> helper("MySharedMemory");
   //ShmMapHelper<int,float>::MapType* mymap = helper.CreateMap("MyMap");

 
   ShmMapHelper<int,ProcessInfo> helper("MySharedMemory");
  std::cout<<"get1"<<std::endl;
   ShmMapHelper<int,ProcessInfo>::MapType* mymap = helper.CreateMap("MyMap");
  std::cout<<"get2"<<std::endl;
   //Insert data in the map
   for(int i = 0; ; ++i){
  std::cout<<"get3"<<std::endl;
    //helper.Lock();
    //(*mymap)[i%100] = i%17;
    ProcessInfo p(i+1); 
    (*mymap)[i] = p;
    //helper.UnLock();
   }
  std::cout<<"get4"<<std::endl;

/*
   ShmMapHelper<int,float>::MapType* mymap2 = helper->GetMap("MyMap");
   for(ShmMapHelper<int,float>::MapType::iterator i = mymap2->begin();
    i != mymap2->end(); ++i)
   {
      std::cout<<i->first<<"==>"<<i->second<<std::endl;
   }
*/

   return 0;
}

