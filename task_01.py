import random
import time
from functools import lru_cache
from collections import OrderedDict



def range_sum_no_cache(array, L, R):
    return sum(array[L:R+1])



def update_no_cache(array, index, value):
    array[index] = value



class LRUCache:
    def __init__(self, capacity: int):
        self.cache = OrderedDict()
        self.capacity = capacity

    def get(self, key):
        if key in self.cache:
            
            self.cache.move_to_end(key)
            return self.cache[key]
        return None

    def put(self, key, value):
        if key in self.cache:
            
            self.cache.move_to_end(key)
        else:
            
            if len(self.cache) >= self.capacity:
                self.cache.popitem(last=False)
        self.cache[key] = value

    def invalidate_keys(self, keys_to_invalidate):
        
        for key in keys_to_invalidate:
            if key in self.cache:
                del self.cache[key]



cache = LRUCache(capacity=1000)



def range_sum_with_cache(array, L, R):
    key = (L, R)  
    cached_result = cache.get(key)
    if cached_result is not None:
        return cached_result
    else:
        result = sum(array[L:R+1])
        cache.put(key, result)
        return result



def update_with_cache(array, index, value):
    array[index] = value
    
    keys_to_invalidate = [
        key for key in cache.cache.keys()
        if key[0] <= index <= key[1]
    ]
    cache.invalidate_keys(keys_to_invalidate)



def test_program():
   
    N = 100_000
    array = [random.randint(1, 100) for _ in range(N)]

   
    Q = 50_000
    queries = []
    for _ in range(Q):
        if random.random() < 0.7: 
            L = random.randint(0, N - 1)
            R = random.randint(L, N - 1)
            queries.append(('Range', L, R))
        else:  
            index = random.randint(0, N - 1)
            value = random.randint(1, 100)
            queries.append(('Update', index, value))

   
    start_no_cache = time.time()
    for query in queries:
        if query[0] == 'Range':
            _, L, R = query
            range_sum_no_cache(array, L, R)
        elif query[0] == 'Update':
            _, index, value = query
            update_no_cache(array, index, value)
    end_no_cache = time.time()
    time_no_cache = end_no_cache - start_no_cache

    
    start_with_cache = time.time()
    for query in queries:
        if query[0] == 'Range':
            _, L, R = query
            range_sum_with_cache(array, L, R)
        elif query[0] == 'Update':
            _, index, value = query
            update_with_cache(array, index, value)
    end_with_cache = time.time()
    time_with_cache = end_with_cache - start_with_cache

  
    print(f"Час виконання без кешу: {time_no_cache:.2f} секунд")
    print(f"Час виконання з кешем: {time_with_cache:.2f} секунд")



if __name__ == "__main__":
    test_program()
