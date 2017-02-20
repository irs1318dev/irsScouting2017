package com.stuin.irs_scout.Views;

import android.content.Context;
import android.view.Gravity;
import android.view.View;
import android.widget.*;
import com.stuin.irs_scout.Data.Measure;
import com.stuin.irs_scout.Data.Task;
import com.stuin.irs_scout.R;

/**
 * Created by Stuart on 2/16/2017.
 */
public class Choice extends Label {
    private RadioGroup radioGroup;
    private boolean miss;
    private String[] choices;

    public Choice(Context context, Task task) {
        super(context, task);
        defaults = false;

        choices = task.additions.split(">");
    }

    @Override
    void create(LinearLayout column) {
        make(column);

        radioGroup = new RadioGroup(getContext());
        radioGroup.setOrientation(LinearLayout.HORIZONTAL);
        radioGroup.setGravity(Gravity.CENTER);
        column.addView(radioGroup);

        for(String s : choices) part(s);

        if(!task.miss.isEmpty()) {
            Switch switch1 = new Switch(getContext());
            switch1.setText(task.success);
            switch1.setTextSize(getResources().getDimension(R.dimen.text_norm));
            switch1.setOnCheckedChangeListener(missListener);
            views.add(switch1);
            column.addView(switch1);
        }
    }

    @Override
    protected TextView part(String name) {
        RadioButton radioButton = new RadioButton(getContext());
        radioButton.setText(name);
        radioButton.setTextSize(getResources().getDimension(R.dimen.text_norm));
        radioButton.setOnCheckedChangeListener(successListener);
        radioButton.setOnLongClickListener(longClickListener);
        radioGroup.addView(radioButton);
        views.add(radioButton);
        return radioButton;
    }

    @Override
    protected void update(Measure measure, boolean send) {
        super.update(measure, send);

        if(measure.miss > measure.success) miss = true;

        CompoundButton radioButton;

        if(!task.miss.isEmpty()) {
            radioButton = (Switch) views.get(views.size() - 1);
            radioButton.setChecked(miss);
        }

        for(int i = 0; i < choices.length; i++) {
            radioButton = (CompoundButton) views.get(i);
            if(i + 1 == measure.success || i + 1 == measure.miss) {
                radioButton.setChecked(true);
            }
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

    private Switch.OnCheckedChangeListener missListener = new Switch.OnCheckedChangeListener() {
        @Override
        public void onCheckedChanged(CompoundButton radioButton, boolean b) {
            miss = b;

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
