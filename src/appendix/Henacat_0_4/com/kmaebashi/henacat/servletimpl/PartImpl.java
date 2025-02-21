package com.kmaebashi.henacat.servletimpl;
import java.io.*;
import java.util.*;
import com.kmaebashi.henacat.servlet.http.*;

public class PartImpl implements Part {
    private String contentType;
    private Map<String, String> headerMap;
    private byte[] data;
    private String name;
    
    public String getContentType() {
	return contentType;
    }
    
    public String getHeader(String name) {
	return headerMap.get(name);
    }
    
    public Collection<String> getHeaderNames() {
	return headerMap.keySet();
    }
    
    public InputStream getInputStream() {
	return new ByteArrayInputStream(data);
    }
    
    public String getName() {
	return name;
    }
    
    public long getSize() {
	return data.length;
    }
    
    public void write(String fileName) throws IOException {
	try (FileOutputStream fos = new FileOutputStream(fileName)) {
	    fos.write(data);
	}
    }
    
    PartImpl(String contentType, Map<String, String> headerMap,
	     byte[] data, String name) {
	this.contentType = contentType;
	this.headerMap = headerMap;
	this.data = data;
	this.name = name;
    }
}
