package com.stuin.irs_scout.Data;

/**
 * Created by Stuart on 2/10/2017.
 */
public class Measure {
    final public String match;
    final public int team;
    final public String task;
    final public String phase;
    public String capability;
    public int success;
    public int attempt;

    public Measure() {
        match = "";
        team = 0;
        task = "";
        phase = "";
        capability = "";
        success = 0;
        attempt = 0;
    }

    public Measure(Task task, Match match, String position, String phase) {
        this.match = match.number;
        this.team = match.getTeam(position);
        this.task = task.task;
        this.phase = phase;
        this.capability = "";
        this.success = 0;
        this.attempt = 0;
    }
}
