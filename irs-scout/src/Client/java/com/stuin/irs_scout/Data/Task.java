package com.stuin.irs_scout.Data;

/**
 * Created by Stuart on 2/10/2017.
 */
public class Task {
    final public String name;
    final public String task;
    final public String actor;
    final public String page;
    final public String format;
    final public String success;
    final public String miss;
    final public String additions;
    final public boolean compacting;
    final public boolean newpart;

    public Task() {
        name = "";
        task = "";
        actor = "";
        page = "";
        format = "";
        success = "";
        miss = "";
        additions = "";
        compacting = false;
        newpart = false;
    }
}
