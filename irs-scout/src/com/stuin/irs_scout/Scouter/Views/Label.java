package com.stuin.irs_scout.Scouter.Views;

import android.content.Context;
import android.view.Gravity;
import android.widget.LinearLayout;
import android.widget.TextView;
import com.stuin.irs_scout.Data.Measure;
import com.stuin.irs_scout.Data.Task;
import com.stuin.irs_scout.R;
import com.stuin.irs_scout.Scouter.Updater;

import java.util.ArrayList;
import java.util.List;

public class Label extends TextView {
    Task task;
    String position;
    LinearLayout linearLayout;
    List<TextView> views = new ArrayList<>();
    Measure measure = new Measure();
    boolean defaults = true;
    public boolean sectionLabel = false;

    public Label(Context context, Task task, String position) {
        super(context);
        this.task = task;
        this.position = position;
    }

    void create(LinearLayout linearLayout) {
        setTextSize(getResources().getDimension(R.dimen.text_norm));
        setText(task.success);
        setTextColor(getResources().getColor(R.color.colorText));
        setGravity(Gravity.CENTER);        linearLayout.addView(this);
    }

    protected TextView part(String name) {
        return new TextView(getContext());
    }

    protected void update(Measure measure, boolean send) {
        this.measure = measure;

        if(send) Updater.measures.add(measure);
    }
}
