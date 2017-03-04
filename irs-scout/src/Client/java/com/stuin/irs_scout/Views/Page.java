package com.stuin.irs_scout.Views;

import android.content.Context;
import android.graphics.Color;
import android.view.Gravity;
import android.widget.LinearLayout;
import android.widget.TextView;
import com.stuin.irs_scout.Data.Match;
import com.stuin.irs_scout.Data.Measure;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;

public class Page extends LinearLayout {
    public String name;
    private LinearLayout column;
    private List<Label> labels = new ArrayList<>();

    public Page(Context context, String name) {
        //Create phase
        super(context);
        this.name = name;

        //Set formatting
        setGravity(Gravity.CENTER);
        newCol();
    }

    public void add(Label objectView) {
        //Add object to column
        labels.add(objectView);
        objectView.create(column);
    }

    public void setMeasures(Map<String, Measure> measures, Match match) {
        for(Label l : labels) {
            if(l.sectionLabel && l.task.success.contains("Team")) l.setText(match.getTeam(l.position));

            if(measures.get(l.task.success) != null) {
                Measure measure = measures.get(l.task.success);
                if(match.getTeam(l.position).equals(measure.team)) l.update(measure, false);
            }
            else l.update(new Measure(l.task, match, l.position, name), false);
        }
    }

    public void newCol() {
        //Make new column
        divider();
        column = new LinearLayout(getContext());
        column.setOrientation(VERTICAL);
        column.setGravity(Gravity.CENTER);
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
