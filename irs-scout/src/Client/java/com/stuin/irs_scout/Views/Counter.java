package com.stuin.irs_scout.Views;

import android.content.Context;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;
import com.stuin.irs_scout.Data.Measure;
import com.stuin.irs_scout.Data.Task;
import com.stuin.irs_scout.R;

/**
 * Created by Stuart on 2/11/2017.
 */
public class Counter extends Label {
    public Counter(Context context, Task task) {
        super(context, task);
    }

    @Override
    protected TextView part(String name) {
        //Simple counter button
        Button button = new Button(getContext());
        button.setText(name);
        button.setTextSize(getResources().getDimension(R.dimen.text_norm));
        button.setOnClickListener(clickListener);
        linearLayout.addView(button);
        return button;
    }

    @Override
    protected void update(Measure measure, boolean send) {
        super.update(measure, send);

        //Set button text
        views.get(0).setText(task.success + ": " + measure.success);
        if(!task.miss.isEmpty()) views.get(1).setText(task.miss + ": " + measure.miss);
    }

    private View.OnClickListener clickListener = new OnClickListener() {
        @Override
        public void onClick(View view) {
            //Add to values
            if(views.indexOf((TextView) view) == 0) measure.success++;
            else measure.miss++;

            update(measure, true);
        }
    };
}
