using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace Задача_Задачи
{
    public partial class Form1 : Form
    {
        public Form1()
        {
            InitializeComponent();
        }

        private void button1_Click(object sender, EventArgs e)
        {
            try
            {
                // Объявляем переменные
                double a1 = double.Parse(textBox1.Text);
                double a2 = double.Parse(textBox2.Text);
                double a3 = double.Parse(textBox3.Text);

                double b1 = double.Parse(textBox4.Text);
                double b2 = double.Parse(textBox5.Text);
                double b3 = double.Parse(textBox6.Text);

                double c1 = double.Parse(textBox7.Text);
                double c2 = double.Parse(textBox8.Text);
                double c3 = double.Parse(textBox9.Text);

                double s1 = double.Parse(textBox10.Text);
                double s2 = double.Parse(textBox11.Text);
                double s3 = double.Parse(textBox12.Text);

                // Главный определитель
                double D = a1 * b2 * c3 + a3 * b1 * c2 + a2 * b3 * c1 - a2 * b1 * c3 - a1 * b3 * c2 - a3 * b2 * c1;

                // Проверка, имеет ли система решения
                if (D != 0)
                {
                    // Дополнительные определители
                    double D1 = s1 * b2 * c3 + s3 * b1 * c2 + s2 * b3 * c1 - s3 * b2 * c1 - s1 * b3 * c2 - s2 * b1 * c3;
                    double D2 = a1 * s2 * c3 + a3 * s1 * c2 + a2 * s3 * c1 - a3 * s2 * c1 - a1 * s3 * c2 - a2 * s1 * c3;
                    double D3 = a1 * b2 * s3 + a3 * b1 * s2 + a2 * b3 * s1 - a3 * b2 * s1 - a1 * b3 * s2 - a2 * b1 * s3;

                    // Решения
                    double x1 = D1 / D;
                    double x2 = D2 / D;
                    double x3 = D3 / D;

                    // Вывод результата
                    textBox13.Text = $"x1 = {x1}{Environment.NewLine}x2 = {x2}{Environment.NewLine}x3 = {x3}";
                }
                else
                {
                    textBox13.Text = "Система имеет бесконечно много решений или не имеет решений.";
                }
            }
            catch (FormatException)
            {
                MessageBox.Show("Пожалуйста, введите корректные числовые значения.", "Ошибка ввода", MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
            catch (Exception ex)
            {
                MessageBox.Show($"Произошла ошибка: {ex.Message}", "Ошибка", MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
        }
    }
}
