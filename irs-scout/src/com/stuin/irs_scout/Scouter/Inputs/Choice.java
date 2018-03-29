package com.stuin.irs_scout.Scouter.Inputs;

import android.content.Context;
import android.view.Gravity;
import android.view.View;
import android.widget.*;
import com.stuin.irs_scout.Data.InputData;
import com.stuin.irs_scout.Data.Measure;
import com.stuin.irs_scout.R;

/**
 * Created by Stuart on 8/3/2017.
 */
public class Choice extends RadioGroup implements Input {
    private InputData id;

    private String[] choices;
    private boolean locked = true;

    public Choice(Context context, InputData inputData) {
        super(context);

        id = inputData;
        choices = id.task.enums.replace('|','>').split(">");
    }

    @Override
    public void create(LinearLayout column) {
        setOrientation(LinearLayout.HORIZONTAL);
        setGravity(Gravity.CENTER);
        column.addView(this);

        for(String s : choices) part(s);
    }

    @Override
    public TextView part(String name) {
        RadioButton radioButton = new RadioButton(getContext());
        radioButton.setText(name);
        radioButton.setTextSize(getResources().getDimension(R.dimen.text_norm));
        radioButton.setOnCheckedChangeListener(successListener);
        radioButton.setOnLongClickListener(longClickListener);
        addView(radioButton);
        return radioButton;
    }

    @Override
    public void update(Measure measure, boolean send) {
        CompoundButton radioButton;
        id.update(measure, send);

        locked = true;
        for(int i = 0; i < choices.length; i++) {
            radioButton = (CompoundButton) getChildAt(i);
            radioButton.setChecked(choices[i].equals(measure.capability));
        }
        locked = false;
    }

    private RadioButton.OnCheckedChangeListener successListener = new RadioButton.OnCheckedChangeListener() {
        @Override
        public void onCheckedChanged(CompoundButton radioButton, boolean b) {
            if(b && !locked) {
                id.measure.capability = radioButton.getText().toString();

                update(id.measure, true);
            }
        }
    };

    private View.OnLongClickListener longClickListener = new OnLongClickListener() {
        @Override
        public boolean onLongClick(View view) {
            id.measure.capability = "";

            RadioButton radioButton = (RadioButton) view;
            radioButton.setChecked(false);

            update(id.measure, true);
            return true;
        }
    };

    @Override
    public InputData getData() {
        return id;
    }
}
