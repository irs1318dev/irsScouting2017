package com.stuin.irs_scout.Views;

import android.content.Context;
import android.view.View;
import android.widget.Button;
import com.stuin.irs_scout.Data.Task;

/**
 * Created by Stuart on 2/11/2017.
 */
public class Counter extends Label {
    public Counter(Context context, Task task) {
        super(context, task);
    }

    @Override
    protected View part(String name) {
        Button button = new Button(getContext());
        button.setText(name + ": 0");
        linearLayout.addView(button);
        return button;
    }
}
