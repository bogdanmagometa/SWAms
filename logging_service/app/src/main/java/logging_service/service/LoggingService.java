package logging_service.service;

import logging_service.domain.Message;
import logging_service.repository.LoggingHazelcastRepository;
import logging_service.repository.LoggingInMemoryRepository;
import logging_service.repository.LoggingRepository;

public class LoggingService {
    private LoggingRepository repository = new LoggingHazelcastRepository();

    public void addMessage(Message message) {
        repository.addMessage(message);
    }
    public Message[] getMessages() {
        Message[] messages = repository.getMessages();
        System.out.println();
        return messages;
    }
}
