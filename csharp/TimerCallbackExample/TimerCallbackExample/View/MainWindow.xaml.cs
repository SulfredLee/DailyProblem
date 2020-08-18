using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Data;
using System.Windows.Documents;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Navigation;
using System.Windows.Shapes;
using Microsoft.Win32;
using TimerCallbackExample.View.Dialog;
using TimerCallbackExample.Services;

namespace TimerCallbackExample
{
    /// <summary>
    /// Interaction logic for MainWindow.xaml
    /// </summary>
    public partial class MainWindow : Window
    {
        private System.Threading.Timer testTimer = null;
        // need dispatcher timer to due with the Signle Threaded Apartment(STA) problem
        // STA problem is due to one want to use the backend thread to control UI things
        private System.Windows.Threading.DispatcherTimer testDispatcherTimer = null;
        private EventTimer m_myTimer = null;

        public MainWindow()
        {
            InitializeComponent();

            // Regist to System time change event
            SystemEvents.TimeChanged += OnTimeChangeEvent;

            double TimeOfExecution = 5; // 0500

            DateTime now = DateTime.Now;
            DateTime today5am = now.Date.AddHours(TimeOfExecution);
            today5am = today5am.AddMinutes(25);
            Debug.WriteLine(today5am.ToString());
            DateTime next5am = now <= today5am ? today5am : today5am.AddDays(1);
            DateTime nextNow = now.Date.AddSeconds(5);

            // nextNow - DateTime.Now
            // this.testTimer = new System.Threading.Timer(new TimerCallback(this.OnRestartCallback), null, nextNow.Subtract(now.Date), TimeSpan.FromSeconds(15));

            // this.testDispatcherTimer = new System.Windows.Threading.DispatcherTimer();
            // this.testDispatcherTimer.Tick += new EventHandler(OnRestartCallback);
            // this.testDispatcherTimer.Interval = nextNow.Subtract(now.Date);
            // this.testDispatcherTimer.Start();

            m_myTimer = new EventTimer(new EventHandler(OnRestartCallback), nextNow, TimeSpan.FromSeconds(10));
        }

        private void OnTimeChangeEvent(object sender, EventArgs e)
        {
            MessageBox.Show("Time Changed");
        }

        // private void OnRestartCallback(Object stateInfo) // TimerCallback use case
        private void OnRestartCallback(object sender, EventArgs e)
        {
            ShowRestartDialog();
            // this.testDispatcherTimer.Interval = TimeSpan.FromSeconds(15);
        }

        private void ShowRestartDialog()
        {
            Application.Current.Windows[0].Opacity = 0;
            RestartDialog restartDialog = new RestartDialog();
            restartDialog.ShowDialog();
            Application.Current.Windows[0].Opacity = 100;
            bool restartResponse = restartDialog.GetResponse();

            if (restartResponse)
                MessageBox.Show("Do restart");
            else
                MessageBox.Show("No restart");
        }
    }
}
