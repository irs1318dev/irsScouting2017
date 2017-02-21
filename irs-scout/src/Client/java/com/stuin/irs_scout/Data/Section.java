package com.stuin.irs_scout.Data;

/**
 * Created by Stuart on 2/20/2017.
 */
public class Section {
    final public String actor;
    final public String observer;
    final public String phase;
    final public String category;
    final public String[] tasks;

    public Section() {
        actor = "";
        observer = "";
        phase = "";
        category = "";
        tasks = new String[0];
    }
}
