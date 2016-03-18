#include "ShmMap.h"
#include <iostream>
#include <unistd.h>

int main ()
{
   using namespace boost::interprocess;

   //Remove shared memory on construction and destruction
   struct shm_remove
   {
      shm_remove() { shared_memory_object::remove("MySharedMemory"); }
      ~shm_remove(){ shared_memory_object::remove("MySharedMemory"); }
   } remover;
 
   ShmMapHelper<int,float> helper("MySharedMemory");
   ShmMapHelper<int,float>::MapType* mymap = helper.CreateMap("MyMap");
   //Insert data in the map
   for(int i = 0; ; ++i){
    helper.Lock();
    (*mymap)[i%100] = i%17;
    helper.UnLock();
   }

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

