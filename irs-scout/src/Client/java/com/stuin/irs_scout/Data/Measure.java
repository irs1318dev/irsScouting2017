package com.stuin.irs_scout.Data;

/**
 * Created by Stuart on 2/10/2017.
 */
public class Measure {
    final public int match;
    final public int team;
    final public int taskId;
    final public String page;
    public int success;
    public int miss;

    public Measure() {
        match = 0;
        team = 0;
        taskId = 0;
        page = "";
        success = 0;
        miss = 0;
    }

    public Measure(Task task, int match, int team) {
        this.match = match;
        this.team = team;
        this.taskId = task.id;
        this.page = task.page;
        this.success = 0;
        this.miss = 0;
    }

    public boolean matches(Measure measure) {
        return (measure.taskId == taskId && measure.team == team && measure.match == match);
    }
}
