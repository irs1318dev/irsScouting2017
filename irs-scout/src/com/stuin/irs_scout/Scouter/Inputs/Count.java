package com.stuin.irs_scout.Scouter.Inputs;

import android.content.Context;
import android.widget.GridLayout;
import android.widget.LinearLayout;
import android.widget.TextView;
import com.stuin.irs_scout.Data.InputData;
import com.stuin.irs_scout.Data.Measure;

/**
 * Created by Stuart on 8/3/2017.
 */
public class Count extends GridLayout implements Input {
    private InputData id;

    public Count(Context context, InputData inputData) {
        super(context);
        id = inputData;
    }

    @Override
    public void create(LinearLayout column) {

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
