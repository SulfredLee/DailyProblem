using Prism.Commands;
using Prism.Mvvm;
using System;
using System.Collections.Generic;
using System.Collections.ObjectModel;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Input;

namespace ListExample
{
    class MainWindowViewModel : BindableBase
    {
        public class MenuNode : BindableBase
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
            public ObservableCollection<MenuNode> ContextMenuList { get; } = new ObservableCollection<MenuNode>();
        }
        public ObservableCollection<ServiceNode> ServiceObjects { get; } = new ObservableCollection<ServiceNode>();
        
        public MainWindowViewModel()
        {
            for (int i = 0; i < 10; i++)
            {
                ServiceNode tempNode = new ServiceNode { InstanceName = "apple", ServiceName = "AP", State = "Normal" };
                tempNode.ContextMenuList.Add(new MenuNode { MenuName = "A Item" });
                tempNode.ContextMenuList.Add(new MenuNode { MenuName = "B Item" });
                tempNode.ContextMenuList.Add(new MenuNode { MenuName = "C Item" });
                ServiceObjects.Add(tempNode);
            }
            for (int i = 0; i < 10; i++)
            {
                ServiceObjects.Add(new ServiceNode { InstanceName = "orange", ServiceName = "OR", State = "Degraded" });
            }
            for (int i = 0; i < 10; i++)
            {
                ServiceObjects.Add(new ServiceNode { InstanceName = "banana", ServiceName = "BA", State = "Down" });
            }
            ConfirmButtonCommand = new DelegateCommand(HandleConfirmButtonCommand);
        }
        public ICommand ConfirmButtonCommand { get; }

        private void HandleConfirmButtonCommand()
        {
            
        }
    }
}
