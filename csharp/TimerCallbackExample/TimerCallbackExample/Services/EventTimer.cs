using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace TimerCallbackExample.Services
{
    class EventTimer
    {
        // need dispatcher timer to due with the Signle Threaded Apartment(STA) problem
        // STA problem is due to one want to use the backend thread to control UI things
        private System.Windows.Threading.DispatcherTimer m_testDispatcherTimer = null;
        private DateTime m_nextCallbackTime;
        private TimeSpan m_repeatPeriod;
        private EventHandler m_eventHD;

        public EventTimer(EventHandler eventHD, DateTime nextCallbackTime, TimeSpan repeatPeriod)
        {
            m_eventHD = eventHD;
            m_nextCallbackTime = nextCallbackTime;
            m_repeatPeriod = repeatPeriod;

            m_testDispatcherTimer = new System.Windows.Threading.DispatcherTimer();
            m_testDispatcherTimer.Tick += new EventHandler(OnTimerEventProxy);
            m_testDispatcherTimer.Interval = GetNextInterval();
            m_testDispatcherTimer.Start();
        }

        private TimeSpan GetNextInterval()
        {
            DateTime now = DateTime.Now;

            while (now > m_nextCallbackTime)
            {
                m_nextCallbackTime = m_nextCallbackTime.Add(m_repeatPeriod);
            }

            return m_nextCallbackTime.Subtract(now);
        }

        private void OnTimerEventProxy(object sender, EventArgs e)
        {
            m_eventHD(sender, e);
            m_testDispatcherTimer.Interval = GetNextInterval();
        }
    }
}
