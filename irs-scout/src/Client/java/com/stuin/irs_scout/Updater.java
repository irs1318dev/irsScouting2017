package com.stuin.irs_scout;

import android.os.CountDownTimer;
import android.view.View;
import android.widget.RadioButton;
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

    Updater(MatchMaker matchMaker, View view) {
        this.matchMaker = matchMaker;
        status = (RadioButton) view;
    }

    private CountDownTimer countDownTimer = new CountDownTimer(50000,100) {
        @Override
        public void onTick(long l) {
            status.setChecked(MainActivity.error);
            if(MainActivity.error) last = "";
            send();
        }

        @Override
        public void onFinish() {
            String s = "/tablet?status=" + status.getText().toString().replace(" ", "");
            class Status extends Request {
                @Override
                public void run(List<String> s) {
                    if(!s.get(0).equals(String.valueOf(matchMaker.match.match))) matchMaker.newMatch();
                }
            }
            new Status().start(s);
            countDownTimer.start();
        }
    };

    void setStatus() {
        countDownTimer.cancel();
        countDownTimer.onFinish();
    }

    private void send() {
        try {
            for(Measure measure : measures) {
                String s = "/matchteamtask?match=" + measure.match + "&team=" + measure.team + "&task=" + measure.task + "&phase=" + measure.phase;
                if(!measure.capability.isEmpty()) s += "&capability=" + measure.capability;
                if(measure.success != 0) s += "&success=" + measure.success;
                if(measure.attempt != 0) s += "&attempt=" + measure.attempt;

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
            }
            while(!finished.isEmpty()) measures.remove(finished.poll());
        } catch(ConcurrentModificationException e) {
            //just keep moving
        }
    }
}
