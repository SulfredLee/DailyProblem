using Prism.Mvvm;
using System;
using System.Collections.Generic;
using System.Collections.ObjectModel;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace ListExample
{
    class MainWindowViewModel : BindableBase
    {
        public class ContextMenuItemNode : BindableBase
        {
            private string _menuName;
            public string MenuName
            {
                get => _menuName;
                set => SetProperty(ref _menuName, value);
            }
        }
        public class ServiceNode : BindableBase
        {
            private string _serviceName;
            public string ServiceName
            {
                get => _serviceName;
                set => SetProperty(ref _serviceName, value);
            }
            private string _instanceName;
            public string InstanceName
            {
                get => _instanceName;
                set => SetProperty(ref _instanceName, value);
            }
            private string _state;
            public string State
            {
                get => _state;
                set => SetProperty(ref _state, value);
            }
            private ObservableCollection<ContextMenuItemNode> _contextMenuList = new ObservableCollection<ContextMenuItemNode>();
            public ObservableCollection<ContextMenuItemNode> ContextMenuList
            {
                get => _contextMenuList;
                set => SetProperty(ref _contextMenuList, value);
            }
        }
        public ObservableCollection<ServiceNode> ServiceObjects { get; } = new ObservableCollection<ServiceNode>();
        
        public MainWindowViewModel()
        {
            for (int i = 0; i < 10; i++)
            {
                ObservableCollection<ContextMenuItemNode> menuList = new ObservableCollection<ContextMenuItemNode>();
                menuList.Add(new ContextMenuItemNode { MenuName = "ABC Item" });
                menuList.Add(new ContextMenuItemNode { MenuName = "EFG Item" });
                ServiceObjects.Add(new ServiceNode { InstanceName = "apple", ServiceName = "AP", State = "Normal", ContextMenuList = menuList });
            }
            for (int i = 0; i < 10; i++)
            {
                ServiceObjects.Add(new ServiceNode { InstanceName = "orange", ServiceName = "OR", State = "Degraded" });
            }
            for (int i = 0; i < 10; i++)
            {
                ServiceObjects.Add(new ServiceNode { InstanceName = "banana", ServiceName = "BA", State = "Down" });
            }
        }
    }
}
