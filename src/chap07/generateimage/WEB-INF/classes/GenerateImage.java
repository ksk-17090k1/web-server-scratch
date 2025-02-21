import java.io.*;
import java.text.*;
import java.awt.*;
import java.awt.image.*;
import javax.servlet.http.*;
import javax.imageio.*;

public class GenerateImage extends HttpServlet {
    @Override
    protected void doGet(HttpServletRequest request, HttpServletResponse response)
        throws IOException {
         response.setContentType("image/png");

         HttpSession session = request.getSession(true);
         Integer counter = (Integer)session.getAttribute("Counter");
         if (counter == null) {
             counter = new Integer(1);
             session.setAttribute("Counter", counter);
         } else {
             counter++;
             session.setAttribute("Counter", counter);
         }
         String counterStr = new DecimalFormat("000000").format(counter);
         
         BufferedImage image = new BufferedImage(100, 25,
                                                 BufferedImage.TYPE_INT_RGB);
         Graphics g =  image.createGraphics();
         g.setColor(Color.BLACK);
         g.fillRect(0, 0, image.getWidth(), image.getHeight());
         
         g.setColor(Color.WHITE);
         Font font = new Font(Font.SANS_SERIF, Font.PLAIN, 20);
         g.setFont(font);
         FontMetrics fm = g.getFontMetrics();
         int strWidth = fm.stringWidth(counterStr);
         int strAscent = fm.getAscent();
         int x = (image.getWidth() - strWidth) / 2;
         int y = image.getHeight() - ((image.getHeight() - strAscent) / 2);
         g.drawString(counterStr, x, y);
         g.dispose();

         ImageIO.write(image, "png", response.getOutputStream());
    }
}
