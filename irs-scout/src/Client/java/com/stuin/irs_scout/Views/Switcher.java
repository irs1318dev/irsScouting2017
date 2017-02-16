package com.stuin.irs_scout.Views;

import android.content.Context;
import android.widget.*;
import com.stuin.irs_scout.Data.Measure;
import com.stuin.irs_scout.Data.Task;
import com.stuin.irs_scout.R;

public class Switcher extends Label {
    public Switcher(Context context, Task task) {
        super(context, task);
    }

    @Override
    protected TextView part(String name) {
        //Create simple checkbox
        CheckBox checkBox = new CheckBox(getContext());
        checkBox.setText(name);
        checkBox.setTextSize(getResources().getDimension(R.dimen.text_norm));
        checkBox.setOnCheckedChangeListener(changeListener);
        linearLayout.addView(checkBox);
        return checkBox;
    }

    @Override
    protected void update(Measure measure) {
        super.update(measure);

        //Match checkboxes to value
        CheckBox checkBox = (CheckBox) views.get(0);
        checkBox.setChecked(measure.success == 1);

        if(!task.miss.isEmpty()) {
            checkBox = (CheckBox) views.get(1);
            checkBox.setChecked(measure.miss == 1);
        }
    }

    private CompoundButton.OnCheckedChangeListener changeListener = new CompoundButton.OnCheckedChangeListener() {
        @Override
        public void onCheckedChanged(CompoundButton compoundButton, boolean b) {
            //Update measure by boolean
            if(views.indexOf(compoundButton) == 0) {
                if(b) measure.success = 1;
                else measure.success = 0;
            } else {
                if(b) measure.miss = 1;
                else measure.miss = 0;
            }
            update(measure);
        }
    };
}
