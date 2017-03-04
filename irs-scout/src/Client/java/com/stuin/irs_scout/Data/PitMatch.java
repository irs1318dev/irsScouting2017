package com.stuin.irs_scout.Data;

/**
 * Created by Stuart on 3/3/2017.
 */
public class PitMatch extends Match {
    final public String[] teams;
    public int position = 0;

    PitMatch() {
        teams = new String[0];
    }

    @Override
    public String getTeam(String position) {
        return teams[this.position];
    }
}
