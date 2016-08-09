/**
 * Created by vsinevic on 13.07.2016.
 */
import javax.swing.*;
import java.awt.*;
import java.awt.image.BufferedImage;
import java.util.LinkedList;
import java.util.List;

public class BlankArea extends JLabel {
    Dimension minSize;
    private BufferedImage background;
    public static List<Position> positions = new LinkedList<Position>();

    public BlankArea(BufferedImage image) {
        int Height = image.getHeight();
        int Width = image.getWidth();
        this.setHorizontalAlignment(JLabel.CENTER);
        this.setVerticalAlignment(JLabel.CENTER);
        minSize = new Dimension(Width, Height);

        setMinimumSize(minSize);
        setPreferredSize(minSize);
        setMaximumSize(minSize);
        setOpaque(true);
        setBorder(BorderFactory.createLineBorder(Color.black));
        background = image;
    }

    public void paintComponent(Graphics g){
        super.paintComponent(g);
//        System.out.println("hey");
        if (background != null) {
            int x = (getWidth() - background.getWidth()) / 2;
            int y = (getHeight() - background.getHeight()) / 2;
            g.drawImage(background, x, y, this);
        }
        g.setColor(Color.RED);
        for (Position pos : positions) {
            g.fillOval(pos.getX(), pos.getY(), 6, 6);
        }
    }
     public void setPositions(List<Position> positions) {
         this.positions = positions;
     }

    public Dimension getMinimumSize() {
        return minSize;
    }

    public Dimension getPreferredSize() {
        return minSize;
    }
}