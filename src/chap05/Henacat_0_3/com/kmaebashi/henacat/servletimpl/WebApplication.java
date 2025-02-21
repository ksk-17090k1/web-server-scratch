package com.kmaebashi.henacat.servletimpl;
import java.io.*;
import java.net.*;
import java.nio.file.*;
import java.util.*;

public class WebApplication {
    private static String WEBAPPS_DIR = "C:\\Henacat_0_3\\webapps";
    private static Map<String, WebApplication> webAppCollection
    	= new HashMap<String, WebApplication>();
    String directory;
    ClassLoader classLoader;
    private Map<String, ServletInfo> servletCollection
    	= new HashMap<String, ServletInfo>();
    private SessionManager sessionManager;
    
    private WebApplication(String dir) throws MalformedURLException {
	this.directory = dir;
	FileSystem fs = FileSystems.getDefault();
	
	Path pathObj = fs.getPath(WEBAPPS_DIR + File.separator + dir);
	this.classLoader 
	    = URLClassLoader.newInstance(new URL[]{pathObj.toUri().toURL()});
    }
    
    public static WebApplication createInstance(String dir)
	    throws MalformedURLException {
	WebApplication newApp = new WebApplication(dir);
	webAppCollection.put(dir, newApp);

	return newApp;
    }

    public void addServlet(String urlPattern, String servletClassName) {
	this.servletCollection.put(urlPattern,
				   new ServletInfo(this, urlPattern,
					           servletClassName));
    }
    
    public ServletInfo searchServlet(String path) {
	return servletCollection.get(path);
    }
    
    public static WebApplication searchWebApplication(String dir) {
	return webAppCollection.get(dir);
    }
    
    SessionManager getSessionManager() {
	if (this.sessionManager == null) {
	    this.sessionManager = new SessionManager();
	}
	return this.sessionManager;
    }
}
