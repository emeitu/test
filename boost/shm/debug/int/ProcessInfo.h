#ifndef _ProcessInfo_H
#define _ProcessInfo_H

#include <pthread.h>

class ProcessInfo {
 public:
    int m_pid;
    pthread_mutex_t m_mutex;

    ProcessInfo(int pid) 
    {
      m_pid=pid;
      pthread_mutex_init(&m_mutex, NULL);
    }

    ProcessInfo() 
    {
      m_pid=-1;
      pthread_mutex_destroy(&m_mutex);
    }
};



#endif
