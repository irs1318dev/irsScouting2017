package com.stuin.irs_scout.Views;

import android.content.Context;
import android.view.Gravity;
import android.view.View;
import android.widget.LinearLayout;
import android.widget.TextView;
import com.stuin.irs_scout.Data.Measure;
import com.stuin.irs_scout.Data.Task;
import com.stuin.irs_scout.R;

import java.util.ArrayList;
import java.util.List;

public class Label extends TextView {
    Task task;
    LinearLayout linearLayout;
    List<TextView> views = new ArrayList<>();
    Measure measure = new Measure();

    public Label(Context context, Task task) {
        super(context);
        this.task = task;
    }

    void create(LinearLayout column) {
        if(task.Compacting < 1) {
            setTextSize(20);
            setText(task.Task);
            setTextColor(getResources().getColor(R.color.colorText));
            setGravity(Gravity.CENTER);
            column.addView(this);
        }

        linearLayout = new LinearLayout(getContext());
        linearLayout.setGravity(Gravity.CENTER);
        column.addView(linearLayout);

        views.add(part(task.Success));
        if(!task.Miss.isEmpty()) views.add(part(task.Miss));
        update(measure);
    }

    protected TextView part(String name) {
        return new TextView(getContext());
    }

    protected void update(Measure measure) {
        this.measure = measure;
    }
}
