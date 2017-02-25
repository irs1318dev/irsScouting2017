package com.stuin.irs_scout.Data;

/**
 * Created by Stuart on 2/10/2017.
 */
public class Measure {
    final public int match;
    final public int team;
    final public String task;
    final public String phase;
    public String value;
    public int success;
    public int miss;

    public Measure() {
        match = 0;
        team = 0;
        task = "";
        phase = "";
        value = "";
        success = 0;
        miss = 0;
    }

    public Measure(Task task, Match match, String position, String phase) {
        this.match = match.number;
        this.team = match.getTeam(position);
        this.task = task.task;
        this.phase = phase;
        this.value = "";
        this.success = 0;
        this.miss = 0;
    }
}
