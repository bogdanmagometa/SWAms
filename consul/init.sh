#!/bin/bash
while ! curl -f -s http://$CONSUL_HTTP_ADDR/v1/status/leader | grep "[0-9]:[0-9]"; do
  sleep 5
done

# Config
consul kv put logging_uri 'http://logging:8081/'
consul kv put messages_uri 'http://messages:8082/'
consul kv put queue_name 'messages_queue'
consul kv put hazelcast_node 'logging'
