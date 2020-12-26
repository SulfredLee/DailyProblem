using System;
using System.Collections.Generic;
using System.Collections.ObjectModel;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Data;

namespace ListExample
{
    public class treeDatagridViewModel
    {
        public class Employee
        {
            public int ID { get; set; }
            public string Name { get; set; }
            public bool IsMale { get; set; }
            public EmployeeType Type { get; set; }
            public Uri SiteID { get; set; }
            public DateTime BirthDate { get; set; }
        }

        public enum EmployeeType
        {
            Normal,
            Supervisor,
            Manager
        }
        private ListCollectionView _employeesCollectionView;
        public ListCollectionView EmployeesCollectionView
        {
            get => _employeesCollectionView;
            set
            {
                _employeesCollectionView = value;
                _employeesCollectionView.GroupDescriptions.Add(new PropertyGroupDescription("Type"));
            }
        }

        public treeDatagridViewModel()
        {
            ObservableCollection<Employee> employees = new ObservableCollection<Employee>();
            employees.Add(new Employee { ID = 1, Name = "Mike", IsMale = true, Type = EmployeeType.Normal, SiteID = new Uri("http://localhost/4322"), BirthDate = new DateTime(1980, 1, 1) });
            employees.Add(new Employee { ID = 2, Name = "George", IsMale = true, Type = EmployeeType.Manager, SiteID = new Uri("http://localhost/4432"), BirthDate = new DateTime(1984, 2, 1) });
            employees.Add(new Employee { ID = 3, Name = "Vicky", IsMale = false, Type = EmployeeType.Supervisor, SiteID = new Uri("http://localhost/4872"), BirthDate = new DateTime(1975, 3, 1) });
            employees.Add(new Employee { ID = 4, Name = "Michael", IsMale = true, Type = EmployeeType.Normal, SiteID = new Uri("http://localhost/4322"), BirthDate = new DateTime(1988, 1, 1) });
            employees.Add(new Employee { ID = 5, Name = "Martin", IsMale = true, Type = EmployeeType.Normal, SiteID = new Uri("http://localhost/4432"), BirthDate = new DateTime(1989, 2, 1) });
            employees.Add(new Employee { ID = 6, Name = "Lucy", IsMale = false, Type = EmployeeType.Supervisor, SiteID = new Uri("http://localhost/4872"), BirthDate = new DateTime(1967, 3, 1) });
            employees.Add(new Employee { ID = 7, Name = "Brian", IsMale = true, Type = EmployeeType.Normal, SiteID = new Uri("http://localhost/4322"), BirthDate = new DateTime(1942, 1, 1) });
            employees.Add(new Employee { ID = 8, Name = "Santa", IsMale = true, Type = EmployeeType.Normal, SiteID = new Uri("http://localhost/4432"), BirthDate = new DateTime(1976, 2, 1) });
            employees.Add(new Employee { ID = 9, Name = "Ruby", IsMale = false, Type = EmployeeType.Normal, SiteID = new Uri("http://localhost/4872"), BirthDate = new DateTime(1990, 3, 1) });

            EmployeesCollectionView = new ListCollectionView(employees);
        }
    }
}
