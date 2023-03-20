import hazelcast
import multiprocessing as mp
import time

QUEUE_NAME = "queue"
PRODUCER_PUTS = 20
PRODUCER_WTIME_SECONDS = 0.1
CONSUMER_WTIME_SECONDS = 0.05
NUM_CONSUMERS = 2
POISON_PILL = -1

def producer_work():
    hz_client = hazelcast.HazelcastClient()
    bq = hz_client.get_queue(QUEUE_NAME).blocking()
    bq.clear()
    for i in range(PRODUCER_PUTS):
        print(f"Putting {i}")
        bq.put(i)
        time.sleep(PRODUCER_WTIME_SECONDS)
    bq.put(POISON_PILL)
    hz_client.shutdown()

def consumer_work():
    hz_client = hazelcast.HazelcastClient()
    bq = hz_client.get_queue(QUEUE_NAME).blocking()
    while True:
        val = bq.take()
        time.sleep(CONSUMER_WTIME_SECONDS)
        if val == POISON_PILL:
            bq.put(val)
            break
        print(f"\t\tReading {val}")
    hz_client.shutdown()

if __name__ == "__main__":
    ctx = mp.get_context("fork")
    
    procs = []

    procs.append(ctx.Process(target=producer_work))

    for _ in range(NUM_CONSUMERS):
        procs.append(ctx.Process(target=consumer_work))
    

    for proc in procs:
        proc.start()
    
    for proc in procs:
        proc.join()
