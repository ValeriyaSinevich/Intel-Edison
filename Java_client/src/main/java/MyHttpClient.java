import com.sun.corba.se.impl.orbutil.ObjectWriter;

import javax.imageio.ImageIO;
import javax.swing.*;
import java.awt.image.BufferedImage;
import java.io.File;
import java.io.IOException;
import java.io.InputStream;
import java.io.PrintWriter;
import java.net.Socket;

/**
 * Created by vsinevic on 13.07.2016.
 */
public class MyHttpClient {
    public final ImageIcon request(String ip, int port) {
        try {
            System.out.println("connecting\n");
            Socket socket = new Socket(ip, port);
            System.out.println("sending request\n");
            PrintWriter printWriter = new PrintWriter(socket.getOutputStream());
            printWriter.println("GET");
            printWriter.println("");
            printWriter.flush();
            System.out.println("request sent\n");

            InputStream inputStream = socket.getInputStream();
            System.out.println("reading image\n");
            BufferedImage bufferedImage = ImageIO.read(inputStream);
            ImageIcon icon = new ImageIcon(bufferedImage);
            System.out.println("image ready\n");
            return icon;
        } catch(IOException e) {
            System.out.printf("can't connect\n");
            return new ImageIcon();
        }
    }

    public final Boolean sendLine(String ip, int port, String line) {
        try {
            System.out.println(line);
            System.out.println("connecting\n");
            Socket socket = new Socket(ip, port);
            System.out.println("sending msgt\n");
            PrintWriter printWriter = new PrintWriter(socket.getOutputStream());
            printWriter.println("POST");
            printWriter.println("");
            printWriter.flush();
            System.out.println("sending line\n");

            printWriter.println(line);
            printWriter.println("");
            printWriter.flush();
            System.out.println("Line sent\n");
            return true;
        } catch(IOException e) {
            System.out.printf("can't connect\n");
            return false;
        }
    }
}
