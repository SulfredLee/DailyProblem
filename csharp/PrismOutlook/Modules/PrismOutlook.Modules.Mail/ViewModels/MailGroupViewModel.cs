﻿using Prism.Commands;
using Prism.Mvvm;
using PrismOutlook.Business;
using PrismOutlook.Core;
using System;
using System.Collections.Generic;
using System.Collections.ObjectModel;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace PrismOutlook.Modules.Mail.ViewModels
{
    public class MailGroupViewModel : ViewModelBase
    {
        private ObservableCollection<NavigationItem> _items;
        public ObservableCollection<NavigationItem> Items
        {
            get { return _items; }
            set { SetProperty(ref _items, value); }
        }
        private DelegateCommand<NavigationItem> _selectedCommand;
        private readonly IApplicationCommands _applicationCommands;

        public DelegateCommand<NavigationItem> SelectedCommand =>
            _selectedCommand ?? (_selectedCommand = new DelegateCommand<NavigationItem>(ExecuteSelectedCommand));

        public MailGroupViewModel(IApplicationCommands applicationCommands)
        {
            GenerateMenu();
            _applicationCommands = applicationCommands;
        }
        void ExecuteSelectedCommand(NavigationItem navigationItem)
        {
            if (navigationItem != null)
                _applicationCommands.NavigateCommand.Execute(navigationItem.NavigationPath);
        }
        void GenerateMenu()
        {
            Items = new ObservableCollection<NavigationItem>();
            var root = new NavigationItem() { Caption = "Personal Folder", NavigationPath = "MailList?id=Default", IsExpanded = true };
            root.Items.Add(new NavigationItem() { Caption = Properties.Resources.Folder_Inbox, NavigationPath = GetNavigationPath(FolderParameters.Inbox) });
            root.Items.Add(new NavigationItem() { Caption = Properties.Resources.Folder_Deleted, NavigationPath = GetNavigationPath(FolderParameters.Deleted) });
            root.Items.Add(new NavigationItem() { Caption = Properties.Resources.Folder_Sent, NavigationPath = GetNavigationPath(FolderParameters.Sent) });

            Items.Add(root);
        }
        string GetNavigationPath(string folder)
        {
            return $"MailList?{FolderParameters.FolderKey}={folder}";
        }
    }
    public class FolderParameters
    {
        public const string FolderKey = "Folder";
        public const string Inbox = "Inbox";
        public const string Sent = "Sent";
        public const string Deleted = "Deleted";
    }
}
