package com.stuin.irs_scout.Views;

import android.content.Context;
import android.graphics.Color;
import android.util.SparseArray;
import android.view.Gravity;
import android.widget.LinearLayout;
import android.widget.TextView;
import com.stuin.irs_scout.Data.Measure;

import java.util.ArrayList;
import java.util.List;

public class Page extends LinearLayout {
    public String name;
    private LinearLayout column;
    private List<Label> labels = new ArrayList<>();

    public Page(Context context, String name) {
        //Create page
        super(context);
        this.name = name;

        //Set formatting
        setGravity(Gravity.CENTER);
        newCol();
    }

    public void add(Label objectView) {
        //Add object to column
        if(objectView.task.newpart) newCol();
        labels.add(objectView);
        objectView.create(column);
    }

    public void setMeasures(SparseArray<Measure> measures, int match, int team) {
        for(Label l : labels) {
            if(measures.get(l.task.id) != null) l.update(measures.get(l.task.id), false);
            else l.update(new Measure(l.task, match, team), false);
        }
    }

    private void newCol() {
        //Make new column
        divider();
        column = new LinearLayout(getContext());
        column.setOrientation(VERTICAL);
        addView(column);
        divider();
    }

    private void divider() {
        //Add decoration line
        TextView textView = new TextView(getContext());
        textView.setHeight(600);
        textView.setWidth(2);
        textView.setBackgroundColor(Color.LTGRAY);
        addView(textView);
    }
}
