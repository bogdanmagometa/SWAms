import hazelcast
import multiprocessing as mp
import time

MAP_NAME = "map"
KEY = "1"
INIT_VAL = 0
NUM_INCREMENTS_PER_CLIENT = 1000
WTIME_SECONDS = 1e-2
NUM_CLIENTS = 3

def without_locks():
    hz_client = hazelcast.HazelcastClient()
    dm = hz_client.get_map(MAP_NAME).blocking()

    for _ in range(NUM_INCREMENTS_PER_CLIENT):
        val = dm.get(KEY)
        val += 1
        time.sleep(WTIME_SECONDS)
        dm.put(KEY, val)

    hz_client.shutdown()


def with_pessimistic_lock():
    hz_client = hazelcast.HazelcastClient()
    dm = hz_client.get_map(MAP_NAME).blocking()

    for _ in range(NUM_INCREMENTS_PER_CLIENT):
        dm.lock(KEY)
        try:
            val = dm.get(KEY)
            val += 1
            time.sleep(WTIME_SECONDS)
            dm.put(KEY, val)
        finally:
            dm.unlock(KEY)

    hz_client.shutdown()

def with_optimistic_lock():
    hz_client = hazelcast.HazelcastClient()
    dm = hz_client.get_map(MAP_NAME).blocking()

    for _ in range(NUM_INCREMENTS_PER_CLIENT):
        while True:
            old_val = dm.get(KEY)
            val = old_val + 1
            time.sleep(WTIME_SECONDS)
            replaced = dm.replace_if_same(KEY, old_val, val)
            if replaced:
                break

    hz_client.shutdown()

STRATEGIES = [
    ("Without locking", without_locks),
    ("With pessimistic lock", with_pessimistic_lock),
    ("With optimistic lock", with_optimistic_lock),
]

if __name__ == "__main__":
    ctx = mp.get_context('fork')

    hz_client = hazelcast.HazelcastClient()
    dm = hz_client.get_map(MAP_NAME).blocking()

    for strategy_name, strategy in STRATEGIES:
        dm.put(KEY, INIT_VAL)

        processes = [ctx.Process(target=strategy) for _ in range(NUM_CLIENTS)]

        start_timestamp = time.time()
        for proc in processes:
            proc.start()
        
        for proc in processes:
            proc.join()
        
        duration_seconds = (time.time() - start_timestamp)
        final_value = dm.get(KEY)

        print(f"{strategy_name}:")
        print(f"\tcounter value:\t{final_value}")
        print(f"\ttime taken:\t{duration_seconds:.2f} seconds")
        print()

    hz_client.shutdown()

