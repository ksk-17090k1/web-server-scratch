import java.io.*;
import java.net.*;

public class FileDownloader {
    private static final String TARGET_ADDRESS = "http://localhost/downloadtest/file.mp4";

    public static void main(String args[]) {
        HttpURLConnection connection = null;
        BufferedInputStream input = null;
        BufferedOutputStream output = null; 
        
        try {
            URL url = new URL(TARGET_ADDRESS);
            connection = (HttpURLConnection)url.openConnection();
            connection.setRequestMethod("GET");
            connection.connect();

            input = new BufferedInputStream(connection.getInputStream());
            output = new BufferedOutputStream(new FileOutputStream("file.mp4"));
            
            int ch;
            while ((ch = input.read()) != -1) {
                output.write(ch);
            }

        } catch (Exception ex) {
            ex.printStackTrace();
        } finally {
            try {
                if (input != null) {
                    input.close();
                }
                if (output != null) {
                    output.close();
                }
                if (connection != null) {
                    connection.disconnect();
                }
            } catch (Exception ex) {
                ex.printStackTrace();
            }
        }
    }
}
