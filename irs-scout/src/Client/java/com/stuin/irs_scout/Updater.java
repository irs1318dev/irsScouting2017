package com.stuin.irs_scout;

import android.os.CountDownTimer;

import java.util.List;

/**
 * Created by Stuart on 2/16/2017.
 */
class Updater {
    private MatchMaker matchMaker;

    Updater(MatchMaker matchMaker) {
        this.matchMaker = matchMaker;
        countDownTimer.start();
    }

    private CountDownTimer countDownTimer = new CountDownTimer(10000,10000) {
        @Override
        public void onTick(long l) {

        }

        @Override
        public void onFinish() {
            class Status extends Request {
                @Override
                public void run(List<String> s) {
                    if(!s.get(0).equals((String.valueOf(matchMaker.match.number)))) matchMaker.newMatch();
                }
            }
            new Status().start("/tablet?status=test");
            countDownTimer.start();
        }
    };
}
