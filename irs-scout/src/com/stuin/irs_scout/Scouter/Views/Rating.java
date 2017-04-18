package com.stuin.irs_scout.Scouter.Views;

import android.content.Context;
import android.widget.LinearLayout;
import android.widget.RatingBar;
import com.stuin.irs_scout.Data.Task;

/**
 * Created by Stuart on 4/18/2017.
 */
public class Rating extends Label {
    RatingBar ratingBar;

    public Rating(Context context, Task task, String position) {
        super(context, task, position);
    }

    @Override
    void create(LinearLayout linearLayout) {
        ratingBar = new RatingBar(getContext());
        ratingBar.setNumStars(3);
        linearLayout.addView(ratingBar);
    }
}
