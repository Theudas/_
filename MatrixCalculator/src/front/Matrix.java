package front;

import java.io.BufferedWriter;
import java.io.FileWriter;
import java.io.IOException;

public class Matrix {

    private int[][] data;
    
    public Matrix(int rows, int columns, int[][] data) {
        this.data = new int[rows][columns];
        for(int i=0;i<rows;++i) {
        	for(int j=0;j<columns;++j) {
        		this.data[i][j]=data[i][j];
        	}
        }
    }
    public int[][] getData() {
    	return this.data;
    }
    // 加法
    public static int[][] add(Matrix matrixA, Matrix matrixB) {
        if (matrixA.getData().length != matrixB.getData().length || matrixA.getData()[0].length != matrixB.getData()[0].length) {
            throw new IllegalArgumentException("Matrix dimensions don't match");
        }
        int rows = matrixA.getData().length;
        int columns = matrixA.getData()[0].length;
        int[][] result = new int[rows][columns];
        for (int i = 0; i < rows; i++) {
            for (int j = 0; j < columns; j++) {
                result[i][j] = matrixA.getData()[i][j] + matrixB.getData()[i][j];
            }
        }
        writeToFile(result, "add.txt");
        return result;
    }
    // 乘法
    public static int[][] multiply(Matrix matrixA, Matrix matrixB) {
        if (matrixA.getData()[0].length != matrixB.getData().length) {
            throw new IllegalArgumentException("Matrix dimensions don't match for multiplication");
        }
        int rowsA = matrixA.getData().length;
        int columnsA = matrixA.getData()[0].length;
        int columnsB = matrixB.getData()[0].length;
        int[][] result = new int[rowsA][columnsB];
        for (int i = 0; i < rowsA; i++) {
            for (int j = 0; j < columnsB; j++) {
                for (int k = 0; k < columnsA; k++) {
                    result[i][j] += matrixA.getData()[i][k] * matrixB.getData()[k][j];
                }
            }
        }
        writeToFile(result, "multiply.txt");
        return result;
    }
    // 转置
    public static int[][] transpose(Matrix matrix) {
        int rows = matrix.getData().length;
        int columns = matrix.getData()[0].length;
        int[][] result = new int[columns][rows];

        for (int i = 0; i < rows; i++) {
            for (int j = 0; j < columns; j++) {
                result[j][i] = matrix.getData()[i][j];
            }
        }
        writeToFile(result, "transpose.txt");
        return result;
    }
    
    private static void writeToFile(int[][] array, String fileName) {
        try (BufferedWriter writer = new BufferedWriter(new FileWriter(fileName))) {
            for (int i = 0; i < array.length; i++) {
                for (int j = 0; j < array[i].length; j++) {
                    writer.write(array[i][j] + " ");
                }
                writer.newLine();
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
