using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace DelayDemoForms
{
    enum Scheduler
    {
        EveryMinutes,
        EveryHour,
        EveryHalfDay,
        EveryDay,
        EveryWeek,
        EveryMonth,
        EveryYear,
    }
    public partial class Form1 : Form
    {
        public Form1()
        {
            InitializeComponent();
            numHours.Value = DateTime.Now.Hour;
            numMins.Value = DateTime.Now.Minute;
        }
        CancellationTokenSource m_ctSource;

        /// <summary>
        /// Setting up time for running the code
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        private void startBtn_Click(object sender, EventArgs e)
        {

            //retrieve hour and minute from the form
            int hour = (int)numHours.Value;
            int minutes = (int)numMins.Value;

            //create next date which we need in order to run the code
            var dateNow = DateTime.Now;
            var date = new DateTime(dateNow.Year, dateNow.Month, dateNow.Day, hour, minutes, 0);

            listBox1.Items.Add("**********Scheduler has been started!*****");

            //get nex date the code need to run
            var nextDateValue=getNextDate(date,getScheduler());

            runCodeAt(nextDateValue, getScheduler());

        }

      
        /// <summary>
        /// Schedule the time the need to be call
        /// </summary>
        /// <param name="date"></param>
        /// <param name="scheduler"></param>
        private void runCodeAt(DateTime date,Scheduler scheduler )
        {
            m_ctSource = new CancellationTokenSource();

            var dateNow = DateTime.Now;
            TimeSpan ts;
            if (date > dateNow)
                ts = date - dateNow;
            else
            {
                date = getNextDate(date, scheduler);
                ts = date - dateNow;
            }

            //enable the progressbar
            prepareControlForStart();

           

            //waits certan time and run the code, in meantime you can cancel the task at anty time
            Task.Delay(ts).ContinueWith((x) => 
                {
                    //run the code at the time
                     methodToCall(date);

                     //setup call next day
                     runCodeAt(getNextDate(date, scheduler), scheduler);

                },m_ctSource.Token);
        }

        /// <summary>
        /// prepare the controls for starting scheduler
        /// </summary>
        private void prepareControlForStart()
        {
            progressBar1.Enabled = true;
            progressBar1.Style = ProgressBarStyle.Marquee;
            button1.Enabled = false;
            groupBox1.Enabled = false;
            groupBox2.Enabled = false;
            button3.Enabled = true;
        }
        /// <summary>
        /// prepare the controls for canceling the scheduler
        /// </summary>
        private void prepareControlsForCancel()
        {
            m_ctSource = null;
            progressBar1.Enabled = false;
            progressBar1.Style = ProgressBarStyle.Blocks;
            groupBox1.Enabled = true;
            groupBox2.Enabled = true;
            button3.Enabled = false;
            button1.Enabled = true;
        }
        /// <summary>
        /// returns next date the code to be run
        /// </summary>
        /// <param name="date"></param>
        /// <param name="scheduler"></param>
        /// <returns></returns>
        private DateTime getNextDate(DateTime date, Scheduler scheduler)
        {
            switch (scheduler)
            {
                case Scheduler.EveryMinutes:
                    return date.AddMinutes(1);
                case Scheduler.EveryHour:
                    return date.AddHours(1);
                case Scheduler.EveryHalfDay:
                    return date.AddHours(12);
                case Scheduler.EveryDay:
                    return date.AddDays(1);
                case Scheduler.EveryWeek:
                    return date.AddDays(7);
                case Scheduler.EveryMonth:
                    return date.AddMonths(1);
                case Scheduler.EveryYear:
                    return date.AddYears(1);
                default:
                    throw new Exception("Invalid scheduler");
            }

        }

        /// <summary>
        /// method to be called after period of time
        /// </summary>
        /// <param name="time"></param>
        /// <returns></returns>
        private void methodToCall(DateTime time)
        {
            //setup next call
            var nextTimeToCall = getNextDate(time,getScheduler());

            this.BeginInvoke((Action)(() =>
            {
                var strText = string.Format("Method is called at {0}. The next call will be at {1}", time, nextTimeToCall);
                listBox1.Items.Add(strText);
                //MessageBox.Show(strText);
            }));

          
           
        }

        /// <summary>
        /// based on the selected radion box returns the scheduler enum
        /// </summary>
        /// <returns></returns>
        private Scheduler getScheduler()
        {
            if(radioButton1.Checked)
                return Scheduler.EveryMinutes;
            if (radioButton2.Checked)
                return Scheduler.EveryHour;
            if (radioButton3.Checked)
                return Scheduler.EveryHalfDay;
            if (radioButton4.Checked)
                return Scheduler.EveryDay;
            if (radioButton5.Checked)
                return Scheduler.EveryWeek;
            if (radioButton6.Checked)
                return Scheduler.EveryMonth;
            if (radioButton7.Checked)
                return Scheduler.EveryYear;

            //default
            return Scheduler.EveryMinutes;
        }

        /// <summary>
        /// canceling the sheduler
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        private void cancelBtn_Click(object sender, EventArgs e)
        {
            if (m_ctSource != null)
            {
                m_ctSource.Cancel();
                prepareControlsForCancel();

                listBox1.Items.Add("**********Scheduler has topped!*****");
            }  
        }

      
        /// <summary>
        /// Exits the app
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        private void exitBtn_Click(object sender, EventArgs e)
        {
            if (progressBar1.Enabled)
                MessageBox.Show("Scheduler is running. Cancel the scheduler first then close the application!");
            else
                this.Close();
        }

    }
}
