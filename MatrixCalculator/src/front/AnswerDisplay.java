package front;

import javax.swing.*;

public class AnswerDisplay {
    public static void displayArray(int[][] array) {
        JFrame frame = new JFrame("运算结果");
        JTable table = new JTable(array.length, array[0].length);

        for (int i = 0; i < array.length; i++) {
            for (int j = 0; j < array[i].length; j++) {
                table.setValueAt(array[i][j], i, j);
            }
        }

        frame.add(new JScrollPane(table));
        frame.setSize(400, 300);
        frame.setVisible(true);
    }

    public static void main(String[] args) {
        int[][] myArray = { { 1, 2, 3 }, { 4, 5, 6 }, { 7, 8, 9 } };
        displayArray(myArray);
    }
}