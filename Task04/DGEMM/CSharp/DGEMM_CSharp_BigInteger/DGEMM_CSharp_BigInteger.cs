using System.Numerics;


public class DGEMM_CSharp_BigInteger
{
    public static void Main(string[] args)
    {
        string inputMatrixAFile = args[0];
        string inputMatrixBFile = args[1];
        string outputMatrixFile = args[2];
        int numThreads = int.Parse(args[3]);

        BigInteger[][] matrixA = LoadMatrix(inputMatrixAFile);
        BigInteger[][] matrixB = LoadMatrix(inputMatrixBFile);

        BigInteger[][] result = DGEMM(matrixA, matrixB, numThreads);

        SaveMatrix(result, outputMatrixFile);
    }

    private static BigInteger[][] LoadMatrix(string filename)
    {
        return File.ReadAllLines(filename)
            .Select(line => line.Split(',')
                .Select(BigInteger.Parse)
                .ToArray())
            .ToArray();
    }

    private static BigInteger[][] DGEMM(BigInteger[][] A, BigInteger[][] B, int numThreads)
    {
        int n = A.Length;
        int m = B[0].Length;
        int p = A[0].Length;

        BigInteger[][] result = new BigInteger[n][];
        for (int i = 0; i < n; i++)
            result[i] = new BigInteger[m];

        var options = new ParallelOptions() { MaxDegreeOfParallelism = numThreads };

        Parallel.For(0, n, options, i =>
        {
            for (int j = 0; j < m; j++)
            {
                BigInteger sum = BigInteger.Zero;
                for (int k = 0; k < p; k++)
                {
                    sum += A[i][k] * B[k][j];
                }
                result[i][j] = sum;
            }
        });

        return result;
    }

    private static void SaveMatrix(BigInteger[][] matrix, string filename)
    {
        using StreamWriter sw = new StreamWriter(filename);
        foreach (var row in matrix)
        {
            sw.WriteLine(string.Join(" ", row));
        }
    }
}
