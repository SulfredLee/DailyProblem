﻿using PrismOutlook.Modules.Mail.Views;
using Prism.Ioc;
using Prism.Modularity;
using Prism.Regions;
using PrismOutlook.Core;
using PrismOutlook.Modules.Mail.Menus;
using PrismOutlook.Modules.Mail.ViewModels;
using Prism.Mvvm;
using PrismOutlook.Services.Interfaces;
using PrismOutlook.Services;

namespace PrismOutlook.Modules.Mail
{
    public class MailModule : IModule
    {
        private readonly IRegionManager _regionManager;
        public MailModule(IRegionManager regionManager)
        {
            _regionManager = regionManager;
        }
        public void OnInitialized(IContainerProvider containerProvider)
        {
            _regionManager.RegisterViewWithRegion(RegionNames.OutlookGroupRegion, typeof(MailGroup));
        }

        public void RegisterTypes(IContainerRegistry containerRegistry)
        {
            ViewModelLocationProvider.Register<MailGroup, MailGroupViewModel>();
            containerRegistry.RegisterForNavigation<MailList, MailListViewModel>();
            containerRegistry.RegisterSingleton<IMailService, MailService>();
            containerRegistry.RegisterDialog<MessageView, MessageViewModel>();
        }
    }
}