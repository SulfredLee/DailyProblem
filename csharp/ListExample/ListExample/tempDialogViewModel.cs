using System.Collections.Generic;
using System.Collections.ObjectModel;
using System.Windows.Data;

namespace ListExample
{
    public class tempDialogViewModel
    {
        public class HostnameNode
        {
            private string _regionName;
            public string RegionName
            {
                get => _regionName;
                set => _regionName = value;
            }
            private string _hostname;
            public string Hostname
            {
                get => _hostname;
                set => _hostname = value;
            }

            private string _instanceName;
            public string InstanceName
            {
                get => _instanceName;
                set => _instanceName = value;
            }
        }

        private ListCollectionView _hostnameList;
        public ListCollectionView HostnameList
        {
            get => _hostnameList;
            set
            {
                _hostnameList = value;
                _hostnameList.GroupDescriptions.Add(new PropertyGroupDescription("RegionName"));
            }
        }

        public tempDialogViewModel()
        {
            ObservableCollection<HostnameNode> hostnameList = new ObservableCollection<HostnameNode>();
            hostnameList.Add(new HostnameNode { Hostname = "host ABC", InstanceName = "instance ABC", RegionName = "Region A" });
            hostnameList.Add(new HostnameNode { Hostname = "host ABC", InstanceName = "instance ABC", RegionName = "Region A" });
            hostnameList.Add(new HostnameNode { Hostname = "host ABC", InstanceName = "instance ABC", RegionName = "Region A" });
            hostnameList.Add(new HostnameNode { Hostname = "host ABC", InstanceName = "instance ABC", RegionName = "Region B" });
            hostnameList.Add(new HostnameNode { Hostname = "host ABC", InstanceName = "instance ABC", RegionName = "Region B" });
            hostnameList.Add(new HostnameNode { Hostname = "host ABC", InstanceName = "instance ABC", RegionName = "Region C" });
            hostnameList.Add(new HostnameNode { Hostname = "host ABC", InstanceName = "instance ABC", RegionName = "Region C" });
            hostnameList.Add(new HostnameNode { Hostname = "host ABC", InstanceName = "instance ABC", RegionName = "Region C" });

            HostnameList = new ListCollectionView(hostnameList);
        }
    }
}
