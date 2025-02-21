package com.kmaebashi.henacat.webserver;
import com.kmaebashi.henacat.servletimpl.WebApplication;

import java.net.*;

public class Main {
    public static void main(String[] argv) throws Exception {
	WebApplication app = WebApplication.createInstance("testbbs");
	app.addServlet("/ShowBBS", "ShowBBS");
	app.addServlet("/PostBBS", "PostBBS");
	try (ServerSocket server = new ServerSocket(8001)) {
	    for (;;) {
		Socket socket = server.accept();
		ServerThread serverThread = new ServerThread(socket);
		Thread thread = new Thread(serverThread);
		thread.start();
	    }
	}
    }
}
