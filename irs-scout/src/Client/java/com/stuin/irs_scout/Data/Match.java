package com.stuin.irs_scout.Data;

/**
 * Created by Stuart on 2/10/2017.
 */
public class Match {
    final public int number;
    final public int team1;
    final public int team2;
    final public int team3;
    final public String alliance;

    public Match() {
        number = 0;
        team1 = 0;
        team2 = 0;
        team3 = 0;
        alliance = "";
    }

    public int getTeam(String position) {
        switch(position.charAt(position.length() - 1)) {
            case '1':
                return team1;
            case '2':
                return team2;
            case '3':
                return team3;
        }
        return 0;
    }
}
