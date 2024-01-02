package front;

import javax.swing.*;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;


public class MatrixOperateFrame extends JFrame {
	private static final long serialVersionUID = 1L;

	public MatrixOperateFrame(int rowsA, int colsA, int rowsB, int colsB) {
		JFrame frame = new JFrame("Matrix Operation App");
        frame.setSize(600, 400);
        
        JPanel matrixPanel = new JPanel(new GridLayout(1, 2));
        MatrixDisplay matrixA = new MatrixDisplay(rowsA, colsA);
        JTable matrixATable = matrixA.getTable();
        matrixPanel.add(new JScrollPane(matrixATable), BorderLayout.CENTER);
        MatrixDisplay matrixB = new MatrixDisplay(rowsB, colsB);
        JTable matrixBTable = matrixB.getTable();
        matrixPanel.add(new JScrollPane(matrixBTable), BorderLayout.CENTER);
        
        JPanel buttonPanel = new JPanel(new GridLayout(1, 4));
        JButton addButton = new JButton("加法");
        addButton.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
            	if (rowsA != rowsB || colsA != colsB) {
            		JOptionPane.showMessageDialog(frame, "两矩阵维数不一致，无法进行加法", "错误", JOptionPane.ERROR_MESSAGE);
                }else {
                	try {
                		int[][] A= new int[rowsA][colsA];
                		int[][] B= new int[rowsB][colsB];
                		for(int i = 0; i < rowsA; ++i) {
                			for(int j = 0; j < colsA; ++j) {
                				A[i][j] = Integer.parseInt((String)matrixA.getValueAt(i, j));
                			}
                		}
                		for(int i = 0; i < rowsB; ++i) {
                			for(int j = 0; j < colsB; ++j) {
                				B[i][j] = Integer.parseInt((String)matrixB.getValueAt(i, j));
                			}
                		}
                		Matrix matrixA_ = new Matrix(rowsA, colsA, A);
                		Matrix matrixB_ = new Matrix(rowsB, colsB, B);
                		int[][] result=Matrix.add(matrixA_, matrixB_);
                		AnswerDisplay.displayArray(result);
                	}catch (NumberFormatException e1) {
                		JOptionPane.showMessageDialog(frame, "输入不合法", "错误", JOptionPane.ERROR_MESSAGE);
                	}
                }
            }
        });

        JButton multiplyButton = new JButton("乘法");
        multiplyButton.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
            	if (colsA != rowsB) {
            		JOptionPane.showMessageDialog(frame, "矩阵A的列数与矩阵B的行数不一致，无法进行乘法", "错误", JOptionPane.ERROR_MESSAGE);
                }else {
                	try {
                		int[][] A= new int[rowsA][colsA];
                		int[][] B= new int[rowsB][colsB];
                		for(int i = 0; i < rowsA; ++i) {
                			for(int j = 0; j < colsA; ++j) {
                				A[i][j] = Integer.parseInt((String)matrixA.getValueAt(i, j));
                			}
                		}
                		for(int i = 0; i < rowsB; ++i) {
                			for(int j = 0; j < colsB; ++j) {
                				B[i][j] = Integer.parseInt((String)matrixB.getValueAt(i, j));
                			}
                		}
                		Matrix matrixA_ = new Matrix(rowsA, colsA, A);
                		Matrix matrixB_ = new Matrix(rowsB, colsB, B);
                		int[][] result=Matrix.multiply(matrixA_, matrixB_);
                		AnswerDisplay.displayArray(result);
                	}catch (NumberFormatException e2) {
                		JOptionPane.showMessageDialog(frame, "输入不合法", "错误", JOptionPane.ERROR_MESSAGE);
                	}
                }
            }
        });

        JButton transposeButton = new JButton("转置(A)");
        transposeButton.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
            	try {
            		int[][] A= new int[rowsA][colsA];
            		for(int i = 0; i < rowsA; ++i) {
            			for(int j = 0; j < colsA; ++j) {
            				A[i][j] = Integer.parseInt((String)matrixA.getValueAt(i, j));
            			}
            		}
            		Matrix matrixA_ = new Matrix(rowsA, colsA, A);
            		int[][] result=Matrix.transpose(matrixA_);
            		AnswerDisplay.displayArray(result);
            	}catch (NumberFormatException e3) {
            		JOptionPane.showMessageDialog(frame, "输入不合法", "错误", JOptionPane.ERROR_MESSAGE);
            	}
            }
        });

        JButton exitButton = new JButton("退出");
        exitButton.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                System.exit(0);
            }
        });

        buttonPanel.add(addButton);
        buttonPanel.add(multiplyButton);
        buttonPanel.add(transposeButton);
        buttonPanel.add(exitButton);

        frame.setLayout(new BorderLayout());
        frame.add(matrixPanel, BorderLayout.CENTER);
        frame.add(buttonPanel, BorderLayout.SOUTH);

        frame.setVisible(true);
	}
}
