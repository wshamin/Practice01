using System;
using System.IO;
using System.Linq;
using System.Threading.Tasks;

public class DGEMM_CSharp_Primitive_Int
{
    public static void Main(string[] args)
    {
        string inputMatrixAFile = args[0];
        string inputMatrixBFile = args[1];
        string outputMatrixFile = args[2];
        int numThreads = int.Parse(args[3]);

        int[][] matrixA = LoadMatrix(inputMatrixAFile);
        int[][] matrixB = LoadMatrix(inputMatrixBFile);

        int[][] result = DGEMM(matrixA, matrixB, numThreads);

        SaveMatrix(result, outputMatrixFile);
    }

    private static int[][] LoadMatrix(string filename)
    {
        return File.ReadAllLines(filename)
            .Select(line => line.Split(',')
                .Select(int.Parse)
                .ToArray())
            .ToArray();
    }

    private static int[][] DGEMM(int[][] A, int[][] B, int numThreads)
    {
        int n = A.Length;
        int m = B[0].Length;
        int p = A[0].Length;

        int[][] result = new int[n][];
        for (int i = 0; i < n; i++)
            result[i] = new int[m];

        var options = new ParallelOptions() { MaxDegreeOfParallelism = numThreads };

        Parallel.For(0, n, options, i =>
        {
            for (int j = 0; j < m; j++)
            {
                int sum = 0;
                for (int k = 0; k < p; k++)
                {
                    sum += A[i][k] * B[k][j];
                }
                result[i][j] = sum;
            }
        });

        return result;
    }

    private static void SaveMatrix(int[][] matrix, string filename)
    {
        using StreamWriter sw = new StreamWriter(filename);
        foreach (var row in matrix)
        {
            sw.WriteLine(string.Join(" ", row));
        }
    }
}
