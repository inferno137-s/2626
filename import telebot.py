using System;
using System.Windows.Forms;

namespace CramerMethod3x3
{
    public partial class Form1 : Form
    {
        public Form1()
        {
            InitializeComponent();
        }

        private void buttonSolve_Click(object sender, EventArgs e)
        {
            try
            {
                // Получаем коэффициенты из текстовых полей
                double a1 = double.Parse(textBoxA1.Text);
                double b1 = double.Parse(textBoxB1.Text);
                double c1 = double.Parse(textBoxC1.Text);
                double d1 = double.Parse(textBoxD1.Text);

                double a2 = double.Parse(textBoxA2.Text);
                double b2 = double.Parse(textBoxB2.Text);
                double c2 = double.Parse(textBoxC2.Text);
                double d2 = double.Parse(textBoxD2.Text);

                double a3 = double.Parse(textBoxA3.Text);
                double b3 = double.Parse(textBoxB3.Text);
                double c3 = double.Parse(textBoxC3.Text);
                double d3 = double.Parse(textBoxD3.Text);

                // Вычисляем главный определитель (Delta)
                double delta = a1 * (b2 * c3 - b3 * c2)
                            - b1 * (a2 * c3 - a3 * c2)
                            + c1 * (a2 * b3 - a3 * b2);

                // Вычисляем определитель для x (DeltaX)
                double deltaX = d1 * (b2 * c3 - b3 * c2)
                               - b1 * (d2 * c3 - d3 * c2)
                               + c1 * (d2 * b3 - d3 * b2);

                // Вычисляем определитель для y (DeltaY)
                double deltaY = a1 * (d2 * c3 - d3 * c2)
                               - d1 * (a2 * c3 - a3 * c2)
                               + c1 * (a2 * d3 - a3 * d2);

                // Вычисляем определитель для z (DeltaZ)
                double deltaZ = a1 * (b2 * d3 - b3 * d2)
                               - b1 * (a2 * d3 - a3 * d2)
                               + d1 * (a2 * b3 - a3 * b2);

                // Проверяем, что система имеет решение
                if (delta == 0)
                {
                    if (deltaX == 0 && deltaY == 0 && deltaZ == 0)
                    {
                        textBoxResult.Text = "Система имеет бесконечное количество решений";
                    }
                    else
                    {
                        textBoxResult.Text = "Система не имеет решений";
                    }
                }
                else
                {
                    // Находим решение системы
                    double x = deltaX / delta;
                    double y = deltaY / delta;
                    double z = deltaZ / delta;

                    // Выводим результат
                    textBoxResult.Text = $"x = {x}, y = {y}, z = {z}";
                }
            }
            catch (Exception ex)
            {
                MessageBox.Show("Ошибка: " + ex.Message);
            }
        }
    }
}
