package com.stuin.irs_scout.Scouter.Inputs;

import android.content.Context;
import android.view.Gravity;
import android.widget.LinearLayout;
import android.widget.TextView;
import com.stuin.irs_scout.Data.InputData;
import com.stuin.irs_scout.Data.Measure;
import com.stuin.irs_scout.R;

/**
 * Created by Stuart on 8/3/2017.
 */
public class Label extends TextView implements Input {
    private InputData id;

    public Label(Context context, InputData inputData) {
        super(context);
        id = inputData;
    }

    @Override
    public void create(LinearLayout column) {
        //Place in column
        setTextSize(getResources().getDimension(R.dimen.text_norm));
        setText(id.task.success);
        setTextColor(getResources().getColor(R.color.colorText));
        setGravity(Gravity.CENTER);
        column.addView(this);
    }

    @Override
    public TextView part(String name) {
        return null;
    }

    @Override
    public void update(Measure measure, boolean send) {
        id.update(measure, send);
    }

    @Override
    public InputData getData() {
        return id;
    }
}
