/**
 * Created by vsinevic on 13.07.2016.
 */
import javax.swing.*;
import java.awt.Dimension;
import java.awt.Color;
import java.awt.Graphics;

public class BlankArea extends JLabel {
    Dimension minSize;

    public BlankArea(Icon image) {
        int Height = image.getIconHeight();
        int Width = image.getIconWidth();
        this.setHorizontalAlignment(JLabel.CENTER);
        this.setVerticalAlignment(JLabel.CENTER);
        minSize = new Dimension(Width, Height);
        setIcon(image);
        setMinimumSize(minSize);
        setPreferredSize(minSize);
        setMaximumSize(minSize);
        setOpaque(true);
        setBorder(BorderFactory.createLineBorder(Color.black));
    }

    public Dimension getMinimumSize() {
        return minSize;
    }

    public Dimension getPreferredSize() {
        return minSize;
    }
}