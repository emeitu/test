#include "ShmMap.h"
#include <cstring>

const char* ShmMapConfig::DEFAULT_SHARED_MEMORY_NAME = "MySharedMemory";
const char* ShmMapConfig::DEFAULT_SHARED_MUTEX_NAME = "MySharedMutex";
const int ShmMapConfig::MAX_NAME_LENGTH = 256;
const int ShmMapConfig::DEFAULT_SHARED_MEMORY_SIZE = 100000000;

std::string ShmMapConfig::name_prefix = "";
std::string ShmMapConfig::shared_memory_name = ShmMapConfig::DEFAULT_SHARED_MEMORY_NAME;
std::string ShmMapConfig::shared_mutex_name = ShmMapConfig::DEFAULT_SHARED_MUTEX_NAME;
int ShmMapConfig::shared_memory_size = ShmMapConfig::DEFAULT_SHARED_MEMORY_SIZE;

const char* ShmMapConfig::GetNamePrefix()
{
    return ShmMapConfig::name_prefix.c_str();
}

void ShmMapConfig::SetNamePrefix(const char* prefix)
{
    ShmMapConfig::name_prefix = prefix;
    ShmMapConfig::shared_memory_name = ShmMapConfig::name_prefix + ShmMapConfig::DEFAULT_SHARED_MEMORY_NAME;
    ShmMapConfig::shared_mutex_name = ShmMapConfig::name_prefix + ShmMapConfig::DEFAULT_SHARED_MUTEX_NAME;
}

int ShmMapConfig::GetSharedMemorySize()
{
    return ShmMapConfig::shared_memory_size;
}

void ShmMapConfig::SetSharedMemorySize(int size)
{
    ShmMapConfig::shared_memory_size = size;
}

const char* ShmMapConfig::GetSharedMemoryName()
{
    return ShmMapConfig::shared_memory_name.c_str();
}


const char* ShmMapConfig::GetSharedMutexName()
{
    return ShmMapConfig::shared_mutex_name.c_str();
}

void RemoveShmMap()
{
    boost::interprocess::shared_memory_object::remove(ShmMapConfig::GetSharedMemoryName());
    boost::interprocess::named_recursive_mutex::remove(ShmMapConfig::GetSharedMutexName());
}
