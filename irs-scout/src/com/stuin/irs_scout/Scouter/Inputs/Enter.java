package com.stuin.irs_scout.Scouter.Inputs;

import android.content.Context;
import android.text.InputFilter;
import android.text.InputType;
import android.view.Gravity;
import android.view.KeyEvent;
import android.widget.EditText;
import android.widget.LinearLayout;
import android.widget.TextView;
import com.stuin.irs_scout.Data.InputData;
import com.stuin.irs_scout.Data.Measure;
import com.stuin.irs_scout.R;

/**
 * Created by Stuart on 8/3/2017.
 */
public class Enter extends EditText implements Input {
    private InputData id;

    public Enter(Context context, InputData inputData) {
        super(context);
        id = inputData;
    }

    @Override
    public void create(LinearLayout column) {
        column.addView(part(id.task.success));

        setInputType(InputType.TYPE_CLASS_NUMBER);
        setTextSize(getResources().getDimension(R.dimen.text_norm));
        setWidth(200);
        setGravity(Gravity.CENTER);
        setOnEditorActionListener(actionListener);

        InputFilter[] filters = new InputFilter[1];
        filters[0] = new InputFilter.LengthFilter(4);
        setFilters(filters);
    }

    @Override
    public TextView part(String name) {
        TextView textView = new TextView(getContext());
        textView.setText(name);
        textView.setGravity(Gravity.CENTER);
        textView.setTextSize(getResources().getDimension(R.dimen.text_norm));
        return textView;
    }

    @Override
    public void update(Measure measure, boolean send) {
        measure.attempts = 100;
        id.update(measure, send);

        String s = measure.successes + "%";
        setText(s);
    }

    private OnEditorActionListener actionListener = new OnEditorActionListener() {
        @Override
        public boolean onEditorAction(TextView textView, int i, KeyEvent keyEvent) {
            id.measure.successes = Integer.valueOf(textView.getText().toString().replace("%", ""));
            if(id.measure.successes > 100) id.measure.successes = 100;

            update(id.measure, true);
            return false;
        }
    };

    @Override
    public InputData getData() {
        return id;
    }
}
