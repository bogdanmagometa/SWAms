# SWAms: Lab 2 (Hazelcast)

## Prerequisites
- install hazelcast
- set up python env:
```bash
$ pip3 install -r requirements.txt
```

## Project structure
- `create_map.py` - create map and fill it with 1000 entries
- `locking_strategies.py` - run 3 locking strategies and display results
- `bqueue.py` - create

## Usage

Start the hazelcast nodes, each with the following command:
```
$ hz start -c hazelcast.yaml
```

Run the corresponding scripts.
