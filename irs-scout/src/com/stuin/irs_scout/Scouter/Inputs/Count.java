package com.stuin.irs_scout.Scouter.Inputs;

import android.content.Context;
import android.view.Gravity;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.GridLayout;
import android.widget.LinearLayout;
import android.widget.TextView;
import com.stuin.irs_scout.Data.InputData;
import com.stuin.irs_scout.Data.Measure;
import com.stuin.irs_scout.R;

/**
 * Created by Stuart on 8/3/2017.
 */
public class Count extends LinearLayout implements Input {
    private InputData id;
    private int miss = -1;
    private String tens = "+10";
    private int max = 40;
    private View repeatView;

    public Count(Context context, InputData inputData) {
        super(context);
        id = inputData;
    }

    @Override
    public void create(LinearLayout column) {
        //Create success and miss buttons
        part(id.task.success + ": ");
        if(!id.task.miss.isEmpty()) {
            miss = getChildCount();
            part(id.task.miss + ": ");
        }

        setOrientation(LinearLayout.HORIZONTAL);
        setGravity(Gravity.CENTER);
        //setColumnCount(2);
        //((GridLayout.LayoutParams) getLayoutParams()).setGravity(Gravity.CENTER);
        column.addView(this);
    }

    @Override
    public TextView part(String name) {
        //Create full button
        Button button = new Button(getContext());
        button.setText(name);
        button.setGravity(Gravity.CENTER);
        button.setTextSize(getResources().getDimension(R.dimen.text_norm));
        button.setOnClickListener(clickListener);
        button.setOnLongClickListener(longClickListener);
        addView(button);

        //Create secondary button
        if(name.contains("*"))
            part(tens);

        return button;
    }

    @Override
    public void update(Measure measure, boolean send) {
        //Set button text
        ((Button) getChildAt(0)).setText(id.task.success + ": " + measure.successes);
        if(miss != -1)
            ((Button) getChildAt(miss)).setText(id.task.success + ": " + (measure.attempts - measure.successes));

        id.update(measure, send);
    }

    private OnClickListener clickListener = new OnClickListener() {
        @Override
        public void onClick(View v) {
            int change = 1;
            if(((TextView) v).getText().equals(tens))
                change = 10;

            if(id.measure.attempts + change < max) {
                if (v == getChildAt(0) || v == getChildAt(miss - 1)) {
                    id.measure.successes += change;
                    id.measure.attempts += change;
                } else
                    id.measure.attempts += change;

                update(id.measure, true);
            }
        }
    };

    private OnLongClickListener longClickListener = new OnLongClickListener() {
        @Override
        public boolean onLongClick(View v) {
            int change = 1;
            if(((TextView) v).getText().equals(tens))
                change = 10;

            if(v == getChildAt(0) || v == getChildAt(miss - 1)) {
                if(id.measure.successes >= change) {
                    id.measure.successes -= change;
                    id.measure.attempts -= change;
                } else {
                    id.measure.attempts -= id.measure.successes;
                    id.measure.successes = 0;
                }
            } else {
                if (id.measure.attempts - id.measure.successes >= change)
                    id.measure.attempts -= change;
                else
                    id.measure.attempts = id.measure.successes;
            }

            //Set repeater
            repeatView = v;
            postDelayed(repeatTimer, 600);

            update(id.measure, true);
            return true;
        }
    };

    private Runnable repeatTimer = new Runnable() {
        @Override
        public void run() {
            if(repeatView.isPressed()) {
                longClickListener.onLongClick(repeatView);
            }
        }
    };

    @Override
    public InputData getData() {
        return id;
    }
}
