package com.kmaebashi.henacat.servletimpl;
import com.kmaebashi.henacat.servlet.http.*;

public class ServletInfo {
    WebApplication webApp;
    String urlPattern;
    String servletClassName;
    HttpServlet servlet;

    public ServletInfo(WebApplication webApp, String urlPattern,
                       String servletClassName) {
	this.webApp = webApp;
	this.urlPattern = urlPattern;
	this.servletClassName = servletClassName;
    }
}
