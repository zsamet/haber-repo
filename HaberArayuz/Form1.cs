using System;
using MySql.Data.MySqlClient;
namespace HaberArayuz

{
    public partial class Form1 : Form
    {
        public Form1()
        {
            InitializeComponent();
        }

        private void Form1_Load(object sender, EventArgs e)
        {
            
        }
        static string connectionString = "Server=172.21.54.148;Port=3306;Database=NYP23-11;User=NYP23-11;Password=Uludag9512357.;";
        MySqlConnection connection = new MySqlConnection(connectionString);
    }
}
