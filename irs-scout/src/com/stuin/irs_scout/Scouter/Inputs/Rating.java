package com.stuin.irs_scout.Scouter.Inputs;

import android.content.Context;
import android.text.InputFilter;
import android.text.InputType;
import android.view.Gravity;
import android.view.KeyEvent;
import android.widget.EditText;
import android.widget.LinearLayout;
import android.widget.RatingBar;
import android.widget.TextView;
import com.stuin.irs_scout.Data.InputData;
import com.stuin.irs_scout.Data.Measure;
import com.stuin.irs_scout.R;

/**
 * Created by Stuart on 8/3/2017.
 */
public class Rating extends RatingBar implements Input {
    private InputData id;

    public Rating(Context context, InputData inputData) {
        super(context);
        id = inputData;
    }

    @Override
    public void create(LinearLayout column) {
        column.addView(part(id.task.success));

        setMax(5);
        setOnRatingBarChangeListener(actionListener);
        column.addView(this);
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
        setProgress(measure.successes);

        measure.attempts = 5;
        id.update(measure, send);
    }

    private OnRatingBarChangeListener actionListener = new OnRatingBarChangeListener() {
        @Override
        public void onRatingChanged(RatingBar ratingBar, float rating, boolean fromUser) {
            id.measure.successes = (int)(rating);

            update(id.measure, fromUser);
        }
    };

    @Override
    public InputData getData() {
        return id;
    }
}
