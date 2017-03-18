package com.stuin.irs_scout.Scouter.Views;

import android.content.Context;
import android.view.Gravity;
import android.widget.*;
import com.stuin.irs_scout.Data.Measure;
import com.stuin.irs_scout.Data.Task;
import com.stuin.irs_scout.MainActivity;
import com.stuin.irs_scout.R;

public class Switcher extends Label {
    private boolean miss;

    public Switcher(Context context, Task task, String position) {
        super(context, task, position);
    }

    @Override
    void create(LinearLayout column) {
        linearLayout = new LinearLayout(getContext());
        linearLayout.setGravity(Gravity.CENTER);
        column.addView(linearLayout);

        part(task.success);
        if(!task.miss.isEmpty()) {
            part(task.miss);
            if(MainActivity.position.contains("Pit")) views.get(1).setVisibility(GONE);
        }
    }

    @Override
    protected TextView part(String name) {
        //Create simple checkbox
        CheckBox checkBox = new CheckBox(getContext());
        checkBox.setText(name);
        checkBox.setTextSize(getResources().getDimension(R.dimen.text_norm));
        checkBox.setOnCheckedChangeListener(changeListener);
        views.add(checkBox);
        linearLayout.addView(checkBox);
        return checkBox;
    }

    @Override
    protected void update(Measure measure, boolean send) {
        super.update(measure, send);

        //Match checkboxes to capability
        CheckBox checkBox = (CheckBox) views.get(0);
        checkBox.setChecked(measure.successes == 1);

        if(!task.miss.isEmpty()) {
            miss = measure.attempts == measure.successes + 1;
            checkBox = (CheckBox) views.get(1);
            checkBox.setChecked(miss);
        }
    }

    private CompoundButton.OnCheckedChangeListener changeListener = new CompoundButton.OnCheckedChangeListener() {
        @Override
        public void onCheckedChanged(CompoundButton compoundButton, boolean b) {
            //Update measure by boolean
            if(views.indexOf(compoundButton) == 0) {
                if(b) {
                    measure.successes = 1;
                    if(miss) measure.attempts = 2;
                    else measure.attempts = 1;
                } else {
                    measure.successes = 0;
                    if(miss) measure.attempts = 1;
                    else measure.attempts = 0;
                }
            } else {
                if(b) measure.attempts = measure.successes + 1;
                else measure.attempts = measure.successes;
                miss = b;
            }

            update(measure, true);
        }
    };
}
