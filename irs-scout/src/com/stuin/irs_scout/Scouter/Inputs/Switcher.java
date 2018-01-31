package com.stuin.irs_scout.Scouter.Inputs;

import android.content.Context;
import android.view.Gravity;
import android.view.View;
import android.widget.*;
import com.stuin.irs_scout.Data.InputData;
import com.stuin.irs_scout.Data.Measure;
import com.stuin.irs_scout.R;

public class Switcher extends LinearLayout implements Input {
    private InputData id;

    public Switcher(Context context, InputData inputData) {
        super(context);
        id = inputData;
    }

    @Override
    public void create(LinearLayout column) {
        part(id.task.success);
        if(!id.task.miss.isEmpty()) part(id.task.miss);

        setOrientation(HORIZONTAL);
        setGravity(Gravity.CENTER);
        column.addView(this);
    }

    @Override
    public TextView part(String name) {
        CompoundButton button = new CheckBox(getContext());
        button.setTextSize(getResources().getDimension(R.dimen.text_norm));
        button.setText(name);
        //button.setTextColor(getResources().getColor(R.color.colorText));
        button.setGravity(Gravity.CENTER);
        button.setOnClickListener(clickListener);
        addView(button);
        return button;
    }

    @Override
    public void update(Measure measure, boolean send) {
        CompoundButton sw = (CompoundButton) getChildAt(0);
        sw.setChecked(measure.successes > 0);

        if(!id.task.miss.isEmpty()) {
            sw = (CompoundButton) getChildAt(1);
            sw.setChecked(measure.attempts - measure.successes > 0);
        }

        id.update(measure, send);
    }

    private OnClickListener clickListener = new OnClickListener() {
        @Override
        public void onClick(View v) {
            CompoundButton sw = (CompoundButton) getChildAt(0);
            id.measure.successes = (sw.isChecked()) ? 1 : 0;

            if(!id.task.miss.isEmpty()) {
                sw = (CompoundButton) getChildAt(1);
                id.measure.attempts = ((sw.isChecked()) ? 1 : 0) + id.measure.successes;
            }

            update(id.measure, true);
        }
    };

    @Override
    public InputData getData() {
        return id;
    }
}
