package com.stuin.irs_scout.Data;

/**
 * Created by Stuart on 2/10/2017.
 */
public class Measure {
    final public int Match;
    final public int Team;
    final public String Task;
    final public String Page;
    final public String Actor;
    public int Success;
    public int Miss;

    public Measure() {
        Match = 0;
        Team = 0;
        Task = "";
        Page = "";
        Actor = "";
        Success = 0;
        Miss = 0;
    }

    public Measure(Task task, int match, int team) {
        Match = match;
        Team = team;
        Task = task.Task;
        Page = task.Page;
        Actor = task.Actor;
        Success = 0;
        Miss = 0;
    }
}
