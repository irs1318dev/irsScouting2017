package com.stuin.irs_scout.Scouter;

import android.view.View;
import com.google.gson.Gson;
import com.stuin.cleanvisuals.Request;
import com.stuin.irs_scout.Data.Measure;
import com.stuin.irs_scout.Data.PitMatch;
import com.stuin.irs_scout.MainActivity;

import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.List;

/**
 * Created by Stuart on 3/3/2017.
 */
public class PitMaker extends MatchMaker {
    private PitMatch pitMatch;
    private List<String> teams;
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

                teams = new ArrayList<>();
                data = new ArrayList<>();
                allData = new ArrayList<>();
                nextTeams = new ArrayDeque<>();

                class Set extends Request {
                    private int i;

                    @Override
                    public void start(String query) {
                        super.start(query);
                        i = teams.indexOf(query.split("=")[2]);
                    }

                    @Override
                    public void run(List<String> measures) {
                        Gson gson = new Gson();
                        for(String s : measures) if(!s.contains("end")) allData.get(i).add(gson.fromJson(s, Measure.class));
                        if(!nextTeams.isEmpty()) new Set().start(nextTeams.poll());
                        else setMatch();
                    }
                }

                for(String team : pitMatch.teams) {
                    allData.add(new ArrayList<>());
                    teams.add(team);
                    if(!team.equals("na")) nextTeams.add("/matchteamtasks?match=na&team=" + team);
                }

                new Set().start(nextTeams.poll());
            }
        }
        new Data().start("/matchteams?match=na");
    }

    public void setTeam(int i) {
        allData.set(pitMatch.position, data);
        pitMatch.position = i;
        data = allData.get(i);

        String title = " Team: " + match.getTeam(MainActivity.position);
        status.setText(title);

        setMatch();
    }
}
