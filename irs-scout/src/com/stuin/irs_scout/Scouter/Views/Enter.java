package com.stuin.irs_scout.Scouter.Views;

import android.content.Context;
import android.text.InputFilter;
import android.text.InputType;
import android.view.Gravity;
import android.view.KeyEvent;
import android.widget.EditText;
import android.widget.LinearLayout;
import android.widget.TextView;
import com.stuin.irs_scout.Data.Measure;
import com.stuin.irs_scout.Data.Task;
import com.stuin.irs_scout.R;

/**
 * Created by Stuart on 2/17/2017.
 */
public class Enter extends Label{
    public Enter(Context context, Task task, String position) {
        super(context, task, position);
    }

    @Override
    void create(LinearLayout linearLayout) {
        this.linearLayout = linearLayout;
        part(task.success);
    }


    @Override
    protected TextView part(String name) {
        TextView textView = new TextView(getContext());
        textView.setText(task.success);
        textView.setGravity(Gravity.CENTER);
        textView.setTextSize(getResources().getDimension(R.dimen.text_norm));
        linearLayout.addView(textView);

        EditText editText = new EditText(getContext());
        editText.setInputType(InputType.TYPE_CLASS_NUMBER);
        editText.setTextSize(getResources().getDimension(R.dimen.text_norm));
        editText.setWidth(200);
        editText.setGravity(Gravity.CENTER);
        editText.setOnEditorActionListener(actionListener);
        linearLayout.addView(editText);

        InputFilter[] filters = new InputFilter[1];
        filters[0] = new InputFilter.LengthFilter(4);
        editText.setFilters(filters);

        views.add(editText);
        return editText;
    }

    @Override
    protected void update(Measure measure, boolean send) {
        super.update(measure, send);
        measure.attempts = 100;

        String s = measure.successes + "%";

        EditText editText = (EditText) views.get(0);
        editText.setText(s);
    }

    private EditText.OnEditorActionListener actionListener = new OnEditorActionListener() {
        @Override
        public boolean onEditorAction(TextView textView, int i, KeyEvent keyEvent) {
            measure.successes = Integer.valueOf(textView.getText().toString().replace("%", ""));
            if(measure.successes > 100) measure.successes = 100;

            update(measure, true);
            return false;
        }
    };
}
