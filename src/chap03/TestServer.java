import java.io.*;
import java.net.*;

public class TestServer {
    public static void main(String[] argv) throws Exception {
        try (ServerSocket server = new ServerSocket(8001);
             FileOutputStream fos = new FileOutputStream("server_recv.txt")) {
            System.out.println("クライアントからの接続を待ちます。");
            Socket socket = server.accept();
            System.out.println("クライアント接続。");
  
            int ch;
            // クライアントから受け取った内容をserver_recv.txtに出力
            InputStream input = socket.getInputStream();
            while ((ch = input.read()) != -1) {
                fos.write(ch);
            }
            socket.close();
        } catch (Exception ex) {
            ex.printStackTrace();
        }
    }
}