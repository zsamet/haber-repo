using MySql.Data.MySqlClient;
using System;
using System.Windows.Forms;

namespace HaberArayuz
{
    public partial class haberGoster : Form
    {
        string haberId;
        static string connectionString = "Server=172.21.54.148;Port=3306;Database=neis_news;User=NYP23-11;Password=Uludag9512357.;";
        MySqlConnection connection = new MySqlConnection(connectionString);

        public haberGoster(string haberBasligi, string haberIcerigi, string _haberId)
        {
            InitializeComponent();
            richTextBox1.Text = haberBasligi; // Örnek olarak haber başlığını kullanıyoruz
            richTextBox2.Text = haberIcerigi; // Örnek olarak haber içeriğini kullanıyoruz
            haberId = _haberId;
        }

        private void haberIncele_Click(object sender, EventArgs e)
        {
            // richTextBox3 içeriğini al
            string richTextBoxText = richTextBox3.Text.Trim(); // Başta ve sondaki boşlukları kaldır

            using (MySqlConnection connection = new MySqlConnection(connectionString))
            {
                try
                {
                    connection.Open();
                    string updateQuery = "UPDATE news SET news_yayin = @news_yayin WHERE ID = @ID";

                    using (MySqlCommand cmd = new MySqlCommand(updateQuery, connection))
                    {
                        // Eğer richTextBoxText boşsa, DBNull.Value kullanarak NULL olarak kaydet
                        cmd.Parameters.AddWithValue("@news_yayin", string.IsNullOrEmpty(richTextBoxText) ? (object)DBNull.Value : richTextBoxText);
                        cmd.Parameters.AddWithValue("@ID", haberId);
                        cmd.ExecuteNonQuery();

                        MessageBox.Show("Metin başarıyla kaydedildi.");
                    }
                }
                catch (Exception ex)
                {
                    MessageBox.Show("Hata oluştu: " + ex.Message);
                }
            }
        }

        private void label2_Click(object sender, EventArgs e)
        {

        }
    }
}
