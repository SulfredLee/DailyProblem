using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading;
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
using System.Windows.Threading;

namespace TaskKilledException
{
    /// <summary>
    /// Interaction logic for MainWindow.xaml
    /// </summary>
    public partial class MainWindow : Window
    {
        private readonly CancellationTokenSource _shutDown = new CancellationTokenSource();
        private CancellationToken _token = new CancellationToken(false);
        private int _testSelection = 0;

        public MainWindow()
        {
            InitializeComponent();
            _testSelection = 2;
            Thread runningTH = new Thread(TestProgressUpdate) { IsBackground = true };
            runningTH.Start();
            Thread shutdownTH = new Thread(ShutdownAction) { IsBackground = true };
            shutdownTH.Start();
        }

        private void TestProgressUpdate()
        {
            int i = 0;
            while (true)
            {
                i = (i + 10) % 100;

                switch (_testSelection)
                {
                    case 0:
                        {
                            if (!Dispatcher.HasShutdownStarted)
                            {
                                Dispatcher.Invoke(() => { testProBar.Value = i; }, DispatcherPriority.Normal, _token);
                            }
                        }
                        break;
                    case 1:
                    case 2:
                        {
                            Dispatcher.Invoke(() => { testProBar.Value = i; });
                        }
                        break;
                    default:
                        break;
                }


                Thread.Sleep(5);
            }
        }

        private void ShutdownAction()
        {
            Thread.Sleep(1500);
            switch (_testSelection)
            {
                case 0:
                    Dispatcher.InvokeShutdown(); // task cancel exception comes up
                    break;
                case 1:
                    Dispatcher.Invoke(() => { Application.Current.Shutdown(); }); // task cancel exception comes up
                    break;
                case 2:
                    Environment.Exit(0); // task cancel exception solved
                    break;
                default:
                    break;
            }
        }
    }
}
