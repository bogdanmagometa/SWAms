package logging_service.repository;

import java.util.HashMap;
import java.util.Map;
import java.util.UUID;

import logging_service.domain.Message;

public class LoggingInMemoryRepository implements LoggingRepository {
    private Map<UUID, String> messageMap = new HashMap<>();

    @Override
    public void addMessage(Message message) {
        UUID uuid = message.getUuid();
        String messageText = message.getMessageText();
        messageMap.put(uuid, messageText);
    }

    @Override
    public Message[] getMessages() {
        Message[] messages = messageMap.values().stream().map(messageText -> {return new Message(null, messageText);}).toArray(Message[]::new);
        return messages;
    }
}
