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
            System.ComponentModel.ComponentResourceManager resources = new System.ComponentModel.ComponentResourceManager(typeof(CaptureLabel));
            this.FormClosing += CaptureLabel_FormClosing;
            this.groupBox1 = new System.Windows.Forms.GroupBox();
            this.csvPathTB = new System.Windows.Forms.TextBox();
            this.imagePathTB = new System.Windows.Forms.TextBox();
            this.button1 = new System.Windows.Forms.Button();
            this.label2 = new System.Windows.Forms.Label();
            this.label1 = new System.Windows.Forms.Label();
            this.menuStrip1 = new System.Windows.Forms.MenuStrip();
            this.fileToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.newToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.saveToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.saveAsToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.toolStripSeparator1 = new System.Windows.Forms.ToolStripSeparator();
            this.exportNormalizedCsvToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.toolStripSeparator2 = new System.Windows.Forms.ToolStripSeparator();
            this.exitToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.modeToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.faceDetectionToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.faceElementsDetectionToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.eyeContourDetectionToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.otherToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.aboutToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.groupBox2 = new System.Windows.Forms.GroupBox();
            this.imagePanel = new System.Windows.Forms.Panel();
            this.statusStrip1 = new System.Windows.Forms.StatusStrip();
            this.inFocusLabel = new System.Windows.Forms.ToolStripStatusLabel();
            this.imageCounterLabel = new System.Windows.Forms.ToolStripStatusLabel();
            this.lookAngleGB = new System.Windows.Forms.GroupBox();
            this.downCB = new System.Windows.Forms.CheckBox();
            this.upCB = new System.Windows.Forms.CheckBox();
            this.rightCB = new System.Windows.Forms.CheckBox();
            this.leftCB = new System.Windows.Forms.CheckBox();
            this.noFaceCB = new System.Windows.Forms.CheckBox();
            this.faceOptionsGB = new System.Windows.Forms.GroupBox();
            this.eyePropertiesGB = new System.Windows.Forms.GroupBox();
            this.REnotVCB = new System.Windows.Forms.CheckBox();
            this.LEnotVCB = new System.Windows.Forms.CheckBox();
            this.eyePropertiesCGB = new System.Windows.Forms.GroupBox();
            this.eyeClosedCB = new System.Windows.Forms.CheckBox();
            this.groupBox1.SuspendLayout();
            this.menuStrip1.SuspendLayout();
            this.groupBox2.SuspendLayout();
            this.statusStrip1.SuspendLayout();
            this.lookAngleGB.SuspendLayout();
            this.faceOptionsGB.SuspendLayout();
            this.eyePropertiesGB.SuspendLayout();
            this.eyePropertiesCGB.SuspendLayout();
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
            this.groupBox1.Location = new System.Drawing.Point(1055, 42);
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
            this.csvPathTB.TabIndex = 2;
            this.csvPathTB.TextChanged += new System.EventHandler(this.csvPathTB_TextChanged);
            // 
            // imagePathTB
            // 
            this.imagePathTB.Location = new System.Drawing.Point(12, 49);
            this.imagePathTB.Name = "imagePathTB";
            this.imagePathTB.Size = new System.Drawing.Size(455, 22);
            this.imagePathTB.TabIndex = 1;
            this.imagePathTB.TextChanged += new System.EventHandler(this.imagePathTB_TextChanged);
            // 
            // button1
            // 
            this.button1.Font = new System.Drawing.Font("Microsoft Sans Serif", 12F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.button1.Location = new System.Drawing.Point(189, 143);
            this.button1.Name = "button1";
            this.button1.Size = new System.Drawing.Size(117, 31);
            this.button1.TabIndex = 3;
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
            this.modeToolStripMenuItem,
            this.otherToolStripMenuItem});
            this.menuStrip1.Location = new System.Drawing.Point(0, 0);
            this.menuStrip1.Name = "menuStrip1";
            this.menuStrip1.Size = new System.Drawing.Size(1550, 24);
            this.menuStrip1.TabIndex = 1;
            this.menuStrip1.Text = "menuStrip1";
            // 
            // fileToolStripMenuItem
            // 
            this.fileToolStripMenuItem.DropDownItems.AddRange(new System.Windows.Forms.ToolStripItem[] {
            this.newToolStripMenuItem,
            this.saveToolStripMenuItem,
            this.saveAsToolStripMenuItem,
            this.toolStripSeparator1,
            this.exportNormalizedCsvToolStripMenuItem,
            this.toolStripSeparator2,
            this.exitToolStripMenuItem});
            this.fileToolStripMenuItem.Name = "fileToolStripMenuItem";
            this.fileToolStripMenuItem.Size = new System.Drawing.Size(37, 20);
            this.fileToolStripMenuItem.Text = "File";
            // 
            // newToolStripMenuItem
            // 
            this.newToolStripMenuItem.Image = ((System.Drawing.Image)(resources.GetObject("newToolStripMenuItem.Image")));
            this.newToolStripMenuItem.Name = "newToolStripMenuItem";
            this.newToolStripMenuItem.Size = new System.Drawing.Size(265, 22);
            this.newToolStripMenuItem.Text = "New";
            this.newToolStripMenuItem.Click += new System.EventHandler(this.newToolStripMenuItem_Click);
            // 
            // saveToolStripMenuItem
            // 
            this.saveToolStripMenuItem.Image = ((System.Drawing.Image)(resources.GetObject("saveToolStripMenuItem.Image")));
            this.saveToolStripMenuItem.Name = "saveToolStripMenuItem";
            this.saveToolStripMenuItem.ShortcutKeys = ((System.Windows.Forms.Keys)((System.Windows.Forms.Keys.Control | System.Windows.Forms.Keys.S)));
            this.saveToolStripMenuItem.Size = new System.Drawing.Size(265, 22);
            this.saveToolStripMenuItem.Text = "Save";
            this.saveToolStripMenuItem.Click += new System.EventHandler(this.saveToolStripMenuItem_Click);
            // 
            // saveAsToolStripMenuItem
            // 
            this.saveAsToolStripMenuItem.Image = ((System.Drawing.Image)(resources.GetObject("saveAsToolStripMenuItem.Image")));
            this.saveAsToolStripMenuItem.Name = "saveAsToolStripMenuItem";
            this.saveAsToolStripMenuItem.ShortcutKeys = ((System.Windows.Forms.Keys)(((System.Windows.Forms.Keys.Control | System.Windows.Forms.Keys.Shift) 
            | System.Windows.Forms.Keys.S)));
            this.saveAsToolStripMenuItem.Size = new System.Drawing.Size(265, 22);
            this.saveAsToolStripMenuItem.Text = "Save as...";
            this.saveAsToolStripMenuItem.Click += new System.EventHandler(this.saveAsToolStripMenuItem_Click);
            // 
            // toolStripSeparator1
            // 
            this.toolStripSeparator1.Name = "toolStripSeparator1";
            this.toolStripSeparator1.Size = new System.Drawing.Size(262, 6);
            // 
            // exportNormalizedCsvToolStripMenuItem
            // 
            this.exportNormalizedCsvToolStripMenuItem.Image = ((System.Drawing.Image)(resources.GetObject("exportNormalizedCsvToolStripMenuItem.Image")));
            this.exportNormalizedCsvToolStripMenuItem.Name = "exportNormalizedCsvToolStripMenuItem";
            this.exportNormalizedCsvToolStripMenuItem.ShortcutKeys = ((System.Windows.Forms.Keys)(((System.Windows.Forms.Keys.Control | System.Windows.Forms.Keys.Shift) 
            | System.Windows.Forms.Keys.E)));
            this.exportNormalizedCsvToolStripMenuItem.Size = new System.Drawing.Size(265, 22);
            this.exportNormalizedCsvToolStripMenuItem.Text = "Export normalized .csv";
            this.exportNormalizedCsvToolStripMenuItem.Click += new System.EventHandler(this.exportNormalizedCsvToolStripMenuItem_Click);
            // 
            // toolStripSeparator2
            // 
            this.toolStripSeparator2.Name = "toolStripSeparator2";
            this.toolStripSeparator2.Size = new System.Drawing.Size(262, 6);
            // 
            // exitToolStripMenuItem
            // 
            this.exitToolStripMenuItem.Name = "exitToolStripMenuItem";
            this.exitToolStripMenuItem.Size = new System.Drawing.Size(265, 22);
            this.exitToolStripMenuItem.Text = "Exit";
            this.exitToolStripMenuItem.Click += new System.EventHandler(this.exitToolStripMenuItem_Click);
            // 
            // modeToolStripMenuItem
            // 
            this.modeToolStripMenuItem.DropDownItems.AddRange(new System.Windows.Forms.ToolStripItem[] {
            this.faceDetectionToolStripMenuItem,
            this.faceElementsDetectionToolStripMenuItem,
            this.eyeContourDetectionToolStripMenuItem});
            this.modeToolStripMenuItem.Name = "modeToolStripMenuItem";
            this.modeToolStripMenuItem.Size = new System.Drawing.Size(50, 20);
            this.modeToolStripMenuItem.Text = "Mode";
            // 
            // faceDetectionToolStripMenuItem
            // 
            this.faceDetectionToolStripMenuItem.Checked = true;
            this.faceDetectionToolStripMenuItem.CheckState = System.Windows.Forms.CheckState.Checked;
            this.faceDetectionToolStripMenuItem.Name = "faceDetectionToolStripMenuItem";
            this.faceDetectionToolStripMenuItem.Size = new System.Drawing.Size(202, 22);
            this.faceDetectionToolStripMenuItem.Text = "Face detection";
            this.faceDetectionToolStripMenuItem.Click += new System.EventHandler(this.faceDetectionToolStripMenuItem_Click);
            // 
            // faceElementsDetectionToolStripMenuItem
            // 
            this.faceElementsDetectionToolStripMenuItem.Name = "faceElementsDetectionToolStripMenuItem";
            this.faceElementsDetectionToolStripMenuItem.Size = new System.Drawing.Size(202, 22);
            this.faceElementsDetectionToolStripMenuItem.Text = "Face elements detection";
            this.faceElementsDetectionToolStripMenuItem.Click += new System.EventHandler(this.faceElementsDetectionToolStripMenuItem_Click);
            // 
            // eyeContourDetectionToolStripMenuItem
            // 
            this.eyeContourDetectionToolStripMenuItem.Name = "eyeContourDetectionToolStripMenuItem";
            this.eyeContourDetectionToolStripMenuItem.Size = new System.Drawing.Size(202, 22);
            this.eyeContourDetectionToolStripMenuItem.Text = "Eye contour detection";
            this.eyeContourDetectionToolStripMenuItem.Click += new System.EventHandler(this.eyeContourDetectionToolStripMenuItem_Click);
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
            this.aboutToolStripMenuItem.Image = ((System.Drawing.Image)(resources.GetObject("aboutToolStripMenuItem.Image")));
            this.aboutToolStripMenuItem.Name = "aboutToolStripMenuItem";
            this.aboutToolStripMenuItem.Size = new System.Drawing.Size(107, 22);
            this.aboutToolStripMenuItem.Text = "About";
            this.aboutToolStripMenuItem.Click += new System.EventHandler(this.aboutToolStripMenuItem_Click);
            // 
            // groupBox2
            // 
            this.groupBox2.Controls.Add(this.imagePanel);
            this.groupBox2.Location = new System.Drawing.Point(7, 42);
            this.groupBox2.Name = "groupBox2";
            this.groupBox2.Size = new System.Drawing.Size(1020, 830);
            this.groupBox2.TabIndex = 9;
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
            // statusStrip1
            // 
            this.statusStrip1.Items.AddRange(new System.Windows.Forms.ToolStripItem[] {
            this.inFocusLabel,
            this.imageCounterLabel});
            this.statusStrip1.Location = new System.Drawing.Point(0, 967);
            this.statusStrip1.Name = "statusStrip1";
            this.statusStrip1.Size = new System.Drawing.Size(1550, 24);
            this.statusStrip1.TabIndex = 9;
            // 
            // inFocusLabel
            // 
            this.inFocusLabel.BorderSides = System.Windows.Forms.ToolStripStatusLabelBorderSides.Right;
            this.inFocusLabel.BorderStyle = System.Windows.Forms.Border3DStyle.Etched;
            this.inFocusLabel.Name = "inFocusLabel";
            this.inFocusLabel.Size = new System.Drawing.Size(1515, 19);
            this.inFocusLabel.Spring = true;
            this.inFocusLabel.Text = "Currently in focus: ";
            this.inFocusLabel.TextAlign = System.Drawing.ContentAlignment.MiddleLeft;
            // 
            // imageCounterLabel
            // 
            this.imageCounterLabel.Name = "imageCounterLabel";
            this.imageCounterLabel.RightToLeft = System.Windows.Forms.RightToLeft.No;
            this.imageCounterLabel.Size = new System.Drawing.Size(0, 19);
            this.imageCounterLabel.TextAlign = System.Drawing.ContentAlignment.MiddleLeft;
            // 
            // lookAngleGB
            // 
            this.lookAngleGB.Controls.Add(this.downCB);
            this.lookAngleGB.Controls.Add(this.upCB);
            this.lookAngleGB.Controls.Add(this.rightCB);
            this.lookAngleGB.Controls.Add(this.leftCB);
            this.lookAngleGB.Location = new System.Drawing.Point(1055, 252);
            this.lookAngleGB.Name = "lookAngleGB";
            this.lookAngleGB.Size = new System.Drawing.Size(126, 69);
            this.lookAngleGB.TabIndex = 4;
            this.lookAngleGB.TabStop = false;
            this.lookAngleGB.Text = "Look angle";
            // 
            // downCB
            // 
            this.downCB.AutoSize = true;
            this.downCB.Location = new System.Drawing.Point(56, 42);
            this.downCB.Name = "downCB";
            this.downCB.Size = new System.Drawing.Size(54, 17);
            this.downCB.TabIndex = 8;
            this.downCB.Text = "Down";
            this.downCB.UseVisualStyleBackColor = true;
            this.downCB.CheckedChanged += new System.EventHandler(this.downCB_CheckedChanged);
            // 
            // upCB
            // 
            this.upCB.AutoSize = true;
            this.upCB.Location = new System.Drawing.Point(6, 43);
            this.upCB.Name = "upCB";
            this.upCB.Size = new System.Drawing.Size(40, 17);
            this.upCB.TabIndex = 7;
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
            this.rightCB.TabIndex = 6;
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
            this.leftCB.TabIndex = 5;
            this.leftCB.Text = "Left";
            this.leftCB.UseVisualStyleBackColor = true;
            this.leftCB.CheckedChanged += new System.EventHandler(this.leftCB_CheckedChanged);
            // 
            // noFaceCB
            // 
            this.noFaceCB.AutoSize = true;
            this.noFaceCB.Location = new System.Drawing.Point(6, 17);
            this.noFaceCB.Name = "noFaceCB";
            this.noFaceCB.Size = new System.Drawing.Size(64, 17);
            this.noFaceCB.TabIndex = 10;
            this.noFaceCB.Text = "No face";
            this.noFaceCB.UseVisualStyleBackColor = true;
            // 
            // faceOptionsGB
            // 
            this.faceOptionsGB.Controls.Add(this.noFaceCB);
            this.faceOptionsGB.Location = new System.Drawing.Point(1055, 327);
            this.faceOptionsGB.Name = "faceOptionsGB";
            this.faceOptionsGB.Size = new System.Drawing.Size(126, 42);
            this.faceOptionsGB.TabIndex = 11;
            this.faceOptionsGB.TabStop = false;
            this.faceOptionsGB.Text = "Face options";
            // 
            // eyePropertiesGB
            // 
            this.eyePropertiesGB.Controls.Add(this.REnotVCB);
            this.eyePropertiesGB.Controls.Add(this.LEnotVCB);
            this.eyePropertiesGB.Location = new System.Drawing.Point(1055, 327);
            this.eyePropertiesGB.Name = "eyePropertiesGB";
            this.eyePropertiesGB.Size = new System.Drawing.Size(200, 69);
            this.eyePropertiesGB.TabIndex = 13;
            this.eyePropertiesGB.TabStop = false;
            this.eyePropertiesGB.Text = "Eye properties ";
            this.eyePropertiesGB.Visible = false;
            // 
            // REnotVCB
            // 
            this.REnotVCB.AutoSize = true;
            this.REnotVCB.Location = new System.Drawing.Point(6, 42);
            this.REnotVCB.Name = "REnotVCB";
            this.REnotVCB.Size = new System.Drawing.Size(121, 17);
            this.REnotVCB.TabIndex = 1;
            this.REnotVCB.Text = "Right eye not visible";
            this.REnotVCB.UseVisualStyleBackColor = true;
            this.REnotVCB.CheckedChanged += new System.EventHandler(this.REnotVCB_CheckedChanged);
            // 
            // LEnotVCB
            // 
            this.LEnotVCB.AutoSize = true;
            this.LEnotVCB.Location = new System.Drawing.Point(6, 19);
            this.LEnotVCB.Name = "LEnotVCB";
            this.LEnotVCB.Size = new System.Drawing.Size(114, 17);
            this.LEnotVCB.TabIndex = 0;
            this.LEnotVCB.Text = "Left eye not visible";
            this.LEnotVCB.UseVisualStyleBackColor = true;
            this.LEnotVCB.CheckedChanged += new System.EventHandler(this.LEnotVCB_CheckedChanged);
            // 
            // eyePropertiesCGB
            // 
            this.eyePropertiesCGB.Controls.Add(this.eyeClosedCB);
            this.eyePropertiesCGB.Location = new System.Drawing.Point(1055, 327);
            this.eyePropertiesCGB.Name = "eyePropertiesCGB";
            this.eyePropertiesCGB.Size = new System.Drawing.Size(200, 43);
            this.eyePropertiesCGB.TabIndex = 14;
            this.eyePropertiesCGB.TabStop = false;
            this.eyePropertiesCGB.Text = "Eye properties";
            // 
            // eyeClosedCB
            // 
            this.eyeClosedCB.AutoSize = true;
            this.eyeClosedCB.Location = new System.Drawing.Point(6, 19);
            this.eyeClosedCB.Name = "eyeClosedCB";
            this.eyeClosedCB.Size = new System.Drawing.Size(78, 17);
            this.eyeClosedCB.TabIndex = 0;
            this.eyeClosedCB.Text = "Eye closed";
            this.eyeClosedCB.UseVisualStyleBackColor = true;
            // 
            // CaptureLabel
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 13F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(1550, 991);
            this.Controls.Add(this.eyePropertiesCGB);
            this.Controls.Add(this.eyePropertiesGB);
            this.Controls.Add(this.faceOptionsGB);
            this.Controls.Add(this.lookAngleGB);
            this.Controls.Add(this.statusStrip1);
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
            this.statusStrip1.ResumeLayout(false);
            this.statusStrip1.PerformLayout();
            this.lookAngleGB.ResumeLayout(false);
            this.lookAngleGB.PerformLayout();
            this.faceOptionsGB.ResumeLayout(false);
            this.faceOptionsGB.PerformLayout();
            this.eyePropertiesGB.ResumeLayout(false);
            this.eyePropertiesGB.PerformLayout();
            this.eyePropertiesCGB.ResumeLayout(false);
            this.eyePropertiesCGB.PerformLayout();
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
        private System.Windows.Forms.ToolStripMenuItem saveToolStripMenuItem;
        private System.Windows.Forms.ToolStripMenuItem saveAsToolStripMenuItem;
        private System.Windows.Forms.ToolStripMenuItem exitToolStripMenuItem;
        private System.Windows.Forms.ToolStripMenuItem otherToolStripMenuItem;
        private System.Windows.Forms.ToolStripMenuItem aboutToolStripMenuItem;
        private System.Windows.Forms.TextBox csvPathTB;
        private System.Windows.Forms.TextBox imagePathTB;
        private System.Windows.Forms.GroupBox groupBox2;
        private System.Windows.Forms.Panel imagePanel;
        private StatusStrip statusStrip1;
        private ToolStripStatusLabel inFocusLabel;
        private GroupBox lookAngleGB;
        private CheckBox upCB;
        private CheckBox rightCB;
        private CheckBox leftCB;
        private CheckBox downCB;
        private ToolStripMenuItem modeToolStripMenuItem;
        private ToolStripMenuItem faceDetectionToolStripMenuItem;
        private ToolStripMenuItem faceElementsDetectionToolStripMenuItem;
        private ToolStripSeparator toolStripSeparator1;
        private ToolStripMenuItem exportNormalizedCsvToolStripMenuItem;
        private ToolStripSeparator toolStripSeparator2;
        private CheckBox noFaceCB;
        private GroupBox faceOptionsGB;
        private GroupBox eyePropertiesGB;
        private CheckBox REnotVCB;
        private CheckBox LEnotVCB;
        private ToolStripMenuItem eyeContourDetectionToolStripMenuItem;
        private GroupBox eyePropertiesCGB;
        private CheckBox eyeClosedCB;
        private ToolStripStatusLabel imageCounterLabel;
    }
}

