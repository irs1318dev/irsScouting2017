package com.stuin.irs_scout.Views;

import android.content.Context;
import android.view.Gravity;
import android.view.View;
import android.widget.*;
import com.stuin.irs_scout.Data.Measure;
import com.stuin.irs_scout.Data.Task;
import com.stuin.irs_scout.R;
import com.stuin.irs_scout.Updater;

/**
 * Created by Stuart on 2/16/2017.
 */
public class Multi extends Label {
    private RadioGroup radioGroup;
    private boolean miss;
    private String[] choices;

    public Multi(Context context, Task task) {
        super(context, task);

        choices = task.additions.split(">");
    }

    @Override
    void create(LinearLayout column) {
        make(column);

        radioGroup = new RadioGroup(getContext());
        radioGroup.setOrientation(LinearLayout.HORIZONTAL);
        radioGroup.setGravity(Gravity.CENTER);
        column.addView(radioGroup);

        for(String s : choices) {
            RadioButton radioButton = (RadioButton) part(s);
            radioButton.setOnCheckedChangeListener(successListener);
        }

        if(!task.miss.isEmpty()) {
            radioGroup = new RadioGroup(getContext());
            radioGroup.setOrientation(LinearLayout.HORIZONTAL);
            radioGroup.setGravity(Gravity.CENTER);
            column.addView(radioGroup);

            RadioButton radioButton = (RadioButton) part(task.success);
            radioButton.setOnCheckedChangeListener(missListener);

            radioButton = (RadioButton) part(task.miss);
            radioButton.setOnCheckedChangeListener(missListener);
        }
    }

    @Override
    protected TextView part(String name) {
        RadioButton radioButton = new RadioButton(getContext());
        radioButton.setText(name);
        radioButton.setTextSize(getResources().getDimension(R.dimen.text_norm));
        radioGroup.addView(radioButton);
        views.add(radioButton);
        return radioButton;
    }

    @Override
    protected void update(Measure measure, boolean send) {
        super.update(measure, send);

        if(measure.miss > measure.success) miss = true;

        RadioButton radioButton;

        if(!task.miss.isEmpty()) {
            radioButton = (RadioButton) views.get(views.size() - 1);
            radioButton.setChecked(miss);

            radioButton = (RadioButton) views.get(views.size() - 2);
            radioButton.setChecked(!miss);
        }

        for(int i = 0; i < choices.length; i++) {
            radioButton = (RadioButton) views.get(i);
            radioButton.setOnLongClickListener(longClickListener);
            //radioButton.setChecked(i + 1 == measure.success || i + 1 == measure.miss);
        }
    }

    private RadioButton.OnCheckedChangeListener successListener = new RadioButton.OnCheckedChangeListener() {
        @Override
        public void onCheckedChanged(CompoundButton radioButton, boolean b) {
            if(b) {
                int i = 0;
                while(radioButton != views.get(i)) i++;

                if(miss) measure.miss = i + 1;
                else measure.success = i + 1;

                update(measure, true);
            }
        }
    };

    private RadioButton.OnCheckedChangeListener missListener = new RadioButton.OnCheckedChangeListener() {
        @Override
        public void onCheckedChanged(CompoundButton radioButton, boolean b) {
            if(b) {
                miss = (radioButton == views.get(views.size() - 1));

                if(measure.success > 0 & miss) {
                    measure.miss = measure.success;
                    measure.success = 0;
                } else if(measure.miss > 0 & !miss) {
                    measure.success = measure.miss;
                    measure.miss = 0;
                }

                update(measure, true);
            }
        }
    };

    private View.OnLongClickListener longClickListener = new OnLongClickListener() {
        @Override
        public boolean onLongClick(View view) {
            measure.success = 0;

            RadioButton radioButton = (RadioButton) view;
            radioButton.setChecked(false);

            update(measure, true);
            return true;
        }
    };
}
