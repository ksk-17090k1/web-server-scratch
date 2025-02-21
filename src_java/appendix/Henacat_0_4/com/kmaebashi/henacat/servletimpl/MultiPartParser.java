package com.kmaebashi.henacat.servletimpl;
import java.io.*;
import java.util.*;
import com.kmaebashi.henacat.servlet.http.*;
import com.kmaebashi.henacat.util.*;

public class MultiPartParser {
    static HttpServletRequestImpl parse(Map<String, String> requestHeader,
	    InputStream input,
	    String contentTypeStr, int contentLength,
	    HttpServletResponseImpl resp,
	    WebApplication webApp) throws IOException {
	ContentType contentType = Util.parseContentType(contentTypeStr);
	String boundary = "--" + contentType.getAttribute("BOUNDARY");
	ArrayList<Part> partList = new ArrayList<Part>();
	int length = contentLength; 
	length = readToBoundary(input, boundary, length, null);
	HashMap<String, byte[][]> parameterMap = new HashMap<String, byte[][]>();
	for (;;) {
            Map<String, String> headerMap = new HashMap<String, String>();
            String line;
            while ((line = Util.readLine(input)) != null) {
        	length -= line.length() + 2; // 2はCR+LF分
        	if (line.equals("")) {
        	    break;
        	}
        	Util.parseHeader(headerMap, line);
            }
            ContentType cd
            	= Util.parseContentType(headerMap.get("CONTENT-DISPOSITION"));
            String quotedName = cd.getAttribute("NAME");
            String name = quotedName.substring(1, quotedName.length() - 1);
            String ct = headerMap.get("CONTENT-TYPE");
            byte[][] dataOut = new byte[1][];
            length = readToBoundary(input, "\r\n" + boundary, length, dataOut);
            PartImpl part = new PartImpl(ct, headerMap, dataOut[0], name);
            partList.add(part);
            if (ct == null) {
        	byte[][] array = parameterMap.get(name);
        	if (array == null) {
        	    parameterMap.put(name, new byte[][] {dataOut[0]});
        	} else {
        	    byte[][] newArray = new byte[array.length + 1][];
        	    System.arraycopy(array, 0, newArray, 0, array.length);
        	    newArray[array.length] = dataOut[0];
        	    parameterMap.put(name, newArray);
        	}
            }
            if (length == 0) {
        	break;
            }
	}
	HttpServletRequestImpl req
		= new HttpServletRequestImpl(requestHeader, parameterMap,
			partList, resp, webApp);
	
	return req;
    }
    
    // inputから、boundaryの終了まで読み取り、boundaryの手前までの
    // バイト列をdataOut[0]に返す(dataOutがnullであれば返さない)。
    // Content-Lengthの残りを戻り値として返す。
    private static int readToBoundary(InputStream input,
	    String boundary, int length,
	    byte[][] dataOut) throws IOException {
	ByteArrayOutputStream out = new ByteArrayOutputStream();
	int ch;
	int bPos = 0;
	boolean found = false;
	while ((ch = input.read()) != -1 && length > 0) {
	    length--;
	    if (ch == boundary.charAt(bPos)) {
		bPos++;
		if (bPos == boundary.length()) {
		    found = true;
		    ch = input.read();
		    if (ch == '\r') {
			input.read(); // '\n'
			length -= 2;
		    } else if (ch == '-') {
			input.read(); // '-'
			input.read(); // \r
			input.read(); // \n
			length -= 4;
		    }
		    break;
		}
	    } else if (bPos > 0) {
		out.write(boundary.substring(0, bPos).getBytes("US-ASCII"));
		if (ch == boundary.charAt(0)) {
		    bPos = 1;
		} else {
		    bPos = 0;
		    out.write((byte)ch);
		}
	    } else {
		out.write((byte)ch);
	    }
	}
	if (found && dataOut != null) {
	    dataOut[0] = out.toByteArray();
	}
	return length;
    }
}
