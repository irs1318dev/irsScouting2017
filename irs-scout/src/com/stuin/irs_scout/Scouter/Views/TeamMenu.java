package com.stuin.irs_scout.Scouter.Views;

import android.content.Context;
import android.widget.*;
import com.stuin.irs_scout.Data.Match;
import com.stuin.irs_scout.Data.Measure;
import com.stuin.irs_scout.Data.PitMatch;
import com.stuin.irs_scout.Scouter.PitMaker;
import com.stuin.irs_scout.R;

import java.util.Arrays;
import java.util.List;
import java.util.Map;

/**
 * Created by Stuart on 3/3/2017.
 */
public class TeamMenu extends Page {
    private RadioGroup list;
    private List<String> teams;
    private boolean set = false;
    public PitMaker pitMaker;

    public TeamMenu(Context context) {
        super(context, "pit");

        ScrollView scrollView = new ScrollView(getContext());
        addView(scrollView);

        list = new RadioGroup(getContext());
        list.setOrientation(VERTICAL);
        scrollView.addView(list);

        list.setOnCheckedChangeListener(new RadioGroup.OnCheckedChangeListener() {
            @Override
            public void onCheckedChanged(RadioGroup radioGroup, int i) {
                pitMaker.setTeam(teams.indexOf(((RadioButton)radioGroup.getChildAt(i - 1)).getText().toString()));
            }
        });
    }

    @Override
    public void setMeasures(Map<String, Measure> measures, Match match) {
        PitMatch pitMatch = (PitMatch) match;
        teams = Arrays.asList(pitMatch.teams);

        if(!set) {
            for(int i = 3; i < 5; i++) {
                for(String team : teams) if(team.length() == i) addTeam(team);
            }

            set = true;
        }
    }

    private void addTeam(String team) {
        RadioButton radioButton = new RadioButton(getContext());
        radioButton.setText(team);
        radioButton.setTextSize(getResources().getDimension(R.dimen.text_norm));
        list.addView(radioButton);
    }
}
