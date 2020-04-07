using System.Drawing;
using System.Reflection;
using System.Windows.Forms;

namespace CaptureLabel
{
    partial class CaptureLabel
    {
        /// <summary>
        /// Required designer variable.
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        /// Clean up any resources being used.
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
        /// Required method for Designer support - do not modify
        /// the contents of this method with the code editor.
        /// </summary>
        private void InitializeComponent()
        {
            this.components = new System.ComponentModel.Container();
            this.groupBox1 = new System.Windows.Forms.GroupBox();
            this.csvPathTB = new System.Windows.Forms.TextBox();
            this.imagePathTB = new System.Windows.Forms.TextBox();
            this.button1 = new System.Windows.Forms.Button();
            this.label2 = new System.Windows.Forms.Label();
            this.label1 = new System.Windows.Forms.Label();
            this.menuStrip1 = new System.Windows.Forms.MenuStrip();
            this.fileToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.newToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.importToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.saveAsToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.exitToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.otherToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.aboutToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.groupBox2 = new System.Windows.Forms.GroupBox();
            this.imagePanel = new System.Windows.Forms.Panel();
            this.ZoomGB = new System.Windows.Forms.GroupBox();
            this.ZoomViewP = new System.Windows.Forms.Panel();
            this.bindingSource1 = new System.Windows.Forms.BindingSource(this.components);
            this.bindingSource2 = new System.Windows.Forms.BindingSource(this.components);
            this.statusStrip1 = new System.Windows.Forms.StatusStrip();
            this.inFocusLabel = new System.Windows.Forms.ToolStripStatusLabel();
            this.backgroundWorker1 = new System.ComponentModel.BackgroundWorker();
            this.FaceDetectionCB = new System.Windows.Forms.CheckBox();
            this.ModeGB = new System.Windows.Forms.GroupBox();
            this.FaceElementsCB = new System.Windows.Forms.CheckBox();
            this.lookAngleGB = new System.Windows.Forms.GroupBox();
            this.upCB = new System.Windows.Forms.CheckBox();
            this.rightCB = new System.Windows.Forms.CheckBox();
            this.leftCB = new System.Windows.Forms.CheckBox();
            this.downCB = new System.Windows.Forms.CheckBox();
            this.groupBox1.SuspendLayout();
            this.menuStrip1.SuspendLayout();
            this.groupBox2.SuspendLayout();
            this.ZoomGB.SuspendLayout();
            ((System.ComponentModel.ISupportInitialize)(this.bindingSource1)).BeginInit();
            ((System.ComponentModel.ISupportInitialize)(this.bindingSource2)).BeginInit();
            this.statusStrip1.SuspendLayout();
            this.ModeGB.SuspendLayout();
            this.lookAngleGB.SuspendLayout();
            this.SuspendLayout();
            // 
            // groupBox1
            // 
            this.groupBox1.Controls.Add(this.csvPathTB);
            this.groupBox1.Controls.Add(this.imagePathTB);
            this.groupBox1.Controls.Add(this.button1);
            this.groupBox1.Controls.Add(this.label2);
            this.groupBox1.Controls.Add(this.label1);
            this.groupBox1.Font = new System.Drawing.Font("Microsoft Sans Serif", 9.75F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.groupBox1.Location = new System.Drawing.Point(1055, 103);
            this.groupBox1.Name = "groupBox1";
            this.groupBox1.Size = new System.Drawing.Size(473, 192);
            this.groupBox1.TabIndex = 0;
            this.groupBox1.TabStop = false;
            this.groupBox1.Text = "Import data";
            // 
            // csvPathTB
            // 
            this.csvPathTB.Location = new System.Drawing.Point(12, 91);
            this.csvPathTB.Name = "csvPathTB";
            this.csvPathTB.Size = new System.Drawing.Size(455, 22);
            this.csvPathTB.TabIndex = 6;
            this.csvPathTB.TextChanged += new System.EventHandler(this.csvPathTB_TextChanged);
            // 
            // imagePathTB
            // 
            this.imagePathTB.Location = new System.Drawing.Point(12, 49);
            this.imagePathTB.Name = "imagePathTB";
            this.imagePathTB.Size = new System.Drawing.Size(455, 22);
            this.imagePathTB.TabIndex = 5;
            this.imagePathTB.TextChanged += new System.EventHandler(this.imagePathTB_TextChanged);
            // 
            // button1
            // 
            this.button1.Font = new System.Drawing.Font("Microsoft Sans Serif", 12F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.button1.Location = new System.Drawing.Point(189, 143);
            this.button1.Name = "button1";
            this.button1.Size = new System.Drawing.Size(117, 31);
            this.button1.TabIndex = 4;
            this.button1.Text = "Import data";
            this.button1.UseVisualStyleBackColor = true;
            this.button1.Click += new System.EventHandler(this.button1_Click);
            // 
            // label2
            // 
            this.label2.AutoSize = true;
            this.label2.Font = new System.Drawing.Font("Microsoft Sans Serif", 9.75F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.label2.Location = new System.Drawing.Point(9, 71);
            this.label2.Name = "label2";
            this.label2.Size = new System.Drawing.Size(64, 16);
            this.label2.TabIndex = 3;
            this.label2.Text = ".csv path:";
            // 
            // label1
            // 
            this.label1.AutoSize = true;
            this.label1.Font = new System.Drawing.Font("Microsoft Sans Serif", 9.75F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.label1.Location = new System.Drawing.Point(9, 29);
            this.label1.Name = "label1";
            this.label1.Size = new System.Drawing.Size(99, 16);
            this.label1.TabIndex = 2;
            this.label1.Text = "Image set path:";
            // 
            // menuStrip1
            // 
            this.menuStrip1.Items.AddRange(new System.Windows.Forms.ToolStripItem[] {
            this.fileToolStripMenuItem,
            this.otherToolStripMenuItem});
            this.menuStrip1.Location = new System.Drawing.Point(0, 0);
            this.menuStrip1.Name = "menuStrip1";
            this.menuStrip1.Size = new System.Drawing.Size(1576, 24);
            this.menuStrip1.TabIndex = 1;
            this.menuStrip1.Text = "menuStrip1";
            // 
            // fileToolStripMenuItem
            // 
            this.fileToolStripMenuItem.DropDownItems.AddRange(new System.Windows.Forms.ToolStripItem[] {
            this.newToolStripMenuItem,
            this.importToolStripMenuItem,
            this.saveAsToolStripMenuItem,
            this.exitToolStripMenuItem});
            this.fileToolStripMenuItem.Name = "fileToolStripMenuItem";
            this.fileToolStripMenuItem.Size = new System.Drawing.Size(37, 20);
            this.fileToolStripMenuItem.Text = "File";
            // 
            // newToolStripMenuItem
            // 
            this.newToolStripMenuItem.Name = "newToolStripMenuItem";
            this.newToolStripMenuItem.Size = new System.Drawing.Size(121, 22);
            this.newToolStripMenuItem.Text = "New";
            // 
            // importToolStripMenuItem
            // 
            this.importToolStripMenuItem.Name = "importToolStripMenuItem";
            this.importToolStripMenuItem.Size = new System.Drawing.Size(121, 22);
            this.importToolStripMenuItem.Text = "Save";
            this.importToolStripMenuItem.Click += new System.EventHandler(this.importToolStripMenuItem_Click);
            // 
            // saveAsToolStripMenuItem
            // 
            this.saveAsToolStripMenuItem.Name = "saveAsToolStripMenuItem";
            this.saveAsToolStripMenuItem.Size = new System.Drawing.Size(121, 22);
            this.saveAsToolStripMenuItem.Text = "Save as...";
            // 
            // exitToolStripMenuItem
            // 
            this.exitToolStripMenuItem.Name = "exitToolStripMenuItem";
            this.exitToolStripMenuItem.Size = new System.Drawing.Size(121, 22);
            this.exitToolStripMenuItem.Text = "Exit";
            // 
            // otherToolStripMenuItem
            // 
            this.otherToolStripMenuItem.DropDownItems.AddRange(new System.Windows.Forms.ToolStripItem[] {
            this.aboutToolStripMenuItem});
            this.otherToolStripMenuItem.Name = "otherToolStripMenuItem";
            this.otherToolStripMenuItem.Size = new System.Drawing.Size(49, 20);
            this.otherToolStripMenuItem.Text = "Other";
            // 
            // aboutToolStripMenuItem
            // 
            this.aboutToolStripMenuItem.Name = "aboutToolStripMenuItem";
            this.aboutToolStripMenuItem.Size = new System.Drawing.Size(107, 22);
            this.aboutToolStripMenuItem.Text = "About";
            // 
            // groupBox2
            // 
            this.groupBox2.Controls.Add(this.imagePanel);
            this.groupBox2.Location = new System.Drawing.Point(7, 42);
            this.groupBox2.Name = "groupBox2";
            this.groupBox2.Size = new System.Drawing.Size(1020, 830);
            this.groupBox2.TabIndex = 7;
            this.groupBox2.TabStop = false;
            this.groupBox2.Text = "Image View";
            // 
            // imagePanel
            // 
            this.imagePanel.Anchor = System.Windows.Forms.AnchorStyles.None;
            this.imagePanel.BackgroundImageLayout = System.Windows.Forms.ImageLayout.Zoom;
            this.imagePanel.BorderStyle = System.Windows.Forms.BorderStyle.FixedSingle;
            this.imagePanel.Location = new System.Drawing.Point(6, 19);
            this.imagePanel.Name = "imagePanel";
            this.imagePanel.Size = new System.Drawing.Size(1000, 800);
            this.imagePanel.TabIndex = 0;
            this.imagePanel.Paint += new System.Windows.Forms.PaintEventHandler(this.imagePanel_Paint);
            this.imagePanel.MouseDown += new System.Windows.Forms.MouseEventHandler(this.imagePanel_MouseDown);
            this.imagePanel.MouseMove += new System.Windows.Forms.MouseEventHandler(this.imagePanel_MouseMove);
            this.imagePanel.MouseUp += new System.Windows.Forms.MouseEventHandler(this.imagePanel_MouseUp);
            this.imagePanel.MouseWheel += new System.Windows.Forms.MouseEventHandler(this.imagePanel_MouseWheel);
            // 
            // ZoomGB
            // 
            this.ZoomGB.Controls.Add(this.ZoomViewP);
            this.ZoomGB.Location = new System.Drawing.Point(1055, 301);
            this.ZoomGB.Name = "ZoomGB";
            this.ZoomGB.Size = new System.Drawing.Size(73, 159);
            this.ZoomGB.TabIndex = 8;
            this.ZoomGB.TabStop = false;
            this.ZoomGB.Text = "Zoom View";
            // 
            // ZoomViewP
            // 
            this.ZoomViewP.Location = new System.Drawing.Point(7, 20);
            this.ZoomViewP.Name = "ZoomViewP";
            this.ZoomViewP.Size = new System.Drawing.Size(400, 400);
            this.ZoomViewP.TabIndex = 0;
            // 
            // statusStrip1
            // 
            this.statusStrip1.Items.AddRange(new System.Windows.Forms.ToolStripItem[] {
            this.inFocusLabel});
            this.statusStrip1.Location = new System.Drawing.Point(0, 944);
            this.statusStrip1.Name = "statusStrip1";
            this.statusStrip1.Size = new System.Drawing.Size(1576, 22);
            this.statusStrip1.TabIndex = 9;
            // 
            // inFocusLabel
            // 
            this.inFocusLabel.Name = "inFocusLabel";
            this.inFocusLabel.Size = new System.Drawing.Size(107, 17);
            this.inFocusLabel.Text = "Currently in focus: ";
            // 
            // FaceDetectionCB
            // 
            this.FaceDetectionCB.AutoSize = true;
            this.FaceDetectionCB.Checked = true;
            this.FaceDetectionCB.CheckState = System.Windows.Forms.CheckState.Checked;
            this.FaceDetectionCB.Location = new System.Drawing.Point(7, 19);
            this.FaceDetectionCB.Name = "FaceDetectionCB";
            this.FaceDetectionCB.Size = new System.Drawing.Size(97, 17);
            this.FaceDetectionCB.TabIndex = 10;
            this.FaceDetectionCB.Text = "Face detection";
            this.FaceDetectionCB.UseVisualStyleBackColor = true;
            this.FaceDetectionCB.CheckedChanged += new System.EventHandler(this.FaceDetectionCB_CheckedChanged);
            // 
            // ModeGB
            // 
            this.ModeGB.Controls.Add(this.FaceElementsCB);
            this.ModeGB.Controls.Add(this.FaceDetectionCB);
            this.ModeGB.Location = new System.Drawing.Point(1055, 42);
            this.ModeGB.Name = "ModeGB";
            this.ModeGB.Size = new System.Drawing.Size(221, 55);
            this.ModeGB.TabIndex = 7;
            this.ModeGB.TabStop = false;
            this.ModeGB.Text = "Mode";
            // 
            // FaceElementsCB
            // 
            this.FaceElementsCB.AutoSize = true;
            this.FaceElementsCB.Location = new System.Drawing.Point(121, 19);
            this.FaceElementsCB.Name = "FaceElementsCB";
            this.FaceElementsCB.Size = new System.Drawing.Size(95, 17);
            this.FaceElementsCB.TabIndex = 11;
            this.FaceElementsCB.Text = "Face elements";
            this.FaceElementsCB.UseVisualStyleBackColor = true;
            this.FaceElementsCB.CheckedChanged += new System.EventHandler(this.FaceElementsCB_CheckedChanged);
            // 
            // lookAngleGB
            // 
            this.lookAngleGB.Controls.Add(this.downCB);
            this.lookAngleGB.Controls.Add(this.upCB);
            this.lookAngleGB.Controls.Add(this.rightCB);
            this.lookAngleGB.Controls.Add(this.leftCB);
            this.lookAngleGB.Location = new System.Drawing.Point(1176, 321);
            this.lookAngleGB.Name = "lookAngleGB";
            this.lookAngleGB.Size = new System.Drawing.Size(126, 79);
            this.lookAngleGB.TabIndex = 1;
            this.lookAngleGB.TabStop = false;
            this.lookAngleGB.Text = "Look angle";
            // 
            // upCB
            // 
            this.upCB.AutoSize = true;
            this.upCB.Location = new System.Drawing.Point(6, 43);
            this.upCB.Name = "upCB";
            this.upCB.Size = new System.Drawing.Size(40, 17);
            this.upCB.TabIndex = 2;
            this.upCB.Text = "Up";
            this.upCB.UseVisualStyleBackColor = true;
            this.upCB.CheckedChanged += new System.EventHandler(this.upCB_CheckedChanged);
            // 
            // rightCB
            // 
            this.rightCB.AutoSize = true;
            this.rightCB.Location = new System.Drawing.Point(56, 19);
            this.rightCB.Name = "rightCB";
            this.rightCB.Size = new System.Drawing.Size(51, 17);
            this.rightCB.TabIndex = 1;
            this.rightCB.Text = "Right";
            this.rightCB.UseVisualStyleBackColor = true;
            this.rightCB.CheckedChanged += new System.EventHandler(this.rightCB_CheckedChanged);
            // 
            // leftCB
            // 
            this.leftCB.AutoSize = true;
            this.leftCB.Location = new System.Drawing.Point(6, 19);
            this.leftCB.Name = "leftCB";
            this.leftCB.Size = new System.Drawing.Size(44, 17);
            this.leftCB.TabIndex = 0;
            this.leftCB.Text = "Left";
            this.leftCB.UseVisualStyleBackColor = true;
            this.leftCB.CheckedChanged += new System.EventHandler(this.leftCB_CheckedChanged);
            // 
            // downCB
            // 
            this.downCB.AutoSize = true;
            this.downCB.Location = new System.Drawing.Point(56, 42);
            this.downCB.Name = "downCB";
            this.downCB.Size = new System.Drawing.Size(54, 17);
            this.downCB.TabIndex = 3;
            this.downCB.Text = "Down";
            this.downCB.UseVisualStyleBackColor = true;
            this.downCB.CheckedChanged += new System.EventHandler(this.downCB_CheckedChanged);
            // 
            // CaptureLabel
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 13F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(1576, 966);
            this.Controls.Add(this.lookAngleGB);
            this.Controls.Add(this.ModeGB);
            this.Controls.Add(this.statusStrip1);
            this.Controls.Add(this.ZoomGB);
            this.Controls.Add(this.groupBox2);
            this.Controls.Add(this.groupBox1);
            this.Controls.Add(this.menuStrip1);
            this.DoubleBuffered = true;
            this.KeyPreview = true;
            this.MainMenuStrip = this.menuStrip1;
            this.Name = "CaptureLabel";
            this.Text = "Capture Label";
            this.KeyDown += new System.Windows.Forms.KeyEventHandler(this.CaptureLabel_KeyDown);
            this.groupBox1.ResumeLayout(false);
            this.groupBox1.PerformLayout();
            this.menuStrip1.ResumeLayout(false);
            this.menuStrip1.PerformLayout();
            this.groupBox2.ResumeLayout(false);
            this.ZoomGB.ResumeLayout(false);
            ((System.ComponentModel.ISupportInitialize)(this.bindingSource1)).EndInit();
            ((System.ComponentModel.ISupportInitialize)(this.bindingSource2)).EndInit();
            this.statusStrip1.ResumeLayout(false);
            this.statusStrip1.PerformLayout();
            this.ModeGB.ResumeLayout(false);
            this.ModeGB.PerformLayout();
            this.lookAngleGB.ResumeLayout(false);
            this.lookAngleGB.PerformLayout();
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion

        private System.Windows.Forms.GroupBox groupBox1;
        private System.Windows.Forms.Label label1;
        private System.Windows.Forms.Label label2;
        private System.Windows.Forms.Button button1;
        private System.Windows.Forms.MenuStrip menuStrip1;
        private System.Windows.Forms.ToolStripMenuItem fileToolStripMenuItem;
        private System.Windows.Forms.ToolStripMenuItem newToolStripMenuItem;
        private System.Windows.Forms.ToolStripMenuItem importToolStripMenuItem;
        private System.Windows.Forms.ToolStripMenuItem saveAsToolStripMenuItem;
        private System.Windows.Forms.ToolStripMenuItem exitToolStripMenuItem;
        private System.Windows.Forms.ToolStripMenuItem otherToolStripMenuItem;
        private System.Windows.Forms.ToolStripMenuItem aboutToolStripMenuItem;
        private System.Windows.Forms.TextBox csvPathTB;
        private System.Windows.Forms.TextBox imagePathTB;
        private System.Windows.Forms.GroupBox groupBox2;
        private System.Windows.Forms.Panel imagePanel;
        private GroupBox ZoomGB;
        private Panel ZoomViewP;
        private BindingSource bindingSource1;
        private BindingSource bindingSource2;
        private StatusStrip statusStrip1;
        private ToolStripStatusLabel inFocusLabel;
        private System.ComponentModel.BackgroundWorker backgroundWorker1;
        private CheckBox FaceDetectionCB;
        private GroupBox ModeGB;
        private CheckBox FaceElementsCB;
        private GroupBox lookAngleGB;
        private CheckBox upCB;
        private CheckBox rightCB;
        private CheckBox leftCB;
        private CheckBox downCB;
    }
}

