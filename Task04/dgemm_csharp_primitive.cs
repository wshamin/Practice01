using System;
using System.Threading.Tasks;

namespace DGEMM
{
    class DGEMM_CSharp_Primitive
    {
        static void Main(string[] args)
        {
            // Загрузите матрицы из файла, переданного через аргументы командной строки

            double[,] A = LoadMatrix(args[0]);
            double[,] B = LoadMatrix(args[1]);
            int numThreads = int.Parse(args[2]);

            int N = A.GetLength(0);
            int M = B.GetLength(1);
            int K = A.GetLength(1);

            double[,] C = new double[N, M];

            Parallel.For(0, N, new ParallelOptions { MaxDegreeOfParallelism = numThreads }, i =>
            {
                for (int j = 0; j < M; j++)
                {
                    for (int k = 0; k < K; k++)
                    {
                        C[i, j] += A[i, k] * B[k, j];
                    }
                }
            });

            // Сохраните результат в файл
        }

        static double[,] LoadMatrix(string filename)
        {
            // Реализуйте функцию загрузки матрицы из файла
        }
    }
}
