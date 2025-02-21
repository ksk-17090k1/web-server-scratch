import java.io.*;
import java.net.*;
import java.nio.file.*;

class ServerThread implements Runnable {
    private static final String DOCUMENT_ROOT = "C:\\Apache24\\htdocs";
    private static final String ERROR_DOCUMENT = "C:\\webserver\\error_document";
    private static final String SERVER_NAME = "localhost:8001";
    private Socket socket;

    @Override
    public void run() {
        OutputStream output = null;
        try {
            InputStream input = socket.getInputStream();

            String line;
            String path = null;
            String ext = null;
            String host = null;
            while ((line = Util.readLine(input)) != null) {
                if (line.equals(""))
                    break;
                if (line.startsWith("GET")) {
                    path = MyURLDecoder.decode(line.split(" ")[1], "UTF-8");
                    String[] tmp = path.split("\\.");
                    ext = tmp[tmp.length - 1];
                } else if (line.startsWith("Host:")) {
                    host = line.substring("Host: ".length());
                }
            }
            if (path == null)
                return;

            if (path.endsWith("/")) {
                path += "index.html";
                ext = "html";
            }
            output = new BufferedOutputStream(socket.getOutputStream());
            
            FileSystem fs = FileSystems.getDefault();
            Path pathObj = fs.getPath(DOCUMENT_ROOT + path);
            Path realPath;
            try {
                realPath = pathObj.toRealPath();
            } catch (NoSuchFileException ex) {
                SendResponse.sendNotFoundResponse(output, ERROR_DOCUMENT);
                return;
            }
            if (!realPath.startsWith(DOCUMENT_ROOT)) {
                SendResponse.sendNotFoundResponse(output, ERROR_DOCUMENT);
                return;
            } else if (Files.isDirectory(realPath)) {
                String location = "http://"
                    + ((host != null) ? host : SERVER_NAME)
                    + path + "/";
                SendResponse.sendMovePermanentlyResponse(output, location);
                return;
            }
            try (InputStream fis
                 = new BufferedInputStream(Files.newInputStream(realPath))) {
                SendResponse.sendOkResponse(output, fis, ext);
            } catch (FileNotFoundException ex) {
                SendResponse.sendNotFoundResponse(output, ERROR_DOCUMENT);
            }
        } catch (Exception ex) {
            ex.printStackTrace();
        } finally {
            try {
                if (output != null) {
                    output.close();
                }
                socket.close();
            } catch (Exception ex) {
                ex.printStackTrace();
            }
        }
    }

    ServerThread(Socket socket) {
        this.socket = socket;
    }
}
