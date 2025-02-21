using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Net.Sockets;
using System.IO;

namespace TcpClientSample
{
    class Program
    {
        static void Main(string[] args)
        {
            using (TcpClient client = new TcpClient("localhost", 8001))
            using (FileStream fos
                = new FileStream("client_recv.txt", FileMode.Create, FileAccess.Write))
            using (FileStream fis
                = new FileStream("client_send.txt", FileMode.Open, FileAccess.Read))
            {
                int ch;
                using (NetworkStream stream = client.GetStream())
                {
                    while ((ch = fis.ReadByte()) != -1)
                    {
                        stream.WriteByte((byte)ch);
                    }
                    stream.WriteByte((byte)0);
                    while ((ch = stream.ReadByte()) != -1)
                    {
                        fos.WriteByte((byte)ch);
                    }
                }
            }
        }
    }
}
