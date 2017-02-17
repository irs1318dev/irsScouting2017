package com.stuin.irs_scout.Views;

import android.content.Context;
import android.view.Gravity;
import android.view.View;
import android.widget.LinearLayout;
import android.widget.RadioButton;
import android.widget.RadioGroup;
import android.widget.TextView;
import com.stuin.irs_scout.Data.Measure;
import com.stuin.irs_scout.Data.Task;

/**
 * Created by Stuart on 2/16/2017.
 */
public class Multi extends Label {
    private RadioGroup radioGroup;
    private boolean miss;
    private String[] choices;

    public Multi(Context context, Task task) {
        super(context, task);

        choices = task.additions.split("|");
    }

    @Override
    void create(LinearLayout column) {
        make(column);

        radioGroup = new RadioGroup(getContext());
        radioGroup.setOrientation(LinearLayout.HORIZONTAL);
        radioGroup.setGravity(Gravity.CENTER);
        radioGroup.setOnCheckedChangeListener(successListener);
        linearLayout.addView(radioGroup);

        for(String s : choices) part(s);

        if(!task.miss.isEmpty()) {
            radioGroup = new RadioGroup(getContext());
            radioGroup.setOrientation(LinearLayout.HORIZONTAL);
            radioGroup.setGravity(Gravity.CENTER);
            radioGroup.setOnCheckedChangeListener(missListener);
            linearLayout.addView(radioGroup);

            part(task.success);
            part(task.miss);
        }
    }

    @Override
    protected TextView part(String name) {
        RadioButton radioButton = new RadioButton(getContext());
        radioButton.setText(name);
        radioGroup.addView(radioButton);
        views.add(radioButton);
        return radioButton;
    }

    @Override
    protected void update(Measure measure, boolean send) {
        super.update(measure, send);

        miss = (measure.miss > measure.success);

        RadioButton radioButton;

        if(!task.miss.isEmpty()) {
            radioButton = (RadioButton) views.get(views.size() - 1);
            radioButton.setChecked(miss);

            radioButton = (RadioButton) views.get(views.size() - 2);
            radioButton.setChecked(!miss);
        }

        for(int i = 0; i < choices.length; i++) {
            radioButton = (RadioButton) views.get(i);
            radioButton.setChecked(i + 1 == measure.success || i + 1 == measure.miss);
        }
    }

    private RadioGroup.OnCheckedChangeListener successListener = new RadioGroup.OnCheckedChangeListener() {
        @Override
        public void onCheckedChanged(RadioGroup radioGroup, int i) {
            if(miss) measure.miss = i + 1;
            else measure.success = i + 1;
            update(measure, true);
        }
    };

    private RadioGroup.OnCheckedChangeListener missListener = new RadioGroup.OnCheckedChangeListener() {
        @Override
        public void onCheckedChanged(RadioGroup radioGroup, int i) {
            miss = (i == 0);
            if(measure.success > 0 & miss) {
                measure.miss = measure.success;
                measure.success = 0;
            } else if(measure.miss > 0 & !miss) {
                measure.success = measure.miss;
                measure.miss = 0;
            }
            update(measure, true);
        }
    };
}
