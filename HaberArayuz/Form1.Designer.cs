namespace HaberArayuz
{
    partial class Form1
    {
        /// <summary>
        ///  Required designer variable.
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        ///  Clean up any resources being used.
        /// </summary>
        /// <param name="disposing">true if managed resources should be disposed; otherwise, false.</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Windows Form Designer generated code

        /// <summary>
        ///  Required method for Designer support - do not modify
        ///  the contents of this method with the code editor.
        /// </summary>
        private void InitializeComponent()
        {
            components = new System.ComponentModel.Container();
            label1 = new Label();
            haberView = new DataGridView();
            haberCek = new Button();
            timer1 = new System.Windows.Forms.Timer(components);
            ((System.ComponentModel.ISupportInitialize)haberView).BeginInit();
            SuspendLayout();
            // 
            // label1
            // 
            label1.AutoSize = true;
            label1.Font = new Font("Tahoma", 18F, FontStyle.Regular, GraphicsUnit.Point);
            label1.Location = new Point(559, 52);
            label1.Name = "label1";
            label1.Size = new Size(248, 36);
            label1.TabIndex = 0;
            label1.Text = "Haber Çeviri Botu";
            // 
            // haberView
            // 
            haberView.AutoSizeColumnsMode = DataGridViewAutoSizeColumnsMode.Fill;
            haberView.ColumnHeadersHeightSizeMode = DataGridViewColumnHeadersHeightSizeMode.AutoSize;
            haberView.Location = new Point(40, 119);
            haberView.Name = "haberView";
            haberView.RowHeadersWidth = 51;
            haberView.RowTemplate.Height = 29;
            haberView.Size = new Size(1376, 476);
            haberView.TabIndex = 1;
            haberView.CellContentClick += haberView_CellContentClick;
            // 
            // haberCek
            // 
            haberCek.Location = new Point(638, 623);
            haberCek.Name = "haberCek";
            haberCek.Size = new Size(188, 56);
            haberCek.TabIndex = 2;
            haberCek.Text = "Haberi İncele";
            haberCek.UseVisualStyleBackColor = true;
            haberCek.Click += haberCek_Click;
            // 
            // Form1
            // 
            AutoScaleDimensions = new SizeF(8F, 20F);
            AutoScaleMode = AutoScaleMode.Font;
            ClientSize = new Size(1462, 733);
            Controls.Add(haberCek);
            Controls.Add(haberView);
            Controls.Add(label1);
            Name = "Form1";
            Text = "Haber Çeviri Botu";
            Load += Form1_Load;
            ((System.ComponentModel.ISupportInitialize)haberView).EndInit();
            ResumeLayout(false);
            PerformLayout();
        }

        #endregion

        private Label label1;
        private DataGridView haberView;
        private Button haberCek;
        private System.Windows.Forms.Timer timer1;
    }
}
