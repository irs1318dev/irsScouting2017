package com.stuin.irs_scout.Views;

import android.content.Context;
import android.view.View;
import android.widget.LinearLayout;
import android.widget.Switch;
import com.stuin.irs_scout.Data.Task;

public class Switcher extends Label {
    public Switcher(Context context, Task task) {
        super(context, task);
    }

    @Override
    protected View part(String name) {
        Switch switch1 = new Switch(getContext());
        switch1.setText(name);
        linearLayout.addView(switch1);
        return switch1;
    }
}
