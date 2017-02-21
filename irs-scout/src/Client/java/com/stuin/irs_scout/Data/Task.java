package com.stuin.irs_scout.Data;

/**
 * Created by Stuart on 2/10/2017.
 */
public class Task {
    final public String task;
    final public String observer;
    final public String phase;
    final public String format;
    final public String successname;
    final public String missname;
    final public String enums;

    public Task() {
        task = "";
        observer = "";
        phase = "";
        format = "";
        successname = "";
        missname = "";
        enums = "";
    }

    public Task(String name) {
        task = "";
        observer = "";
        phase = "";
        format = "label";
        successname = name;
        missname = "";
        enums = "";
    }
}
