package util;

import java.util.Calendar;
import java.util.Timer;
import java.util.TimerTask;
import java.util.concurrent.TimeUnit;

public class EventTimer {
    private TimerTask task;
    private Calendar nextCallbackTime;
    private int repeatPeriodSec;
    private Timer eventTimer = new Timer();

    public EventTimer(TimerTask task, Calendar nextCallbackTime, long repeatPeriodSec) {
        this.task = task;
        this.nextCallbackTime = (Calendar)nextCallbackTime.clone();
        this.repeatPeriodSec = (int)repeatPeriodSec;

        if (this.task != null) {
            ValidateCallbackTime();
            eventTimer.schedule(this.task, this.nextCallbackTime.getTime(), TimeUnit.MILLISECONDS.convert(repeatPeriodSec, TimeUnit.SECONDS));
        }
    }

    private void ValidateCallbackTime() {
        Calendar now = Calendar.getInstance();

        while (this.nextCallbackTime.compareTo(now) <= 0) {
            this.nextCallbackTime.add(Calendar.SECOND, this.repeatPeriodSec);
        }
    }
}
