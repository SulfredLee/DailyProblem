package main;

import Dialog.ShutdownDialog;
import util.EventTimer;

import javax.swing.*;
import java.awt.event.MouseAdapter;
import java.awt.event.MouseEvent;
import java.util.Calendar;
import java.util.Timer;
import java.util.TimerTask;
import java.util.concurrent.CountDownLatch;
import java.util.concurrent.TimeUnit;
// import org.assertj.swing.edt.GuiActionRunner;

public class DialogExample {
    static private Timer postponeTimer = new Timer();
    // static private Timer dailyShutdownTimer = new Timer();
    static private EventTimer dailyShutdownTimer;

    public static void main(String[] args) {
        JFrame f = new JFrame();//creating instance of JFrame

        JButton b = new JButton("click");//creating instance of JButton
        b.setBounds(130,100,100, 40);//x axis, y axis, width, height

        f.add(b);//adding button in JFrame

        f.setSize(400,500);//400 width and 500 height
        f.setLayout(null);//using no layout managers
        f.setVisible(true);//making the frame visible

        // click button
        b.addMouseListener(new MouseAdapter() {
                @Override
                public void mousePressed(MouseEvent e) {
                    // when right click
                    if (e.getButton() == MouseEvent.BUTTON1) {
                        System.out.println("Hello world");
                    }
                }
            });
        // Object[] options = {
        //     "Shutdown"
        //     , "Postpone 5 Minutes"
        // };
        // int n = JOptionPane.showOptionDialog(f
        //                                      , "Shutdown is Needed!"
        //                                      , "Shutdown Dialog"
        //                                      , JOptionPane.YES_NO_OPTION
        //                                      , JOptionPane.WARNING_MESSAGE
        //                                      , null
        //                                      , options
        //                                      , options[0]);
        // System.out.format("Response: %d", n);
        // ShutdownDialog dd = GuiActionRunner.execute(() -> new ShutdownDialog());

        // Example to use countdownlatch
        // postponeTimer.schedule(new PostponeTask(), postponeTimeSec * 1000);
        // timer.schedule(new PostponeTask(this), postponeTimeSec * 1000);
        // System.out.format("Before threadID: %s\n", Thread.currentThread().getName());
        // try {
        //     cdl.await(10, TimeUnit.SECONDS);
        // } catch (InterruptedException ex) {
        //     System.out.println("Fail to on pause");
        // }
        // System.out.format("After threadID: %s\n", Thread.currentThread().getName());
        // ShowDialog();
        System.out.println("Hello world");
        // ProcessShutdownDialog();
        class ShutdownTask extends TimerTask {
            public void run() {
                ProcessShutdownDialog();
            }
        }
        Calendar today = Calendar.getInstance();
        // today.set(Calendar.HOUR_OF_DAY, 2);
        today.set(Calendar.MINUTE, 28);
        today.set(Calendar.SECOND, 0);
        System.out.println(today.toString());
        // dailyShutdownTimer.schedule(new ShutdownTask(), today.getTime(), TimeUnit.MILLISECONDS.convert(1, TimeUnit.MINUTES));

        dailyShutdownTimer = new EventTimer(new ShutdownTask(), today, TimeUnit.SECONDS.convert(1, TimeUnit.DAYS));
    }

    public static void ProcessShutdownDialog() {
        class PostponeTask extends TimerTask {
            public void run() {
                ProcessShutdownDialog();
            }
        }

        ShutdownDialog dd = new ShutdownDialog(10);
        if (dd.GetUserResponse() == 1) {
            // shutdown
            System.exit(0);
            // f.dispose();
        } else {
            postponeTimer.schedule(new PostponeTask(), TimeUnit.MILLISECONDS.convert(10, TimeUnit.SECONDS));
        }

    }

    public static void foo(int xx) {
        int y = xx + 1;
    }
}
