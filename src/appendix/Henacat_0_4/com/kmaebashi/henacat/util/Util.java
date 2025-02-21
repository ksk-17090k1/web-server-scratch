package com.kmaebashi.henacat.util;
import java.io.*;
import java.util.*;
import java.text.*;

public class Util {
    // InputStreamからのバイト列を、行単位で読み込むユーティリティメソッド
    public static String readLine(InputStream input) throws IOException {
	int ch;
	String ret = "";
	while ((ch = input.read()) != -1) {
	    if (ch == '\r') {
		// 何もしない
	    } else if (ch == '\n') {
		break;
	    } else {
		ret += (char)ch;
	    }
	}
	if (ch == -1) {
	    return null;
	} else {
	    return ret;
	}
    }

    // 1行の文字列を、バイト列としてOutputStreamに書き込む
    // ユーティリティメソッド
    public static void writeLine(OutputStream output, String str)
	throws  IOException {
	for (char ch : str.toCharArray()) {
	    output.write((int)ch);
	}
	output.write((int)'\r');
	output.write((int)'\n');
    }

    // 現在時刻から、HTTP標準に合わせてフォーマットされた日付文字列を返す
    public static String getDateStringUtc() {
	Calendar cal = Calendar.getInstance(TimeZone.getTimeZone("UTC"));
	DateFormat df = new SimpleDateFormat("EEE, dd MMM yyyy HH:mm:ss",
					     Locale.US);
	df.setTimeZone(cal.getTimeZone());
	return df.format(cal.getTime()) + " GMT";
    }

    // 拡張子とContent-Typeの対応表
    private static final HashMap<String, String> contentTypeMap =
	new HashMap<String, String>() {{
	    put("html", "text/html");
	    put("htm", "text/html");
	    put("txt", "text/plain");
	    put("css", "text/css");
	    put("png", "image/png");
	    put("jpg", "image/jpeg");
	    put("jpeg", "image/jpeg");
	    put("gif", "image/gif");
	}
    };

    // 拡張子を受け取りContent-Typeを返す
    public static String getContentType(String ext) {
	String ret = contentTypeMap.get(ext.toLowerCase());
	if (ret == null) {
	    return "application/octet-stream";
	} else {
	    return ret;
	}
    }
    
    // リクエスト(等の)ヘッダを名前と値に分離し、headerMapに追加する。
    public static void parseHeader(Map<String, String> headerMap,
	 String line) {
        int colonPos = line.indexOf(':');
        if (colonPos == -1)
            return;

        String headerName = line.substring(0, colonPos).toUpperCase();
        String headerValue = line.substring(colonPos + 1).trim();
        headerMap.put(headerName, headerValue);
    }
    
    // Content-Typeの文字列をパースする
    public static ContentType parseContentType(String str) {
	String[] temp = str.split(" *; *");
	String[] typeSubType = temp[0].split("/");
	String type = typeSubType[0];
	String subType = null;
	if (typeSubType.length > 1) {
	    subType = typeSubType[1];
	}
	Map<String, String> attributes = new HashMap<String, String>(); 
	
	for (int i = 1; i < temp.length; i++) {
	    String[] keyValue = temp[i].split("=");
	    attributes.put(keyValue[0].toUpperCase(), keyValue[1]);
	}
	
	return new ContentType(type, subType, attributes);
    }
}
