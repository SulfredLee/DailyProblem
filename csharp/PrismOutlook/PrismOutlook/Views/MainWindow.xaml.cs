﻿using Infragistics.Themes;
using Infragistics.Windows.OutlookBar;
using Infragistics.Windows.Ribbon;
using Prism.Regions;
using PrismOutlook.Core;
using System.Windows;

namespace PrismOutlook.Views
{
    /// <summary>
    /// Interaction logic for MainWindow.xaml
    /// </summary>
    public partial class MainWindow : XamRibbonWindow
    {
        private readonly IApplicationCommands _applicationCommands;
        public MainWindow(IApplicationCommands applicationCommands)
        {
            InitializeComponent();

            Infragistics.Themes.ThemeManager.ApplicationTheme = new Office2013Theme();
            _applicationCommands = applicationCommands;
        }
        private void XamOutlookBar_SelectedGroupChanged(object sender, RoutedEventArgs e)
        {
            IOutlookBarGroup group = ((XamOutlookBar)sender).SelectedGroup as IOutlookBarGroup;
            if (group != null)
            {
                _applicationCommands.NavigateCommand.Execute(group.DefaultNavigationPath);
            }
        }
    }
}
