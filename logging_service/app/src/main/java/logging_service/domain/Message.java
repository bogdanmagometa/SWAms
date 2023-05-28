package logging_service.domain;

import java.util.UUID;

import javax.annotation.Nonnull;

public class Message {
    private UUID uuid;
    private String messageText;
    public Message(UUID uuid, @Nonnull String messageText) {
        this.uuid = uuid;
        this.messageText = messageText;
    }

    public String getMessageText() {
        return messageText;
    }

    public UUID getUuid() {
        return uuid;
    }

    @Override
    public String toString() {
        String format = "Message(messageText=\"%s\", uuid=\"%s\")";
        return String.format(format, messageText, uuid.toString());
    }
}
