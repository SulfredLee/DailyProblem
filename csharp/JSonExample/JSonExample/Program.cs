using Newtonsoft.Json;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace JSonExample
{
    class Program
    {
        public class EligibleRole
        {
            public List<string> theArray { get; set; }
        }
        static void Main(string[] args)
        {
            string json = System.IO.File.ReadAllText("ConfigFile.json");
            var eligible_role = JsonConvert.DeserializeObject<EligibleRole>(json);
            foreach (var ele in eligible_role.theArray)
            {
                Console.WriteLine(ele);
            }
        }
    }
}
