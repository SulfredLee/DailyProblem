using Infragistics.Controls.Menus;
using Infragistics.Windows.OutlookBar;
using Infragistics.Windows.Ribbon;
using PrismOutlook.Bussiness;
using PrismOutlook.Core;
using PrismOutlook.Modules.Mail.ViewModels;
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
using System.Windows.Navigation;
using System.Windows.Shapes;

namespace PrismOutlook.Modules.Mail.Menus
{
    /// <summary>
    /// Interaction logic for MailGroup.xaml
    /// </summary>
    public partial class MailGroup : OutlookBarGroup, IOutlookBarGroup
    {
        // NavigationItem _selectedItem;
        public MailGroup()
        {
            InitializeComponent();
            _dataTree.Loaded += DataTree_Loaded;
            // _dataTree.ActiveNodeChanging += DataTree_ActiveNodeChanging;
        }

        private void DataTree_ActiveNodeChanging(object sender, ActiveNodeChangingEventArgs e)
        {
            // this method can keep tracing the changing, no needed for this project

            /*
            _selectedItem = e.NewActiveTreeNode.Data as NavigationItem;
            if (_selectedItem != null)
            { 
            }*/
        }

        private void DataTree_Loaded(object sender, RoutedEventArgs e)
        {
            _dataTree.Loaded -= DataTree_Loaded;

            var parentNode = _dataTree.Nodes[0];
            var nodeToSelect = parentNode.Nodes[0];
            nodeToSelect.IsSelected = true;
        }

        public string DefaultNavigationPath
        {
            get
            {
                var item = _dataTree.SelectionSettings.SelectedNodes[0] as XamDataTreeNode;
                if (item != null)
                    return ((NavigationItem)item.Data).NavigationPath;

                return $"MailList?{FolderParameters.FolderKey}={FolderParameters.Inbox}";
            }
        }
    }
}
