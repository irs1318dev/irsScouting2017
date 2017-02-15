package com.stuin.irs_scout;

import com.google.gson.Gson;
import com.stuin.irs_scout.Data.Match;
import com.stuin.irs_scout.Data.Measure;
import com.stuin.irs_scout.Views.Page;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;

/**
 * Created by Stuart on 2/14/2017.
 */
public class MatchMaker {
    private Match match = new Match();
    private List<Measure> data = new ArrayList<>();
    private Map<String, Page> pages;

    public void newMatch() {
        class Data extends Next {
            @Override
            public void run(List<String> s) {
                match = new Gson().fromJson(s.get(0), Match.class);
                class End extends Next {
                    @Override
                    public void run(List<String> measures) {
                        Gson gson = new Gson();
                        for(String s : measures) data.add(gson.fromJson(s, Measure.class));
                    }
                }
                new Request("/matchdata",new End());
            }
        }
        new Request("/match", new Data());
    }

    public void setMatch() {

    }
}
