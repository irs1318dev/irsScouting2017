package com.stuin.irs_scout;

import android.content.Context;
import android.graphics.Color;
import android.view.Gravity;
import android.widget.LinearLayout;
import android.widget.TextView;
import com.stuin.irs_scout.Views.Label;

import java.util.ArrayList;
import java.util.List;

class FormPage extends LinearLayout {
    String name;
    private LinearLayout column;

    FormPage(Context context, String name) {
        //Create Page
        super(context);
        this.name = name;

        //Set formatting
        setGravity(Gravity.CENTER);
        newCol();
    }

    void add(Label objectView) {
        objectView.create(column);
    }

    private void newCol() {
        TextView textView = new TextView(getContext());
        textView.setHeight(600);
        textView.setWidth(2);
        textView.setBackgroundColor(Color.LTGRAY);
        addView(textView);

        column = new LinearLayout(getContext());
        column.setOrientation(VERTICAL);
        addView(column);
    }
}
