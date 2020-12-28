using Prism.Ioc;
using Prism.Regions;
using System;
using System.Collections.Generic;
using System.Collections.Specialized;
using System.Linq;
using System.Reflection;
using System.Text;
using System.Threading.Tasks;
using System.Windows;

namespace PrismOutlook.Core.Regions
{
    public class DependentViewRegionBehavior : RegionBehavior
    {
        public const string BehaviorKey = "DependentViewRegionBehavior";
        private readonly IContainerExtension _container;

        Dictionary<object, List<DependentViewInfo>> _dependentViewCache = new Dictionary<object, List<DependentViewInfo>>();

        public DependentViewRegionBehavior(IContainerExtension container)
        {
            _container = container;
        }
        protected override void OnAttach()
        {
            Region.ActiveViews.CollectionChanged += ActiveViews_CollectionChanged;
        }

        private void ActiveViews_CollectionChanged(object sender, NotifyCollectionChangedEventArgs e)
        {
            if (e.Action == NotifyCollectionChangedAction.Add)
            {
                foreach (var newView in e.NewItems)
                {
                    var dependentViews = new List<DependentViewInfo>();
                    // check if view already has dependents
                    if (_dependentViewCache.ContainsKey(newView))
                    {
                        // if it dos use those
                        dependentViews = _dependentViewCache[newView];
                    }
                    else
                    {
                        // if not, create them
                        // get the attributes
                        var atts = GetCustomAttributes<DependentViewAttribute>(newView.GetType());

                        foreach (var att in atts)
                        {
                            var info = CreateDependentViewInfo(att);

                            if (info.View is ISupportDataContext infoDC && newView is ISupportDataContext viewDC)
                            {
                                infoDC.DataContext = viewDC.DataContext;
                            }
                            dependentViews.Add(info);
                        }

                        _dependentViewCache.Add(newView, dependentViews);
                    }

                    // inject
                    dependentViews.ForEach(item => Region.RegionManager.Regions[item.Region].Add(item.View));
                }
                
                // find the region, then inject the view into the region
            }
            else if (e.Action == NotifyCollectionChangedAction.Remove)
            {
                foreach (var oldView in e.OldItems)
                {
                    if (_dependentViewCache.ContainsKey(oldView))
                    {
                        var dependentView = _dependentViewCache[oldView];
                        dependentView.ForEach(item => Region.RegionManager.Regions[item.Region].Remove(item.View));

                        // if being perm removed, remove from cache
                        if (!ShouldKeepAlive(oldView))
                            _dependentViewCache.Remove(oldView);
                    }
                }
            }
        }

        private bool ShouldKeepAlive(object oldView)
        {
            var regionLifetime = GetViewOrDataContextLifeTime(oldView);
            if (regionLifetime != null)
                return regionLifetime.KeepAlive;

            return true;
        }
        IRegionMemberLifetime GetViewOrDataContextLifeTime(object view)
        {
            if (view is IRegionMemberLifetime regionLifeTime)
                return regionLifeTime;

            if (view is FrameworkElement fe)
                return fe.DataContext as IRegionMemberLifetime;

            return null;
        }

        DependentViewInfo CreateDependentViewInfo(DependentViewAttribute attribute)
        {
            var info = new DependentViewInfo();
            info.Region = attribute.Region;
            // create the view instance
            info.View = _container.Resolve(attribute.Type);
            return info;
        }
        private static IEnumerable<T> GetCustomAttributes<T>(Type type)
        {
            return type.GetCustomAttributes(typeof(T), true).OfType<T>();
        }
    }
}
