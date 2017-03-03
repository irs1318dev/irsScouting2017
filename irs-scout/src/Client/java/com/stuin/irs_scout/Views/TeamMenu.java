package com.stuin.irs_scout.Views;

import android.content.Context;
import android.view.View;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.Spinner;
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
    private Spinner spinner;
    public PitMaker pitMaker;

    public TeamMenu(Context context) {
        super(context, "setup");
        spinner = new Spinner(context);
        spinner.setOnItemSelectedListener(selectedListener);
        addView(spinner);
    }

    @Override
    public void setMeasures(Map<String, Measure> measures, Match match) {
        PitMatch pitMatch = (PitMatch) match;

        ArrayAdapter<String> dataAdapter = new ArrayAdapter<>(getContext(), android.R.layout.simple_spinner_item, Arrays.asList(pitMatch.teams));
        dataAdapter.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item);
        spinner.setAdapter(dataAdapter);
    }

    private Spinner.OnItemSelectedListener selectedListener = new Spinner.OnItemSelectedListener() {
        @Override
        public void onItemSelected(AdapterView<?> adapterView, View view, int i, long l) {
            pitMaker.setTeam(i);
        }

        @Override
        public void onNothingSelected(AdapterView<?> adapterView) {

        }
    };
}
