import hazelcast

if __name__ == "__main__":
    hz = hazelcast.HazelcastClient()
    map = hz.get_map("my-distributed-map").blocking()

    for i in range(1000):
        map.put(i, f"value{i}")

    hz.shutdown()
