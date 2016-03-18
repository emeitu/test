#ifndef    SHARED_MEMORY_MAP_HELPER
#define SHARED_MEMORY_MAP_HELPER

#include <boost/interprocess/managed_shared_memory.hpp>
#include <boost/interprocess/containers/map.hpp>
#include <boost/interprocess/allocators/allocator.hpp>

#include <boost/interprocess/sync/scoped_lock.hpp>
#include <boost/interprocess/sync/named_recursive_mutex.hpp>

#include <functional>
#include <utility>
#include <string>

template <typename KeyType, typename MappedType>
class ShmMapHelper
{
public:
    typedef std::pair<const KeyType,MappedType> ValueType;
    typedef boost::interprocess::allocator<ValueType, boost::interprocess::managed_shared_memory::segment_manager> ShmemAllocator;
    typedef boost::interprocess::map<KeyType, MappedType, std::less<KeyType>, ShmemAllocator> MapType;
public:
    MapType* CreateMap(const char* MapName)
    {
        ShmemAllocator alloc_inst(segment.get_segment_manager());
        MapType* map = segment.construct<MapType>(MapName)(std::less<KeyType>(),alloc_inst);
        return map;
    }

    MapType* GetMap(const char* MapName)
    {
        MapType* map = segment.find<MapType>(MapName).first;
        return map;
    }
public:
    ShmMapHelper(const char* shared_memory_name = "MySharedMemory", int shared_memory_size= 100000000, const char* mutex_name=ShmMapConfig::GetSharedMutexName())
    : segment(boost::interprocess::open_or_create, shared_memory_name, shared_memory_size),
    mutex(boost::interprocess::open_or_create, mutex_name)
    {
        is_locked = false;
    }
    ~ShmMapHelper()
    {
        UnLock();
    }
public:
    void Lock()
    {
        if(!is_locked)
        {
            mutex.lock();
            is_locked = true;
        }
    }
    void UnLock()
    {
        if(is_locked)
        {
            mutex.unlock();
            is_locked = false;
        }
    }
private:
    boost::interprocess::managed_shared_memory segment;
    boost::interprocess::named_recursive_mutex mutex;
    bool is_locked;
};

void RemoveShmMap();

enum SharedMapOpErrorCode
{
    MAP_OP_OK = 0,
    MAP_NOT_FOUND = -1,
    KEY_NOT_FOUND = -2,
    NO_MORE_MEMORY = -3,
    INVALID_PARAM = -4,
};

template <typename Type> 
int Get(const char* map_name, int key, Type& info)
{
    typedef typename ShmMapHelper<int, Type>::MapType MapType;
    int return_code = MAP_OP_OK;
    ShmMapHelper<int, Type> helper;
    helper.Lock();
    MapType* map = helper.GetMap(map_name);
    if(map!=NULL)
    {
        typedef typename MapType::iterator iterator;
        iterator i = map->find(key);
        if(i != map->end())
        {
            info = i->second;
            return_code = MAP_OP_OK;
        }
        else
        {
            return_code = KEY_NOT_FOUND;
        }
    }
    else
    {
        return_code = MAP_NOT_FOUND;
    }
    helper.UnLock();
    return return_code;
}

template <typename Type>
int Set(const char* map_name, int key, const Type& info)
{
    typedef typename ShmMapHelper<int, Type>::MapType MapType;
        int return_code = MAP_OP_OK;
        ShmMapHelper<int, Type> helper;
        helper.Lock();
        MapType* map = helper.GetMap(map_name);
        if(map!=NULL)
        {
        try{
            (*map)[key] = info;
        }
        catch(...)
        {
            return_code = NO_MORE_MEMORY;
        }
        }
        else
        {
                return_code = MAP_NOT_FOUND;
        }
        helper.UnLock();
        return return_code;
}

#endif

