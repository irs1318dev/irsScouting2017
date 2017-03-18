package com.stuin.irs_scout.Data;

/**
 * Created by Stuart on 2/10/2017.
 */
public class Match {
    final public String match;
    final public String team1;
    final public String team2;
    final public String team3;
    final public String alliance;

    public Match() {
        match = "";
        team1 = "";
        team2 = "";
        team3 = "";
        alliance = "";
    }

    public String getTeam(String position) {
        switch(position.charAt(position.length() - 1)) {
            case '1':
                return team1;
            case '2':
                return team2;
            case '3':
                return team3;
        }
        return "";
    }
}
