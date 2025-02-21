package com.kmaebashi.henacat.util;
import java.util.*;

public class ContentType {
    private String type;
    private String subType;
    private Map<String, String> attributes;
    
    public String getType() {
        return type;
    }

    public String getSubType() {
        return subType;
    }
    
    public String getAttribute(String key) {
        return attributes.get(key);
    }
    
    ContentType(String type, String subType,
	    Map<String, String> attributes) {
	this.type = type;
	this.subType = subType;
	this.attributes = attributes;
    }
}
