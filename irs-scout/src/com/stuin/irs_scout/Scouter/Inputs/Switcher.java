package com.stuin.irs_scout.Scouter.Inputs;

import android.content.Context;
import android.view.Gravity;
import android.widget.LinearLayout;
import android.widget.Switch;
import android.widget.TextView;
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
        column.addView(this);
    }

    @Override
    public TextView part(String name) {
        Switch sw = new Switch(getContext());
        sw.setTextSize(getResources().getDimension(R.dimen.text_norm));
        sw.setText(id.task.success);
        //sw.setTextColor(getResources().getColor(R.color.colorText));
        sw.setGravity(Gravity.CENTER);
        addView(sw);
        return sw;
    }

    @Override
    public void update(Measure measure, boolean send) {
        Switch sw = (Switch) getChildAt(0);
        sw.setChecked(measure.successes > 0);

        if(!id.task.miss.isEmpty()) {
            sw = (Switch) getChildAt(1);
            sw.setChecked(measure.attempts - measure.successes > 0);
        }

        id.update(measure, send);
    }

    @Override
    public InputData getData() {
        return id;
    }
}
