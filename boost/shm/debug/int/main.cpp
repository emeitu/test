//#include "ShmMap.h"
#include <iostream>
#include <unistd.h>
#include <memory>

   //Remove shared memory on construction and destruction
  struct shm_remove
   {
    public:
      shm_remove() { 
        std::cout<<"gou zao==>"<<std::endl;
      }
      ~shm_remove(){ 
        std::cout<<"xi gou==>"<<std::endl;
      }
   };

int main ()
{

   std::auto_ptr<shm_remove> remove(new shm_remove);

   return 0;
}

