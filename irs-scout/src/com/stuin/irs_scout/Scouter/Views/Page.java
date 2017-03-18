package com.stuin.irs_scout.Scouter.Views;

import android.content.Context;
import android.graphics.Color;
import android.view.Gravity;
import android.widget.LinearLayout;
import android.widget.TextView;
import com.stuin.cleanvisuals.Slider;
import com.stuin.cleanvisuals.SliderSync;
import com.stuin.irs_scout.Data.Match;
import com.stuin.irs_scout.Data.Measure;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;

public class Page extends LinearLayout {
    public String name;
    public SliderSync sliderSync;

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

    public void link(Page page, Slider.Endings endings) {
        sliderSync = new SliderSync(this, page);
        sliderSync.setup(true, 2000, -2000, 500);
        sliderSync.endings(endings);
    }

    public void add(Label objectView) {
        //Add object to column
        labels.add(objectView);
        objectView.create(column);
    }

    public void setMeasures(Map<String, Measure> measures, Match match) {
        for(Label l : labels) {
            if(l.sectionLabel && l.task.success.contains("Team")) l.setText(match.getTeam(l.position));

            String key = l.task.task + ':' + match.getTeam(l.position);
            if(measures.get(key) != null) l.update(measures.get(key), false);
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
