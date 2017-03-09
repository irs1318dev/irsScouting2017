package com.stuin.irs_scout;

import android.view.View;
import com.google.gson.Gson;
import com.stuin.irs_scout.Data.Measure;
import com.stuin.irs_scout.Data.PitMatch;

import java.util.ArrayList;
import java.util.List;

/**
 * Created by Stuart on 3/3/2017.
 */
public class PitMaker extends MatchMaker {
    private PitMatch pitMatch;
    private List<List<Measure>> allData;

    PitMaker(PageManager pageManager, View view) {
        super(pageManager, view);
    }

    void newMatch() {
        class Data extends Request {
            @Override
            public void run(List<String> s) {
                pitMatch = new Gson().fromJson(s.get(0), PitMatch.class);
                match = pitMatch;

                String title = " Team: " + match.getTeam(MainActivity.position);
                status.setText(title);

                allData = new ArrayList<>();

                for(String team : pitMatch.teams) {
                    allData.add(new ArrayList<>());

                    class Set extends Request {
                        private int i = allData.size() - 1;

                        @Override
                        public void run(List<String> measures) {
                            Gson gson = new Gson();
                            for(String s : measures) if(!s.contains("end")) allData.get(i).add(gson.fromJson(s, Measure.class));
                        }
                    }
                    new Set().start("/matchteamtasks?team=" + team);
                }

                setMatch();
            }
        }
        new Data().start("/matchteams?match=na");
    }

    public void setTeam(int i) {
        pitMatch.position = i;
        data = allData.get(i);

        setMatch();
    }
}
