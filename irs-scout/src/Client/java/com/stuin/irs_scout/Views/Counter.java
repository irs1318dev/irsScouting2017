package com.stuin.irs_scout.Views;

import android.content.Context;
import android.widget.LinearLayout;
import com.stuin.irs_scout.Data.Task;

/**
 * Created by Stuart on 2/11/2017.
 */
public class Counter extends Label {
    public Counter(Context context, Task task) {
        super(context, task);
    }

    @Override
    public void create(LinearLayout column) {
        if(task.Compacting == 0) super.create(column);

        LinearLayout linearLayout = new LinearLayout(getContext());
        column.addView(linearLayout);
    }
}
