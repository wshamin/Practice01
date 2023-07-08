import java.io.BufferedWriter;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.List;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.TimeUnit;

public class DGEMM_Java_Primitive_Int {
    public static void main(String[] args) {
        String inputMatrixAFile = args[0];
        String inputMatrixBFile = args[1];
        String outputMatrixFile = args[2];
        int numThreads = Integer.parseInt(args[3]);

        int[][] matrixA = loadMatrix(inputMatrixAFile);
        if (matrixA == null) {
            System.err.println("Ошибка при загрузке матрицы A");
            return;
        }

        int[][] matrixB = loadMatrix(inputMatrixBFile);
        if (matrixB == null) {
            System.err.println("Ошибка при загрузке матрицы B");
            return;
        }

        int[][] result = dgemm(matrixA, matrixB, numThreads);

        saveMatrix(result, outputMatrixFile);
    }

    private static int[][] loadMatrix(String filename) {
        try {
            List<String> lines = Files.readAllLines(Paths.get(filename));
            int n = lines.size();
            int m = lines.get(0).split(",").length;
            int[][] matrix = new int[n][m];

            for (int i = 0; i < n; i++) {
                String[] values = lines.get(i).split(",");
                for (int j = 0; j < m; j++) {
                    matrix[i][j] = Integer.parseInt(values[j]);
                }
            }

            return matrix;
        } catch (IOException e) {
            e.printStackTrace();
            return null;
        }
    }

    private static int[][] dgemm(int[][] A, int[][] B, int numThreads) {
        int n = A.length;
        int m = B[0].length;
        int p = A[0].length;
        ExecutorService executorService = Executors.newFixedThreadPool(numThreads);

        int[][] result = new int[n][m];
        for (int i = 0; i < n; i++) {
            final int threadRow = i;
            executorService.submit(() -> {
                for (int j = 0; j < m; j++) {
                    int sum = 0;
                    for (int k = 0; k < p; k++) {
                        sum += A[threadRow][k] * B[k][j];
                    }
                    result[threadRow][j] = sum;
                }
            });
        }

        executorService.shutdown();
        try {
            if (!executorService.awaitTermination(60, TimeUnit.MINUTES)) {
                executorService.shutdownNow();
            }
        } catch (InterruptedException ex) {
            executorService.shutdownNow();
            Thread.currentThread().interrupt();
        }

        return result;
    }

    private static void saveMatrix(int[][] matrix, String filename) {
        try (BufferedWriter bw = Files.newBufferedWriter(Paths.get(filename))) {
            int n = matrix.length;
            int m = matrix[0].length;

            for (int i = 0; i < n; i++) {
                for (int j = 0; j < m; j++) {
                    bw.write(matrix[i][j] + (j == m - 1 ? "" : " "));
                }
                bw.newLine();
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
