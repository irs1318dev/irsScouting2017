package com.stuin.irs_scout;

import android.view.View;
import android.widget.TextView;
import com.google.gson.Gson;
import com.stuin.irs_scout.Data.Match;
import com.stuin.irs_scout.Data.Measure;
import com.stuin.irs_scout.Views.Page;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

/**
 * Created by Stuart on 2/14/2017.
 */
class MatchMaker {
    Match match = new Match();

    private PageManager pageManager;
    private List<Measure> data;
    private List<Page> pages;
    private TextView status;

    MatchMaker(PageManager pageManager, View view) {
        this.pages = pageManager.pages;
        this.pageManager = pageManager;
        status = (TextView) view;
        newMatch();
    }

    void newMatch() {
        class Data extends Request {
            @Override
            public void run(List<String> s) {
                match = new Gson().fromJson(s.get(0), Match.class);
                if(MainActivity.position.charAt(0) != match.alliance.charAt(0)) match = new Gson().fromJson(s.get(1), Match.class);

                String title = "Match: " + match.number;
                if(!MainActivity.position.contains("Fuel")) title += " Team: " + match.getTeam(MainActivity.position);
                status.setText(title);
                data = new ArrayList<>();

                class Set extends Request {
                    @Override
                    public void run(List<String> measures) {
                        Gson gson = new Gson();
                        for(String s : measures) if(!s.contains("end")) data.add(gson.fromJson(s, Measure.class));
                        setMatch();
                    }
                }
                new Set().start("/matchteamtasks?team=" + match.getTeam(MainActivity.position));
            }
        }
        new Data().start("/matchteams");
    }

    private void setMatch() {
        pageManager.reset();
        for(Page p : pages) {
            Map<String, Measure> pageData = new HashMap<>();
            for(Measure m : data) if(m.phase.equals(p.name)) pageData.put(m.task, m);
            p.setMeasures(pageData, match);
        }
    }
}
