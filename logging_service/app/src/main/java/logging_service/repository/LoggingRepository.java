package logging_service.repository;

import logging_service.domain.Message;

public interface LoggingRepository {
    public void addMessage(Message message);
    public Message[] getMessages();
}
