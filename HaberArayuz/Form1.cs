using System;
using System.Data;
using MySql.Data.MySqlClient;


namespace HaberArayuz
{
    public partial class Form1 : Form
    {
        static string connectionString = "Server=172.21.54.148;Port=3306;Database=neis_news;User=NYP23-11;Password=Uludag9512357.;";
        MySqlConnection connection = new MySqlConnection(connectionString);

        public Form1()
        {
            InitializeComponent();
            InitializeTimer();
        }

        private void InitializeTimer()
        {
            // Timer ayarlarý
            timer1.Interval = 20000; // 10 saniyede bir güncelle
            timer1.Tick += new EventHandler(timer1_Tick); // Olay iþleyicisi
            timer1.Start(); // Timer'ý baþlat
        }

        private void timer1_Tick(object sender, EventArgs e)
        {
            LoadData(); // Veriyi yüklemek için metod
        }

        private void Form1_Load(object sender, EventArgs e)
        {
            LoadData();
        }

        private void LoadData()
        {
            try
            {
                connection.Open();
                string query = "SELECT * FROM news";
                MySqlDataAdapter da = new MySqlDataAdapter(query, connection);
                DataTable dt = new DataTable();
                da.Fill(dt);
                haberView.DataSource = dt;
            }
            catch (Exception ex)
            {
                MessageBox.Show("Bir hata oluþtu: " + ex.Message);
            }
            finally
            {
                if (connection.State == ConnectionState.Open)
                {
                    connection.Close();
                }
            }
        }

        private void haberCek_Click(object sender, EventArgs e)
        {
            
        }


        private void haberView_CellContentClick(object sender, DataGridViewCellEventArgs e)
        {

        }
    }
}
