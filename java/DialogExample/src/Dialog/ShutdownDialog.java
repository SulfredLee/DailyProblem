package Dialog;

import javax.swing.*;
import java.awt.*;
import java.awt.event.MouseAdapter;
import java.awt.event.MouseEvent;
import java.util.Timer;
import java.util.TimerTask;
import java.util.concurrent.CountDownLatch;
import java.util.concurrent.TimeUnit;

public class ShutdownDialog extends JDialog {
    private int userResponse = 0;
    private JButton shutdownBtn = new JButton();
    private JButton postponeBtn = new JButton();
    private JLabel headMsg = new JLabel();
    private CountdownHelper countHelper;

    public ShutdownDialog(int countForSec) {
        super(null, java.awt.Dialog.ModalityType.TOOLKIT_MODAL);

        setupUI();
        addListeners();
        toFront();
        countHelper = new CountdownHelper(this, countForSec);
        Thread thread = new Thread(countHelper);
        thread.start();
        setVisible(true);
    }

    public int GetUserResponse() {
        return userResponse;
    }

    public JLabel GetHeadMsg() {
        return this.headMsg;
    }

    public synchronized void SetUserResponse(int response) {
        this.userResponse = response;
    }

    private void setupUI() {
        // setup UI members
        String title = "Shutdown Dialog";
        String displayMessage = "Needed to Shutdown";
        String shutdownLabel = "Shutdown";
        String postponeLabel = "Postpone 5 minutes";

        // set title
        this.setTitle(title);

        // handle head message
        this.headMsg.setText(displayMessage);
        this.headMsg.setFont(new Font(headMsg.getFont().getFontName(), Font.BOLD, 38));
        this.headMsg.setHorizontalAlignment(JLabel.CENTER);

        // handle response buttons
        this.shutdownBtn.setText(shutdownLabel);
        this.shutdownBtn.setFont(new Font(this.shutdownBtn.getFont().getFontName(), Font.PLAIN, 20));
        this.postponeBtn.setText(postponeLabel);
        this.postponeBtn.setFont(new Font(this.postponeBtn.getFont().getFontName(), Font.PLAIN, 20));

        JPanel buttonPanel = new JPanel();
        buttonPanel.setLayout(new GridLayout(0, 2));
        buttonPanel.add(shutdownBtn);
        buttonPanel.add(postponeBtn);

        // add to dialog
        add(this.headMsg, BorderLayout.PAGE_START);
        add(buttonPanel, BorderLayout.PAGE_END);

        setDefaultCloseOperation(DO_NOTHING_ON_CLOSE);
        setSize(520, 200);
        setResizable(false);
        setLocationRelativeTo(null);
    }

    private void addListeners() {
        // shutdown button
        shutdownBtn.addMouseListener(new MouseAdapter() {
                @Override
                public void mousePressed(MouseEvent e) {
                    // when right click
                    if (e.getButton() == MouseEvent.BUTTON1) {
                        SetUserResponse(1);
                        countHelper.DoStop();
                        dispose();
                    }
                }
            });
        // postpone button
        postponeBtn.addMouseListener(new MouseAdapter() {
                @Override
                public void mousePressed(MouseEvent e) {
                    // when right click
                    if (e.getButton() == MouseEvent.BUTTON1) {
                        SetUserResponse(0);
                        countHelper.DoStop();
                        dispose();
                    }
                }
            });
    }

    public class CountdownHelper implements Runnable {
        private boolean doStop = false;
        private int countForSec = 10;
        private ShutdownDialog shutdownDialog;

        public CountdownHelper(ShutdownDialog dialog, int countForSec) {
            this.shutdownDialog = dialog;
            this.countForSec = countForSec;
        }

        public synchronized void DoStop() {
            this.doStop = true;
        }

        private synchronized boolean KeepRunning() {
            return this.doStop == false;
        }

        @Override
        public void run() {
            int fastCount = 0;
            int totalFastCount = 10; // fast count is used to split 1 second to pieces
            int fastCountSleepMSec = 1000 / totalFastCount;

            if (this.shutdownDialog == null) return; // should not go to this line

            while (KeepRunning() && this.countForSec >= 0) {
                if (fastCount == 0) {
                    fastCount = totalFastCount;
                    this.shutdownDialog.GetHeadMsg().setText("Shutdown After: " + Integer.toString(this.countForSec) + " second");
                    this.countForSec = this.countForSec - 1;
                }
                fastCount = fastCount - 1;

                try {
                    // do not let the thread sleep too long so that kill thread earilier
                    Thread.sleep(fastCountSleepMSec);
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
            }
            if (this.countForSec < 0) { // if timeout
                this.shutdownDialog.SetUserResponse(1);
                this.shutdownDialog.dispose();
            }
        }
    }

}
