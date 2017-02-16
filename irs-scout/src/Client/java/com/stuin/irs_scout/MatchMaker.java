package com.stuin.irs_scout;

import android.util.SparseArray;
import android.view.View;
import android.widget.TextView;
import com.google.gson.Gson;
import com.stuin.irs_scout.Data.Match;
import com.stuin.irs_scout.Data.Measure;
import com.stuin.irs_scout.Views.Page;

import java.util.ArrayList;
import java.util.List;

/**
 * Created by Stuart on 2/14/2017.
 */
class MatchMaker {
    private Match match = new Match();
    private List<Measure> data;
    private List<Page> pages;
    private TextView status;

    MatchMaker(List<Page> pages, View view) {
        this.pages = pages;
        status = (TextView) view;
        newMatch();
    }

    void newMatch() {
        class Data extends Next {
            @Override
            public void run(List<String> s) {
                match = new Gson().fromJson(s.get(0), Match.class);
                if(!MainActivity.position.contains(match.alliance)) match = new Gson().fromJson(s.get(1), Match.class);
                status.setText("Match: " + match.number + " Team " + MainActivity.position + ": " + getTeam());
                data = new ArrayList<>();

                class Set extends Next {
                    @Override
                    public void run(List<String> measures) {
                        Gson gson = new Gson();
                        for(String s : measures) data.add(gson.fromJson(s, Measure.class));
                        setMatch();
                    }
                }
                new Request("/matchteam?team=" + getTeam(),new Set());
            }
        }
        new Request("/match", new Data());
    }

    private void setMatch() {
        for(Page p : pages) {
            SparseArray<Measure> pageData = new SparseArray<>();
            for(Measure m : data) if(m.page.equals(p.name)) pageData.put(m.taskId, m);
            p.setMeasures(pageData, match.number, getTeam());
        }
    }

    int getTeam() {
        String position = MainActivity.position;
        switch(position.charAt(position.length() - 1)) {
            case '1':
                return match.team1;
            case '2':
                return match.team2;
            case '3':
                return match.team3;
        }
        return 0;
    }
}
