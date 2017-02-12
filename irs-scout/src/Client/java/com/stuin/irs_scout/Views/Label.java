package com.stuin.irs_scout.Views;

import android.content.Context;
import android.view.Gravity;
import android.view.View;
import android.widget.LinearLayout;
import android.widget.TextView;
import com.stuin.irs_scout.Data.Measure;
import com.stuin.irs_scout.Data.Task;
import com.stuin.irs_scout.R;

public class Label extends TextView {
    protected Task task;
    public Measure measure;

    public Label(Context context, Task task) {
        super(context);
        this.task = task;
    }

    public void create(LinearLayout column) {
        setTextSize(20);
        setText(task.getName());
        setTextColor(getResources().getColor(R.color.colorText));
        setGravity(Gravity.CENTER);
        column.addView(this);
    }

    View.OnClickListener clickListener = new View.OnClickListener() {
        @Override
        public void onClick(View view) {

        }
    };
}
