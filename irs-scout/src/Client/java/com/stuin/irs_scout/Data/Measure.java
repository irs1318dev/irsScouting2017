package com.stuin.irs_scout.Data;

/**
 * Created by Stuart on 2/10/2017.
 */
public class Measure {
    final public int match;
    final public int team;
    final public String page;
    final public String actor;
    final public String task;
    public int success;
    public int miss;

    public Measure() {
        match = 0;
        team = 0;
        task = "";
        page = "";
        actor = "";
        success = 0;
        miss = 0;
    }

    public Measure(Task task, int match, int team) {
        this.match = match;
        this.team = team;
        this.page = task.page;
        this.actor = task.actor;
        this.task = task.task;
        this.success = 0;
        this.miss = 0;
    }
}
