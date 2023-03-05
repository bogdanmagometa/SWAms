package logging_service.controller;

import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.net.InetSocketAddress;
import java.sql.Timestamp;
import java.text.SimpleDateFormat;
import java.util.Arrays;
import java.util.HashMap;
import java.util.Map;
import java.util.UUID;
import java.util.concurrent.Executors;
import java.util.concurrent.ThreadPoolExecutor;

import com.sun.net.httpserver.*;
import org.json.*;

import logging_service.domain.Message;
import logging_service.service.LoggingService;

public class WebServer {
    final private int PORT = 8001;
    final private int BACKLOG = 10;
    final private int N_THREADS = 10;
    final private SimpleDateFormat TIMESTAMP_FORMAT = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss");

    private LoggingService loggingService = new LoggingService();

    public void startServer() throws IOException {
        HttpServer server = HttpServer.create(new InetSocketAddress("localhost", PORT), BACKLOG);

        ThreadPoolExecutor threadPoolExecutor = (ThreadPoolExecutor) Executors.newFixedThreadPool(N_THREADS);

        server.createContext("/", new RootHttpHandler());
        server.setExecutor(threadPoolExecutor);
        server.start();
    }

    private String getCurrentTimestamp() {
        Timestamp timestamp = new Timestamp(System.currentTimeMillis());
        String timestampStr = TIMESTAMP_FORMAT.format(timestamp);
        return timestampStr;
    }

    private void logInfo(String text) {
        System.out.println(getCurrentTimestamp() + ": " + text);
    }

    private void logError(String text) {
        System.err.println(getCurrentTimestamp() + ": " + text);
    }

    //TODO: look into static nested classes
    private class RootHttpHandler implements HttpHandler {
        final private static int UUID_SIZE_BYTES = 16;

        @Override
        public void handle(HttpExchange exchange) {
            try {
                if (exchange.getRequestMethod().equals("GET")) {
                    handleGet(exchange);
                } else if (exchange.getRequestMethod().equals("POST")) {
                    handlePost(exchange);
                } else {
                    exchange.sendResponseHeaders(405, -1);
                }
            } catch (IOException ex) {
                ex.printStackTrace();
            }
        }
        
        private void handleGet(HttpExchange exchange) throws IOException {
            Message[] messages = loggingService.getMessages();
            exchange.sendResponseHeaders(200, 0);
            OutputStream responseBody = exchange.getResponseBody();
            String[] messageTextArray = Arrays.stream(messages).map(message -> {return message.getMessageText();}).toArray(String[]::new);
            JSONArray messagesJson = new JSONArray(Arrays.asList(messageTextArray));
            responseBody.write(messagesJson.toString().getBytes()); //TODO: look into encodings
            responseBody.flush();
            responseBody.close();
        }

        private void handlePost(HttpExchange exchange) throws IOException {
            InputStream requestBodyStream = exchange.getRequestBody();
            
            // byte[] requestBytes = requestBodyStream.readAllBytes();
            
            byte[] uuidBytes = requestBodyStream.readNBytes(UUID_SIZE_BYTES);
            if (uuidBytes.length != UUID_SIZE_BYTES) {
                logError("Received bad POST request body for / uri.");
                exchange.sendResponseHeaders(400, -1);
                return;
            }
            UUID uuid = UUID.nameUUIDFromBytes(uuidBytes);

            byte[] messageBytes = requestBodyStream.readAllBytes();
            String message = new String(messageBytes);

            logInfo("Received message \"" + message + "\" with UUID " + uuid.toString());
            loggingService.addMessage(new Message(uuid, message));

            exchange.sendResponseHeaders(200, -1);
        }
    }

}
