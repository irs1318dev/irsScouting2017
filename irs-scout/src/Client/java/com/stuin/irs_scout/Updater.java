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
    static public List<Measure> measures = new ArrayList<>();

    private MatchMaker matchMaker;
    private RadioButton status;

    Updater(MatchMaker matchMaker, View view) {
        this.matchMaker = matchMaker;
        status = (RadioButton) view;
    }

    private CountDownTimer countDownTimer = new CountDownTimer(10000,100) {
        @Override
        public void onTick(long l) {
            status.setChecked(MainActivity.error);
            send();
        }

        @Override
        public void onFinish() {
            String s = "/tablet?status=" + status.getText().toString().replace(" ", "");
            class Status extends Request {
                @Override
                public void run(List<String> s) {
                    if(!s.get(0).equals(String.valueOf(matchMaker.match.number))) matchMaker.newMatch();
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
        if(!MainActivity.error) {
            for(Measure measure : measures) {
                String s = "/matchteamtask?match=" + measure.match + "&team=" + measure.team + "&task=" + measure.task;
                if(measure.success != 0) s += "&success=" + measure.success;
                if(measure.miss != 0) s += "&miss=" + measure.miss;

                class Remove extends Request {
                    private Measure measure;

                    private Remove(Measure measure) {
                        this.measure = measure;
                    }

                    @Override
                    public void run(List<String> s) {
                        measures.remove(measure);
                    }
                }
                new Remove(measure).start(s);
            }
        }
    }
}
