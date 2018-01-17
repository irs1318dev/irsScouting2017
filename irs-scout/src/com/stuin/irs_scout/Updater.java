package com.stuin.irs_scout;

import android.os.AsyncTask;
import android.os.CountDownTimer;
import android.view.View;
import android.widget.RadioButton;
import com.stuin.cleanvisuals.Request;
import com.stuin.irs_scout.Data.Measure;
import com.stuin.irs_scout.MatchMaker;

import java.util.*;

/**
 * Created by Stuart on 2/16/2017.
 */
public class Updater {
    private static List<Measure> measures = new ArrayList<>();
    private MatchMaker matchMaker;
    private Queue<Measure> finished = new ArrayDeque<>();
    private RadioButton status;
    private String last = "";
    private String ip = "";
    private int cutoff = 0;

    public Updater(MatchMaker matchMaker, View view) {
        this.matchMaker = matchMaker;
        status = (RadioButton) view;
    }

    public static void addMeasure(Measure measure) {
        measures.add(measure);
        MatchMaker.update(measure);
    }

    //Main timer
    private CountDownTimer countDownTimer = new CountDownTimer(10000,100) {
        @Override
        public void onTick(long l) {
            //Check for error
            status.setChecked(Request.error);
            if(Request.error) last = "";

            //Data slowdown
            if(cutoff < 30) AsyncTask.execute(send);
            cutoff--;
        }

        @Override
        public void onFinish() {
            //Get current page and match
            String s = "/tablet?status=" + status.getText().toString().replace(" ", "") + ip;
            ip = "";
            class Status extends Request {
                @Override
                public void run(List<String> s) {
                    //Check if match changed
                    if(!s.get(0).equals(matchMaker.match.match) && !matchMaker.match.match.equals("na")) matchMaker.newMatch();
                }
            }
            new Status().start(s);
            countDownTimer.start();
        }
    };

    public void setStatus() {
        //Manually send status update
        ip = "&ip=" + Request.address;
        countDownTimer.cancel();
        countDownTimer.onFinish();
    }

    private Runnable send = new Runnable() {
        @Override
        public void run() {
            //Get first measure
            if(measures.size() > 0) {
                Measure measure = measures.get(0);

                //Make string of data
                String s = "/matchteamtask?match=" + measure.match + "&team=" + measure.team + "&task=" + measure.task + "&phase=" + measure.phase;
                if(!measure.capability.isEmpty() && !measure.capability.equals("0")) s += "&capability=" + measure.capability;
                if(measure.successes != 0) s += "&success=" + measure.successes;
                if(measure.attempts != 0) s += "&attempt=" + measure.attempts;

                //Check sending and start next
                if(!s.equals(last)) {
                    class Remove extends Request {
                        private Measure measure;

                        private Remove(Measure measure) {
                            this.measure = measure;
                        }

                        //List measure as done and confirmed
                        @Override
                        public void run(List<String> s) {
                            finished.add(measure);
                        }
                    }
                    new Remove(measure).start(s);
                } else measures.remove(measure);

                last = s;
                cutoff += 2;

                while(!finished.isEmpty()) measures.remove(finished.poll());
            }
        }
    };
}
