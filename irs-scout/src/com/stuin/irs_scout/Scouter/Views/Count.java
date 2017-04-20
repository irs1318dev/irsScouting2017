package com.stuin.irs_scout.Scouter.Views;

import android.content.Context;
import android.os.CountDownTimer;
import android.view.Gravity;
import android.view.View;
import android.widget.Button;
import android.widget.LinearLayout;
import android.widget.TextView;
import com.stuin.irs_scout.Data.Measure;
import com.stuin.irs_scout.Data.Task;
import com.stuin.irs_scout.MainActivity;
import com.stuin.irs_scout.R;

/**
 * Created by Stuart on 2/11/2017.
 */
public class Count extends Label {
    private boolean drop;
    private boolean missing;
    private int large = 0;
    private int miss = -1;
    private int max = 200;

    public Count(Context context, Task task, String position) {
        super(context, task, position);
        if(!task.miss.isEmpty()) miss = 1;

        if(task.success.contains("+")) large = 10;

        if(large > 0) {
            max = 300;
            if(miss != -1) miss = 2;
        }
    }
 
    @Override
    void create(LinearLayout column) {
        linearLayout = new LinearLayout(getContext());
        linearLayout.setOrientation(LinearLayout.HORIZONTAL);
        linearLayout.setGravity(Gravity.CENTER);
        column.addView(linearLayout);

        part(task.success);
        if(large > 0) part("+" + large);

        if(miss != -1) {
            if(large > 0) {
                linearLayout = new LinearLayout(getContext());
                linearLayout.setOrientation(LinearLayout.HORIZONTAL);
                linearLayout.setGravity(Gravity.CENTER);
                column.addView(linearLayout);
            }

            part(task.miss);
            if(large > 0) part("+" + large);
        }

    }


    @Override
    protected TextView part(String name) {
        //Simple counter button
        Button button = new Button(getContext());
        button.setText(name);
        button.setTextSize(getResources().getDimension(R.dimen.text_norm));
        button.setOnClickListener(clickListener);
        button.setOnLongClickListener(longClickListener);
        button.setGravity(Gravity.CENTER);
        views.add(button);
        linearLayout.addView(button);
        return button;
    }

    @Override
    protected void update(Measure measure, boolean send) {
        super.update(measure, send);

        //Set button text
        views.get(0).setText(task.success + ": " + measure.successes);
        if(miss != -1) views.get(miss).setText(task.miss + ": " + (measure.attempts - measure.successes));
    }

    private View.OnClickListener clickListener = new OnClickListener() {
        @Override
        public void onClick(View view) {
            //Add to values
            if(!drop) {
                if(view == views.get(0)) {
                    if(measure.successes < max) {
                        measure.successes++;
                        measure.attempts++;
                    }
                } else if(miss != -1 && view == views.get(miss)) {
                    if(measure.attempts - measure.successes < max) measure.attempts++;
                } else if(large > 0 && view == views.get(1)) {
                    if(measure.successes + large - 1 < max) {
                        measure.successes += large;
                        measure.attempts += large;
                    }
                } else if(miss != -1 && large > 0 && view == views.get(3)) {
                    if(measure.attempts - measure.successes + large - 1 < max) measure.attempts += large;
                }
            } else {
                countDownTimer.cancel();
                drop = false;
            }

            update(measure, true);
        }
    };

    private View.OnLongClickListener longClickListener = new OnLongClickListener() {
        @Override
        public boolean onLongClick(View view) {
            boolean start = true;

            if(view == views.get(0)) {
                missing = false;
                if(measure.successes > 0) {
                    measure.successes--;
                    measure.attempts--;
                }
            } else if(large > 0 && view == views.get(1)) {
                int old = measure.successes;
                measure.successes -= large;
                if(measure.successes < 0) measure.successes = 0;
                measure.attempts -= (old - measure.successes);
                start = false;
            } else if(miss != -1 && view == views.get(miss)) {
                missing = true;
                if(measure.attempts > 0) measure.attempts--;
            } else if(miss != -1 && large > 0 && view == views.get(3)) {
                measure.attempts -= large;
                if(measure.attempts < 0) measure.attempts = 0;
                start = false;
            }

            drop = true;
            if(start) countDownTimer.start();

            update(measure, false);
            return false;
        }
    };

    private CountDownTimer countDownTimer = new CountDownTimer(400, 10) {
        @Override
        public void onTick(long l) {
        }

        @Override
        public void onFinish() {
            if(drop) {
                if(!missing) {
                    if(measure.successes > 0) {
                        measure.successes--;
                        measure.attempts--;
                    }
                } else if(measure.attempts - measure.successes > 0) measure.attempts--;
                countDownTimer.start();
            }
            update(measure,false);
        }
    };
}
