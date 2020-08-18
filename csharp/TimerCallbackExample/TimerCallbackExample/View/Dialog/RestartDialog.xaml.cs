using System;
using System.Collections.Generic;
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
using System.Windows.Shapes;

namespace TimerCallbackExample.View.Dialog
{
    /// <summary>
    /// Interaction logic for RestartDialog.xaml
    /// </summary>
    public partial class RestartDialog : Window
    {
        private bool m_response = true;

        public RestartDialog()
        {
            InitializeComponent();
            CountForSec(20);
        }

        public bool GetResponse()
        {
            return m_response;
        }

        private void BtnDialogOk_Click(object sender, RoutedEventArgs e)
        {
            m_response = true;
            SystemCommands.CloseWindow(this);
        }

        private void BtnDialogCancel_Click(object sender, RoutedEventArgs e)
        {
            m_response = false;
            SystemCommands.CloseWindow(this);
        }

        private async void CountForSec(int count)
        {
            while (count > 0)
            {
                lbCountDown.Content = "Restart After: " + count.ToString() + " second";
                count--;
                await Task.Delay(1000);
            }
            m_response = true;
            SystemCommands.CloseWindow(this);
        }
    }
}
