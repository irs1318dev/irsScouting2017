package com.stuin.irs_scout;

import android.view.View;
import android.widget.TextView;
import com.google.gson.Gson;
import com.stuin.irs_scout.Data.Match;
import com.stuin.irs_scout.Data.Measure;
import com.stuin.irs_scout.MainActivity;
import com.stuin.cleanvisuals.Request;
import com.stuin.irs_scout.Scouter.Page;
import com.stuin.irs_scout.Scouter.PageManager;
import org.w3c.dom.Text;

import java.util.*;

/**
 * Created by Stuart on 2/14/2017.
 */
public class MatchMaker {
    Match match = new Match();
    public TextView nameView = null;

    private PageManager pageManager;
    protected static List<Measure> data;
    protected Queue<String> nextTeams;
    protected TextView status;

    public MatchMaker(PageManager pageManager, View view) {
        //Set variables
        this.pageManager = pageManager;
        status = (TextView) view;
        newMatch();
    }

    void newMatch() {
        //Get team list
        class Data extends Request {
            @Override
            public void run(List<String> s) {
                //Get correct alliance
                match = new Gson().fromJson(s.get(0), Match.class);
                if(MainActivity.position.toLowerCase().charAt(0) != match.alliance.charAt(0)) match = new Gson().fromJson(s.get(1), Match.class);

                //Write match at top
                String title = "Match: " + match.match;
                if(!MainActivity.alliance) title += " Team: " + match.getTeam(MainActivity.position);
                status.setText(title);
                data = new ArrayList<>();

                //Get any previous match data
                class Set extends Request {
                    @Override
                    public void run(List<String> measures) {
                        //Add data to list
                        Gson gson = new Gson();
                        for(String s : measures) if(!s.contains("end")) data.add(gson.fromJson(s, Measure.class));

                        //If any other match data to get
                        if(nextTeams != null && !nextTeams.isEmpty()) new Set().start(nextTeams.poll());
                        else setMatch();
                    }
                }

                //Format request for each team
                if(!MainActivity.alliance) new Set().start("/matchteamtasks?team=" + match.getTeam(MainActivity.position));
                else {
                    new Set().start("/matchteamtasks?team=" + match.getTeam("1"));
                    nextTeams = new ArrayDeque<>();
                    nextTeams.add("/matchteamtasks?team=" + match.getTeam("2"));
                    nextTeams.add("/matchteamtasks?team=" + match.getTeam("3"));
                }
            }
        }
        new Data().start("/matchteams");
    }

    void setMatch() {
        //Clear previous data
        pageManager.reset();

        //Get each page
        for(int i = 0; i < pageManager.getChildCount(); i++) {
            Map<String, Measure> pageData = new HashMap<>();
            Page p = (Page) pageManager.getChildAt(i);

            //Enter any data from server
            for(Measure m : data) {
                if(m.phase.equals(p.name)) pageData.put(m.task + ':' + m.team, m);
            }
            p.setMeasures(pageData, match);
        }

        setName();
    }

    private void setName() {
        class Name extends Request {
            @Override
            String name = s.get(0);
            public void run(List<String> s) {
                if(nameView != null && s.size() > 0 && !s.get(0).equals("na")) {

                    while(name.length() > 33) {
                        int i = name.length() - 1;
                        while(i > 0 && name.charAt(i) != ' ')
                            i--;
                        name = name.substring(0, i) + "...";
                    }

                    nameView.setText(name);
                    nameView.setVisibility(View.VISIBLE);
                }
            }
        }
        if(!MainActivity.alliance)
            new Name().start("/teamname?team=" + match.getTeam(MainActivity.position));
    }

    static void update(Measure measure) {
        //Add measure to offline backup
        for(int i = 0; i < data.size(); i++) {
            Measure m = data.get(i);
            //Check for previous entry
            if(measure.equals(m)) {
                data.set(i, measure);
                return;
            }
        }
        data.add(measure);
    }
}
