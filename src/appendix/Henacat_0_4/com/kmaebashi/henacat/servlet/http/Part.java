package com.kmaebashi.henacat.servlet.http;
import java.io.*;
import java.util.*;

public interface Part {
    String getContentType();
    String getHeader(String name);
    Collection<String> getHeaderNames();
    InputStream getInputStream();
    String getName();
    long getSize();
    void write(String fileName) throws IOException;
}