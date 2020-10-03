using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows;

namespace WPFControlStudy.ViewModel
{
    class MainWindowViewModel
    {
        public int Height { get; set; }
        public int Width { get; set; }
        public string Title { get; set; }
        public List<TodoItem> todoItemList { get; set; }

        public class TodoItem
        {
            public string Title { get; set; }
            public int Completion { get; set; }
        }
        public MainWindowViewModel()
        {
            this.Height = 100;
            this.Width = 200;

            todoItemList = new List<TodoItem>();
            todoItemList.Add(new TodoItem() { Title = "Complete this WPF tutorial", Completion = 45 });
            todoItemList.Add(new TodoItem() { Title = "Learn C#", Completion = 80 });
            todoItemList.Add(new TodoItem() { Title = "Wash the car", Completion = 0 });
        }
    }
}
