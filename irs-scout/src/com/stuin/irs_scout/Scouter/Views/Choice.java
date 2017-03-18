package com.stuin.irs_scout.Scouter.Views;

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
    private String[] choices;
    private boolean locked = true;

    public Choice(Context context, Task task, String position) {
        super(context, task, position);
        defaults = false;

        choices = task.enums.replace('|','>').split(">");
    }

    @Override
    void create(LinearLayout column) {
        radioGroup = new RadioGroup(getContext());
        radioGroup.setOrientation(LinearLayout.HORIZONTAL);
        radioGroup.setGravity(Gravity.CENTER);
        column.addView(radioGroup);

        for(String s : choices) part(s);
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

        CompoundButton radioButton;
        locked = true;

        for(int i = 0; i < choices.length; i++) {
            radioButton = (CompoundButton) views.get(i);
            radioButton.setChecked(choices[i].toLowerCase().equals(measure.capability));
        }

        locked = false;
    }

    private RadioButton.OnCheckedChangeListener successListener = new RadioButton.OnCheckedChangeListener() {
        @Override
        public void onCheckedChanged(CompoundButton radioButton, boolean b) {
            if(b && !locked) {
                measure.capability = radioButton.getText().toString().toLowerCase();

                update(measure, true);
            }
        }
    };

    private View.OnLongClickListener longClickListener = new OnLongClickListener() {
        @Override
        public boolean onLongClick(View view) {
            measure.capability = "";

            RadioButton radioButton = (RadioButton) view;
            radioButton.setChecked(false);

            update(measure, true);
            return true;
        }
    };
}
