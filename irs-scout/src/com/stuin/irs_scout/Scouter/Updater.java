package com.stuin.irs_scout.Scouter;

import android.os.AsyncTask;
import android.os.CountDownTimer;
import android.view.View;
import android.widget.RadioButton;
import com.stuin.cleanvisuals.Request;
import com.stuin.irs_scout.Data.Measure;

import java.util.*;

/**
 * Created by Stuart on 2/16/2017.
 */
public class Updater {
    public static List<Measure> measures = new ArrayList<>();

    private MatchMaker matchMaker;
    private Queue<Measure> finished = new ArrayDeque<>();
    private RadioButton status;
    private String last = "";
    private String ip = "";
    private int cutoff = 0;

    Updater(MatchMaker matchMaker, View view) {
        this.matchMaker = matchMaker;
        status = (RadioButton) view;
    }

    private CountDownTimer countDownTimer = new CountDownTimer(10000,100) {
        @Override
        public void onTick(long l) {
            status.setChecked(Request.error);
            if(Request.error) last = "";
            if(cutoff < 30) AsyncTask.execute(send);
            cutoff--;
        }

        @Override
        public void onFinish() {
            String s = "/tablet?status=" + status.getText().toString().replace(" ", "") + ip;
            ip = "";
            class Status extends Request {
                @Override
                public void run(List<String> s) {
                    if(!s.get(0).equals(matchMaker.match.match) && !matchMaker.match.match.equals("na")) matchMaker.newMatch();
                }
            }
            new Status().start(s);
            countDownTimer.start();
        }
    };

    public void setStatus() {
        ip = "&ip=" + Request.address;
        countDownTimer.cancel();
        countDownTimer.onFinish();
    }

    private Runnable send = new Runnable() {
        @Override
        public void run() {
            try {
                for(Measure measure : measures) {
                    String s = "/matchteamtask?match=" + measure.match + "&team=" + measure.team + "&task=" + measure.task + "&phase=" + measure.phase;
                    if(!measure.capability.isEmpty() && !measure.capability.equals("0")) s += "&capability=" + measure.capability;
                    if(measure.successes != 0) s += "&success=" + measure.successes;
                    if(measure.attempts != 0) s += "&attempt=" + measure.attempts;

                    matchMaker.update(measure);

                    if(!s.equals(last)) {
                        class Remove extends Request {
                            private Measure measure;

                            private Remove(Measure measure) {
                                this.measure = measure;
                            }

                            @Override
                            public void run(List<String> s) {
                                finished.add(measure);
                            }
                        }
                        new Remove(measure).start(s);
                    } else measures.remove(measure);
                    last = s;
                    cutoff += 2;
                }
                while(!finished.isEmpty()) measures.remove(finished.poll());
            } catch(ConcurrentModificationException e) {
                //just keep moving
            }
        }
    };
}
