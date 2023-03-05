package logging_service;

import java.io.IOException;

import logging_service.controller.WebServer;

public class Main {

    public static void main(String[] args) throws IOException {
        WebServer webServer = new WebServer();
        webServer.startServer();
    }
}
