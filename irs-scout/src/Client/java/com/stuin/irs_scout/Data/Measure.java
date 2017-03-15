package com.stuin.irs_scout.Data;

/**
 * Created by Stuart on 2/10/2017.
 */
public class Measure {
    final public String match;
    final public String team;
    final public String task;
    final public String phase;
    public String capability;
    public int successes;
    public int attempts;
    public int cycle_times;

    public Measure() {
        match = "";
        team = "";
        task = "";
        phase = "";
        capability = "";
        successes = 0;
        attempts = 0;
        cycle_times = 0;
    }

    public Measure(Task task, Match match, String position, String phase) {
        this.match = match.match;
        this.team = match.getTeam(position);
        this.task = task.task;
        this.phase = phase;
        this.capability = "";
        this.successes = 0;
        this.attempts = 0;
        this.cycle_times = 0;
    }
}
