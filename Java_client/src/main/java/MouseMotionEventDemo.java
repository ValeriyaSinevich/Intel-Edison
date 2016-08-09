/**
 * Created by vsinevic on 13.07.2016.
 */

import java.awt.Dimension;
import java.awt.event.MouseMotionListener;
import java.awt.event.MouseEvent;
import java.awt.GridLayout;
import java.awt.image.BufferedImage;
import java.io.File;
import java.io.IOException;
import java.net.URISyntaxException;
import java.util.LinkedList;
import java.util.List;

import javax.imageio.ImageIO;
import javax.swing.*;

public class MouseMotionEventDemo extends JPanel
        implements MouseMotionListener {
    final String HOST = "10.188.44.145";
    final int PORT = 8080;

    public final BufferedImage getImage() {
        MyHttpClient myHttpClient = new MyHttpClient();
        BufferedImage image = myHttpClient.request(HOST, PORT);
        System.out.println(image.getWidth());
        System.out.println(image.getHeight());
        return image;
    }

    public final BufferedImage getImageFromFile() {
        File file = new File("image02.png");
        try {
            BufferedImage image =
                    ImageIO.read(new File(getClass().getResource("image02.png").toURI()));
            return image;
        } catch (URISyntaxException e) {
            System.out.println(e.getMessage());
        } catch (IOException e) {
            System.out.println(e.getMessage());
        }
        return new BufferedImage(600,
                450, BufferedImage.TYPE_INT_RGB);
    }

    public final void sendLine(Line line) {
        MyHttpClient myHttpClient = new MyHttpClient();
        Boolean success = myHttpClient.sendLine(HOST, PORT, line.toJson());
    }

    BlankArea blankArea;
    JTextArea textArea;
    public static List<Position> positions;
    private Boolean mousePressed = false;
    static final String NEWLINE = System.getProperty("line.separator");

    public static void main(String[] args) {
        /* Use an appropriate Look and Feel */
        try {
            //UIManager.setLookAndFeel("com.sun.java.swing.plaf.windows.WindowsLookAndFeel");
            //UIManager.setLookAndFeel("com.sun.java.swing.plaf.gtk.GTKLookAndFeel");
            UIManager.setLookAndFeel("javax.swing.plaf.metal.MetalLookAndFeel");
        } catch (UnsupportedLookAndFeelException ex) {
            ex.printStackTrace();
        } catch (IllegalAccessException ex) {
            ex.printStackTrace();
        } catch (InstantiationException ex) {

            ex.printStackTrace();
        } catch (ClassNotFoundException ex) {
            ex.printStackTrace();
        }
        /* Turn off metal's use of bold fonts */
        UIManager.put("swing.boldMetal", Boolean.FALSE);

        //Schedule a job for the event dispatch thread:
        //creating and showing this application's GUI.
        javax.swing.SwingUtilities.invokeLater(new Runnable() {
            public void run() {
                createAndShowGUI();
            }
        });
    }

    /**
     * Create the GUI and show it.  For thread safety,
     * this method should be invoked from the
     * event-dispatching thread.
     */
    private static void createAndShowGUI() {
        //Create and set up the window.
        JFrame frame = new JFrame("MouseMotionEventDemo");
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);

        //Create and set up the content pane.
        JComponent newContentPane = new MouseMotionEventDemo();
        newContentPane.setOpaque(true); //content panes must be opaque
        frame.setContentPane(newContentPane);

        //Display the window.
        frame.pack();
        frame.setVisible(true);
    }

    public MouseMotionEventDemo() {
        super(new GridLayout(0,1));
//        BufferedImage image = getImageFromFile();
        BufferedImage image = getImage();
//        JLabel area = new JLabel("Background", icon, JLabel.CENTER);
        blankArea = new BlankArea(image);
        int Height = image.getHeight();
        int Width = image.getWidth();
        //blankArea. setSize(Height, Width);
        add(blankArea);
//        add(area);

        textArea = new JTextArea();
        textArea.setEditable(false);
        positions = new LinkedList<Position>();
        JScrollPane scrollPane = new JScrollPane(textArea,
                JScrollPane.VERTICAL_SCROLLBAR_ALWAYS,
                JScrollPane.HORIZONTAL_SCROLLBAR_AS_NEEDED);
        scrollPane.setPreferredSize(new Dimension(Width, Height));

        //add(scrollPane);

        //Register for mouse events on blankArea and panel.
        blankArea.addMouseMotionListener(this);
        addMouseMotionListener(this);

        //setPreferredSize(new Dimension(450, 450));
        setBorder(BorderFactory.createEmptyBorder(20,20,20,20));
    }

    void eventOutput(String eventDescription, MouseEvent e) {
        textArea.append(eventDescription
                + " (" + e.getX() + "," + e.getY() + ")"
                + " detected on "
                + e.getComponent().getClass().getName()
                + NEWLINE);
        if (eventDescription.equals("Mouse dragged")) {
            mousePressed = true;
            Position pos = new Position(e.getX(), e.getY());
            positions.add(pos);
            blankArea.setPositions(positions);
            blankArea.repaint();
            //textArea.setCaretPosition(textArea.getDocument().getLength());
        } else {
            if (mousePressed) {
                Line line = new Line(positions);
                blankArea.setPositions(positions);
                blankArea.repaint();
                System.out.println("line created\n");
//                System.out.println(line.getByIndex(line.length() - 1));
                sendLine(line);
                mousePressed = false;
            }
        }
    }

    public void mouseMoved(MouseEvent e) {
        eventOutput("Mouse moved", e);
    }

    public void mouseDragged(MouseEvent e) {
        eventOutput("Mouse dragged", e);
    }

    protected ImageIcon createImageIcon(String path,
                                        String description) {
        java.net.URL imgURL = getClass().getResource(path);
        if (imgURL != null) {
            return new ImageIcon(imgURL, description);
        } else {
            System.err.println("Couldn't find file: " + path);
            return null;
        }
    }


}