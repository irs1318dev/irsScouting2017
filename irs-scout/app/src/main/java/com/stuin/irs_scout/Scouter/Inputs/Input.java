package com.stuin.irs_scout.Scouter.Inputs;

import android.widget.LinearLayout;
import android.widget.TextView;
import com.stuin.irs_scout.Data.InputData;
import com.stuin.irs_scout.Data.Measure;

/**
 * Created by Stuart on 8/3/2017.
 */
public interface Input {
    void create(LinearLayout column);
    TextView part(String name);
    void update(Measure measure, boolean send);
    InputData getData();

}
