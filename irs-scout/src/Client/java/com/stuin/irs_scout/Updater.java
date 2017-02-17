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
    public static Stack<Measure> allMeasures = new Stack<>();

    private Queue<Measure> measures;
    private MatchMaker matchMaker;
    private RadioButton status;

    Updater(MatchMaker matchMaker, View view) {
        this.matchMaker = matchMaker;
        status = (RadioButton) view;
        countDownTimer.start();
    }

    private CountDownTimer countDownTimer = new CountDownTimer(10000,1000) {
        @Override
        public void onTick(long l) {
            status.setChecked(MainActivity.error);
            send();
        }

        @Override
        public void onFinish() {
            class Status extends Request {
                @Override
                public void run(List<String> s) {
                    if(!s.get(0).equals((String.valueOf(matchMaker.match.number)))) matchMaker.newMatch();
                }
            }
            new Status().start("/tablet?status=" + status.getText().toString());
            countDownTimer.start();
        }
    };

    void setStatus() {
        countDownTimer.cancel();
        countDownTimer.onFinish();
    }

    private void send() {
        if(!MainActivity.error & allMeasures.size() > 0) {
            clear();
            Measure measure = measures.peek();

            String s = "/matchteamtask?match=" + measure.match + "&team=" + measure.team + "&task=" + measure.taskId;
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
                    send();
                }
            }
            new Remove(measure).start(s);
        }
    }

    private void clear() {
        measures = new ArrayDeque<>();
        Collection<Integer> tasks = new ArrayList<>();

        class Link {
            int task;
            int team;
            String page;

            Link(int task, int team, String page) {
                this.task = task;
                this.team = team;
                this.page = page;
            }
        }

        while(allMeasures.size() > 0) {
            Measure m = allMeasures.pop();
            Link link = new Link(m.taskId, m.team, m.page);
            if(!tasks.contains(link.hashCode())) {
                tasks.add(link.hashCode());
                measures.add(m);
            }
        }
    }
}
