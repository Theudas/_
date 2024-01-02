package front;

import javax.swing.*;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;

public class InputRowAndColFrame {
	private JFrame frame;
    private JTextField rowsFieldA, colsFieldA;
    private JTextField rowsFieldB, colsFieldB;
    public InputRowAndColFrame() {
        frame = new JFrame("输入行数和列数");
        frame.setSize(300, 200);
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        frame.setLayout(new BorderLayout());

        JPanel panel = new JPanel();
        panel.setLayout(new GridLayout(5, 3));

        JLabel rowsLabelA = new JLabel("矩阵A行数:");
        JLabel colsLabelA = new JLabel("矩阵A列数:");
        JLabel rowsLabelB = new JLabel("矩阵B行数:");
        JLabel colsLabelB = new JLabel("矩阵B列数:");
        rowsLabelA.setHorizontalAlignment(SwingConstants.CENTER);
        rowsLabelA.setVerticalAlignment(SwingConstants.CENTER);
        colsLabelA.setHorizontalAlignment(SwingConstants.CENTER);
        colsLabelA.setVerticalAlignment(SwingConstants.CENTER);
        rowsLabelB.setHorizontalAlignment(SwingConstants.CENTER);
        rowsLabelB.setVerticalAlignment(SwingConstants.CENTER);
        colsLabelB.setHorizontalAlignment(SwingConstants.CENTER);
        colsLabelB.setVerticalAlignment(SwingConstants.CENTER);

        rowsFieldA = new JTextField(5);
        colsFieldA = new JTextField(5);
        rowsFieldB = new JTextField(5);
        colsFieldB = new JTextField(5);
        
        JButton submitButton = new JButton("提交");
        submitButton.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                onSubmission();
            }
        });
        JButton exitButton = new JButton("退出");
        exitButton.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
            	System.exit(0);
            }
        });

        panel.add(rowsLabelA);
        panel.add(rowsFieldA);
        panel.add(colsLabelA);
        panel.add(colsFieldA);
        panel.add(rowsLabelB);
        panel.add(rowsFieldB);
        panel.add(colsLabelB);
        panel.add(colsFieldB);
        panel.add(submitButton);
        panel.add(exitButton);
        frame.add(panel, BorderLayout.CENTER);
        frame.setVisible(true);
    }
    private boolean isInputValid(int x, int lower, int upper) {
    	return x >= lower && x <= upper;
    }
    private void onSubmission() {
        try {
            int rowsA = Integer.parseInt(rowsFieldA.getText());
            int colsA = Integer.parseInt(colsFieldA.getText());
            int rowsB = Integer.parseInt(rowsFieldB.getText());
            int colsB = Integer.parseInt(colsFieldB.getText());
            
            System.out.println("用户输入: " + rowsA + " " + colsA + " " + rowsB + " " + colsB);

            if(isInputValid(rowsA, 1, 10) && isInputValid(colsA, 1, 10) && isInputValid(rowsB, 1, 10) && isInputValid(rowsB, 1, 10)) {
            	MatrixOperateFrame mof = new MatrixOperateFrame(rowsA, colsA, rowsB, colsB);
            	mof.setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE); // 关闭新窗口时只关闭当前窗口
            	mof.setVisible(true);
            }
            else {
            	JOptionPane.showMessageDialog(frame, "请输入1~10的数字", "错误", JOptionPane.ERROR_MESSAGE);
            }
        } catch (NumberFormatException ex) {
            JOptionPane.showMessageDialog(frame, "请输入有效的数字", "错误", JOptionPane.ERROR_MESSAGE);
        }
    }

    public static void main(String[] args) {
        SwingUtilities.invokeLater(new Runnable() {
            @Override
            public void run() {
                new InputRowAndColFrame();
            }
        });
    }
}
