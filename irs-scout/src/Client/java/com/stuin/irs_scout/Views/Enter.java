package com.stuin.irs_scout.Views;

import android.content.Context;
import android.text.InputType;
import android.view.KeyEvent;
import android.view.View;
import android.widget.EditText;
import android.widget.TextView;
import com.stuin.irs_scout.Data.Measure;
import com.stuin.irs_scout.Data.Task;
import com.stuin.irs_scout.R;

/**
 * Created by Stuart on 2/17/2017.
 */
public class Enter extends Label{
    public Enter(Context context, Task task) {
        super(context, task);
    }

    @Override
    protected TextView part(String name) {
        EditText editText = new EditText(getContext());
        editText.setInputType(InputType.TYPE_CLASS_NUMBER);
        editText.setTextSize(getResources().getDimension(R.dimen.text_norm));
        editText.setWidth(200);
        editText.setOnEditorActionListener(actionListener);
        linearLayout.addView(editText);
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
            if(textView.getText().length() > 0 && textView.getText().length() < 4) {
                measure.success = Integer.valueOf(textView.getText().toString());
            } else measure.success = 0;

            update(measure, true);
            return false;
        }
    };
}
