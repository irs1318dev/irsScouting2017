package com.stuin.irs_scout.Views;

import android.content.Context;
import android.view.Gravity;
import android.widget.LinearLayout;
import android.widget.TextView;
import com.stuin.irs_scout.Data.Measure;
import com.stuin.irs_scout.Data.Task;
import com.stuin.irs_scout.R;
import com.stuin.irs_scout.Updater;

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
        //Make label
        if(task.compacting < 1) {
            setTextSize(getResources().getDimension(R.dimen.text_norm));
            setText(task.task);
            setTextColor(getResources().getColor(R.color.colorText));
            setGravity(Gravity.CENTER);
            column.addView(this);
        }

        //Make new row
        linearLayout = new LinearLayout(getContext());
        linearLayout.setGravity(Gravity.CENTER);
        column.addView(linearLayout);

        //Create two objects
        views.add(part(task.success));
        if(!task.miss.isEmpty()) views.add(part(task.miss));
        update(measure, false);
    }

    protected TextView part(String name) {
        return new TextView(getContext());
    }

    protected void update(Measure measure, boolean send) {
        this.measure = measure;

        if(send) Updater.allMeasures.push(measure);
    }
}
