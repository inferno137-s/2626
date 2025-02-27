using System;
using System.Windows.Forms;

namespace CramerMethodApp
{
    public partial class MainForm : Form
    {
        public MainForm()
        {
            InitializeComponent();
        }

        private void btnSolve_Click(object sender, EventArgs e)
        {
            try
            {
                // Получаем коэффициенты из текстовых полей
                double a11 = double.Parse(txtA11.Text);
                double a12 = double.Parse(txtA12.Text);
                double a13 = double.Parse(txtA13.Text);
                double b1 = double.Parse(txtB1.Text);

                double a21 = double.Parse(txtA21.Text);
                double a22 = double.Parse(txtA22.Text);
                double a23 = double.Parse(txtA23.Text);
                double b2 = double.Parse(txtB2.Text);

                double a31 = double.Parse(txtA31.Text);
                double a32 = double.Parse(txtA32.Text);
                double a33 = double.Parse(txtA33.Text);
                double b3 = double.Parse(txtB3.Text);

                // Основная матрица
                double[,] A = {
                    { a11, a12, a13 },
                    { a21, a22, a23 },
                    { a31, a32, a33 }
                };

                // Вектор свободных членов
                double[] B = { b1, b2, b3 };

                // Вычисляем определитель основной матрицы
                double detA = Determinant(A);

                if (detA == 0)
                {
                    txtResult.Text = "Система не имеет единственного решения (определитель равен нулю).";
                    return;
                }

                // Матрицы для вычисления определителей по методу Крамера
                double[,] A1 = ReplaceColumn(A, B, 0);
                double[,] A2 = ReplaceColumn(A, B, 1);
                double[,] A3 = ReplaceColumn(A, B, 2);

                // Вычисляем определители
                double detA1 = Determinant(A1);
                double detA2 = Determinant(A2);
                double detA3 = Determinant(A3);

                // Находим решения
                double x1 = detA1 / detA;
                double x2 = detA2 / detA;
                double x3 = detA3 / detA;

                // Выводим результат
                txtResult.Text = $"x1 = {x1:F2}\r\nx2 = {x2:F2}\r\nx3 = {x3:F2}";
            }
            catch (Exception ex)
            {
                txtResult.Text = "Ошибка: " + ex.Message;
            }
        }

        // Метод для вычисления определителя матрицы 3x3
        private double Determinant(double[,] matrix)
        {
            return matrix[0, 0] * (matrix[1, 1] * matrix[2, 2] - matrix[1, 2] * matrix[2, 1])
                 - matrix[0, 1] * (matrix[1, 0] * matrix[2, 2] - matrix[1, 2] * matrix[2, 0])
                 + matrix[0, 2] * (matrix[1, 0] * matrix[2, 1] - matrix[1, 1] * matrix[2, 0]);
        }

        // Метод для замены столбца в матрице
        private double[,] ReplaceColumn(double[,] matrix, double[] column, int colIndex)
        {
            double[,] result = (double[,])matrix.Clone();
            for (int i = 0; i < 3; i++)
            {
                result[i, colIndex] = column[i];
            }
            return result;
        }
    }
}
