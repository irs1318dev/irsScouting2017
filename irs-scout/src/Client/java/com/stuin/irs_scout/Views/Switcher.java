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
    public void create(LinearLayout column) {
        if(task.Compacting == 0) super.create(column);

        LinearLayout linearLayout = new LinearLayout(getContext());
        column.addView(linearLayout);

        Switch switch1 = new Switch(getContext());
        switch1.setText(task.getSuccess());
        linearLayout.addView(switch1);

        if(task.getMiss() != null) {
            switch1 = new Switch(getContext());
            switch1.setText(task.getMiss());
            linearLayout.addView(switch1);
        }
    }
}
