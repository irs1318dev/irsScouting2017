package com.stuin.irs_scout.Views;

import android.content.Context;
import android.view.View;
import android.widget.CheckBox;
import android.widget.LinearLayout;
import android.widget.Switch;
import com.stuin.irs_scout.Data.Task;

public class Switcher extends Label {
    public Switcher(Context context, Task task) {
        super(context, task);
    }

    @Override
    protected View part(String name) {
        CheckBox checkBox = new CheckBox(getContext());
        checkBox.setText(name);
        checkBox.setTextSize(18);
        linearLayout.addView(checkBox);
        return checkBox;
    }
}
