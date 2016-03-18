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

#if 0 
   ShmMapHelper<int,ProcessInfo> helper("MySharedMemory");
   ShmMapHelper<int,ProcessInfo>::MapType* mymap = helper.CreateMap("MyMap");
   std::cout<<"mymap:"<<mymap<<std::endl;

   ShmMapHelper<int,ProcessInfo>::MapType* mymap1 = helper.CreateMap("MyMap");
   std::cout<<"mymap1:"<<mymap1<<std::endl;

   //Insert data in the map
   for(int i = 0; ; ++i){
    //helper.Lock();
    //(*mymap)[i%100] = i%17;
    ProcessInfo p(i+1); 
    (*mymap)[i] = p;
    //helper.UnLock();
   }
#else  
   ShmMapHelper<int,ProcessInfo> *helper = new  ShmMapHelper<int, ProcessInfo>("MySharedMemory");
   ShmMapHelper<int,ProcessInfo>::MapType* mymap = helper->CreateMap("MyMap");
   std::cout<<"mymap:"<<mymap<<std::endl;
   //Insert data in the map
   for(int i = 0; ; ++i){
    //helper.Lock();
    //(*mymap)[i%100] = i%17;
    ProcessInfo p(i); 
    (*mymap)[i] = p;
    //helper.UnLock();
   }

#endif
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

