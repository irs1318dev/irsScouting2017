package com.stuin.irs_scout.Data;

import com.stuin.irs_scout.Scouter.Updater;

/**
 * Created by Stuart on 8/3/2017.
 */
public class InputData {
    public Task task;
    public String position;
    public Measure measure;
    public boolean sectionLabel;

    public InputData(Task task, String position) {
        this.task = task;
        this.position = position;
    }

    public void update(Measure measure, boolean send) {
        this.measure = measure;
        if(send) Updater.measures.add(measure);
    }
}
