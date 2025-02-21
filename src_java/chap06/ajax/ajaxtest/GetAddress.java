import java.io.*;
import com.kmaebashi.henacat.servlet.*;
import com.kmaebashi.henacat.servlet.http.*;

public class GetAddress extends HttpServlet {
    @Override
    public void doGet(HttpServletRequest request, HttpServletResponse response)
        throws IOException, ServletException {
        response.setContentType("text/plain;charset=UTF-8");
        PrintWriter out = response.getWriter();

        String postalCode = request.getParameter("postalCode");
        String ret;
        if (postalCode.equals("162-0846")) {
            ret = "東京都新宿区市谷左内町";
        } else if (postalCode.equals("100-0014")) {
            ret = "東京都千代田区永田町";
        } else {
            ret = "不明";
        }
        out.print(ret);
    }
}