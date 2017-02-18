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
public class Multi extends Label {
    private String[] choices;

    public Multi(Context context, Task task) {
        super(context, task);
        defaults = false;

        choices = task.additions.split(">");
    }

    @Override
    protected TextView part(String name) {
        Switch compoundButton = new Switch(getContext());
        compoundButton.setText(name);
        compoundButton.setTextSize(getResources().getDimension(R.dimen.text_norm));
        compoundButton.setOnCheckedChangeListener(successListener);
        linearLayout.addView(compoundButton);
        views.add(compoundButton);
        return compoundButton;
    }

    @Override
    protected void update(Measure measure, boolean send) {
        super.update(measure, send);


    }

    private Switch.OnCheckedChangeListener successListener = new Switch.OnCheckedChangeListener() {
        @Override
        public void onCheckedChanged(CompoundButton compoundButton, boolean b) {
            String aByte = "";
            for(View v : views) {
                compoundButton = (CompoundButton) v;
                if(compoundButton.isChecked()) aByte += '1';
                else aByte += '0';
            }

            measure.success = Byte.decode(aByte).intValue();
            update(measure,true);
        }
    };
}
