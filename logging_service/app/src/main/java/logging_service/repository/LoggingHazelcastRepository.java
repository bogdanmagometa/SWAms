package logging_service.repository;

import java.util.Map;
import java.util.UUID;

import com.hazelcast.core.Hazelcast;
import com.hazelcast.core.HazelcastInstance;

import logging_service.domain.Message;

public class LoggingHazelcastRepository implements LoggingRepository {
    private HazelcastInstance hzInstance = Hazelcast.newHazelcastInstance();
    private Map<UUID, String> messageMap = hzInstance.getMap("logging_map");

    @Override
    public void addMessage(Message message) {
        UUID uuid = message.getUuid();
        String messageText = message.getMessageText();
        messageMap.put(uuid, messageText);
    }

    @Override
    public Message[] getMessages() {
        Message[] messages = messageMap.entrySet().stream()
                .map(entry -> {return new Message(entry.getKey(), entry.getValue());})
                .toArray(Message[]::new);
        return messages;
    }
}
