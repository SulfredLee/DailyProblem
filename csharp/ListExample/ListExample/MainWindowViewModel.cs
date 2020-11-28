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
        }
        public ObservableCollection<ServiceNode> ServiceObjects { get; } = new ObservableCollection<ServiceNode>();
        public MainWindowViewModel()
        {
            for (int i = 0; i < 10; i++)
            {
                ServiceObjects.Add(new ServiceNode { InstanceName = "apple", ServiceName = "AP", State = "Normal" });
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
