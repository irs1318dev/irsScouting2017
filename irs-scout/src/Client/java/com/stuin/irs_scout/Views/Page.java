package com.stuin.irs_scout.Views;

import android.content.Context;
import android.graphics.Color;
import android.view.Gravity;
import android.widget.LinearLayout;
import android.widget.TextView;

public class Page extends LinearLayout {
    public String name;
    private LinearLayout column;

    public Page(Context context, String name) {
        //Create Page
        super(context);
        this.name = name;

        //Set formatting
        setGravity(Gravity.CENTER);
        newCol();
    }

    public void add(Label objectView) {
        if(objectView.task.NewPart) newCol();
        objectView.create(column);
    }

    private void newCol() {
        divider();
        column = new LinearLayout(getContext());
        column.setOrientation(VERTICAL);
        addView(column);
        divider();
    }

    private void divider() {
        TextView textView = new TextView(getContext());
        textView.setHeight(600);
        textView.setWidth(2);
        textView.setBackgroundColor(Color.LTGRAY);
        addView(textView);
    }
}
