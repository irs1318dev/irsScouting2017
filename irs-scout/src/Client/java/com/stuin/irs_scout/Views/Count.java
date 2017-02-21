package com.stuin.irs_scout.Views;

import android.content.Context;
import android.os.CountDownTimer;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;
import com.stuin.irs_scout.Data.Measure;
import com.stuin.irs_scout.Data.Task;
import com.stuin.irs_scout.R;

/**
 * Created by Stuart on 2/11/2017.
 */
public class Count extends Label {
    private CountDownTimer countDownTimer;
    private boolean drop;
    private boolean missing;
    private int max = 20;

    public Count(Context context, Task task) {
        super(context, task);
    }

    @Override
    protected TextView part(String name) {
        //Simple counter button
        Button button = new Button(getContext());
        button.setText(name);
        button.setTextSize(getResources().getDimension(R.dimen.text_norm));
        button.setOnClickListener(clickListener);
        button.setOnLongClickListener(longClickListener);
        linearLayout.addView(button);
        return button;
    }

    @Override
    protected void update(Measure measure, boolean send) {
        super.update(measure, send);

        //Set button text
        views.get(0).setText(task.successname + ": " + measure.success);
        if(!task.missname.isEmpty()) views.get(1).setText(task.missname + ": " + measure.miss);
    }

    private View.OnClickListener clickListener = new OnClickListener() {
        @Override
        public void onClick(View view) {
            //Add to values
            if(!drop) {
                if(views.indexOf((TextView) view) == 0) {
                    if(measure.success < max) measure.success++;
                } else if(measure.miss < max) measure.miss++;
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
            if(view == views.get(0)) {
                missing = false;
                if(measure.success > 0) measure.success--;
            }
            else {
                missing = true;
                if(measure.miss > 0) measure.miss--;
            }

            drop = true;
            countDownTimer = new CountDownTimer(400, 10) {
                @Override
                public void onTick(long l) {
                }

                @Override
                public void onFinish() {
                    if(drop) {
                        if(!missing) {
                            if(measure.success > 0) measure.success--;
                        } else if(measure.miss > 0) measure.miss--;
                        countDownTimer.start();
                    }
                    update(measure,false);
                }
            }.start();

            update(measure, false);
            return false;
        }
    };
}
