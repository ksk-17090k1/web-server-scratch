using System;
using System.IO;
using System.Net;
using System.Net.Sockets;

namespace TcpServer
{
    class Program
    {
        static void Main(string[] args)
        {
            TcpListener listener = new TcpListener(IPAddress.Any, 8001);
            listener.Start();
            Console.WriteLine("クライアントからの接続を待ちます。");
            using (TcpClient client = listener.AcceptTcpClient())
            using (FileStream fos 
                = new FileStream("server_recv.txt", FileMode.Create, FileAccess.Write))
            using (FileStream fis
                = new FileStream("server_send.txt", FileMode.Open, FileAccess.Read))
            {
                Console.WriteLine("クライアント接続。");
                using (NetworkStream stream = client.GetStream())
                {
                    int ch;
                    while ((ch = stream.ReadByte()) != 0)
                    {
                        fos.WriteByte((byte)ch);
                    }
                    while ((ch = fis.ReadByte()) != -1)
                    {
                        stream.WriteByte((byte)ch);
                    }
                }
            }
            Console.WriteLine("通信を終了しました。");
        }
    }
}
