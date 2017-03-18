package com.stuin.irs_scout.Views;

import android.content.Context;
import android.view.View;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.ListView;
import com.stuin.irs_scout.Data.Match;
import com.stuin.irs_scout.Data.Measure;
import com.stuin.irs_scout.Data.PitMatch;
import com.stuin.irs_scout.PitMaker;

import java.util.Arrays;
import java.util.Map;

/**
 * Created by Stuart on 3/3/2017.
 */
public class TeamMenu extends Page {
    private ListView list;
    private boolean set = false;
    public PitMaker pitMaker;

    public TeamMenu(Context context) {
        super(context, "pit");
        list = new ListView(context);
		
        addView(list);
    }

    @Override
    public void setMeasures(Map<String, Measure> measures, Match match) {
        PitMatch pitMatch = (PitMatch) match;

        if(!set) {
            ArrayAdapter<String> dataAdapter = new ArrayAdapter<>(getContext(), android.R.layout.simple_spinner_item, Arrays.asList(pitMatch.teams));
            dataAdapter.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item);
            list.setAdapter(dataAdapter);
            set = true;
        }
    }

    
}
