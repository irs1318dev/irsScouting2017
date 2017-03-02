package com.stuin.irs_scout.Views;

import android.content.Context;
import android.text.InputFilter;
import android.text.InputType;
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
        EditText editText = new EditText(getContext());
        editText.setInputType(InputType.TYPE_CLASS_NUMBER);
        editText.setTextSize(getResources().getDimension(R.dimen.text_norm));
        editText.setWidth(200);
        editText.setOnEditorActionListener(actionListener);

        InputFilter[] filters = new InputFilter[1];
        filters[0] = new InputFilter.LengthFilter(2);
        editText.setFilters(filters);

        TextView textView = new TextView(getContext());
        textView.setText("%");
        textView.setTextSize(getResources().getDimension(R.dimen.text_norm));

        linearLayout.addView(editText);
        linearLayout.addView(textView);
        views.add(editText);
        return editText;
    }

    @Override
    protected void update(Measure measure, boolean send) {
        super.update(measure, send);

        String s = measure.success + "";
        if(s.equals("0")) s = "";

        EditText editText = (EditText) views.get(0);
        editText.setText(s);
    }

    private EditText.OnEditorActionListener actionListener = new OnEditorActionListener() {
        @Override
        public boolean onEditorAction(TextView textView, int i, KeyEvent keyEvent) {
            update(measure, true);
            return false;
        }
    };
}
