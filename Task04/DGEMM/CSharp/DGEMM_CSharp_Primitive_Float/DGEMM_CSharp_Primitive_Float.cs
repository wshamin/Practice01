using System;
using System.IO;
using System.Linq;
using System.Threading.Tasks;

public class DGEMM_CSharp_Primitive_Float
{
    public static void Main(string[] args)
    {
        string inputMatrixAFile = args[0];
        string inputMatrixBFile = args[1];
        string outputMatrixFile = args[2];
        int numThreads = int.Parse(args[3]);

        float[][] matrixA = LoadMatrix(inputMatrixAFile);
        float[][] matrixB = LoadMatrix(inputMatrixBFile);

        float[][] result = DGEMM(matrixA, matrixB, numThreads);

        SaveMatrix(result, outputMatrixFile);
    }

    private static float[][] LoadMatrix(string filename)
    {
        var culture = System.Globalization.CultureInfo.InvariantCulture;

        return File.ReadAllLines(filename)
           .Select(line => line.Split(',')
               .Select(x => float.Parse(x, culture))
                .ToArray())
            .ToArray();
    }


    private static float[][] DGEMM(float[][] A, float[][] B, int numThreads)
    {
        int n = A.Length;
        int m = B[0].Length;
        int p = A[0].Length;

        float[][] result = new float[n][];
        for (int i = 0; i < n; i++)
            result[i] = new float[m];

        var options = new ParallelOptions() { MaxDegreeOfParallelism = numThreads };

        Parallel.For(0, n, options, i =>
        {
            for (int j = 0; j < m; j++)
            {
                float sum = 0;
                for (int k = 0; k < p; k++)
                {
                    sum += A[i][k] * B[k][j];
                }
                result[i][j] = sum;
            }
        });

        return result;
    }

    private static void SaveMatrix(float[][] matrix, string filename)
    {
        using StreamWriter sw = new StreamWriter(filename);
        foreach (var row in matrix)
        {
            sw.WriteLine(string.Join(" ", row.Select(x => x.ToString("0.00"))));
        }
    }
}
