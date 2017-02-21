package com.stuin.irs_scout.Data;

/**
 * Created by Stuart on 2/10/2017.
 */
public class Measure {
    final public int match;
    final public int team;
    final public String task;
    final public String page;
    public String value;

    public Measure() {
        match = 0;
        team = 0;
        task = "";
        page = "";
        value = "";
    }

    public Measure(Task task, int match, int team) {
        this.match = match;
        this.team = team;
        this.task = task.successname;
        this.page = task.page;
        this.value = "";
    }
}
