using Prism.Commands;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace PrismOutlook.Core
{
    public interface IApplicationCommands
    {
        CompositeCommand NavigateCommand { get; }
    }
    public class ApplicationCommands : IApplicationCommands
    {

        public CompositeCommand NavigateCommand { get; } = new CompositeCommand();
    }
}
