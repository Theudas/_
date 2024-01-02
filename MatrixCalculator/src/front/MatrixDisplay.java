package front;

import javax.swing.*;
import javax.swing.event.TableModelEvent;
import javax.swing.event.TableModelListener;
import javax.swing.table.DefaultTableModel;
import java.awt.*;

public class MatrixDisplay {
    private int rows;
    private int columns;
    private Object[][] data;
    private DefaultTableModel tableModel;
    private JTable table;
    private JFrame frame;

    public MatrixDisplay(int rows, int columns) {
        this.rows = rows;
        this.columns = columns;
        this.data = new Object[rows][columns];

        for (int i = 0; i < rows; i++) {
            for (int j = 0; j < columns; j++) {
                data[i][j] = "null";
            }
        }

        Object[] columnNames = new Object[columns];
        for (int j = 0; j < columns; j++) {
            columnNames[j] = "第" + (j + 1) + "列";
        }

        this.tableModel = new DefaultTableModel(data, columnNames);

        this.tableModel.addTableModelListener(new TableModelListener() {
            @Override
            public void tableChanged(TableModelEvent e) {
                int row = e.getFirstRow();
                int column = e.getColumn();
                if (row != TableModelEvent.HEADER_ROW && column != TableModelEvent.ALL_COLUMNS) {
                    data[row][column] = tableModel.getValueAt(row, column);
                    System.out.println(""+row+" "+column+" "+data[row][column]);
                }
            }
        });

        this.table = new JTable(tableModel);

        this.frame = new JFrame("矩阵显示");
        this.frame.setSize(400, 300);

        JScrollPane scrollPane = new JScrollPane(table);

        this.frame.add(scrollPane);
    }

    public void displayMatrix() {
        SwingUtilities.invokeLater(() -> {
            frame.setVisible(true);
        });
    }

    public JTable getTable() {
        return table;
    }

    public Object getValueAt(int row, int column) {
        return tableModel.getValueAt(row, column);
    }
}