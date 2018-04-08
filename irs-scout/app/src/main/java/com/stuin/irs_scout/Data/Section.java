package com.stuin.irs_scout.Data;

import com.stuin.irs_scout.MainActivity;

/**
 * Created by Stuart on 2/20/2017.
 */
public class Section {
    final public String actor;
    final public String observer;
    final public String phase;
    final public String category;
    final public String[] tasks;
    final public String newpart;
    public String position;

    public Section() {
        actor = "";
        observer = "";
        phase = "";
        category = "";
        position = MainActivity.position;
        tasks = new String[0];
        newpart = "false";
    }
}
