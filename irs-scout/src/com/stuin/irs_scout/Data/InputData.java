package com.stuin.irs_scout.Data;

import com.stuin.irs_scout.Updater;

/**
 * Created by Stuart on 8/3/2017.
 */
public class InputData {
    public Task task;
    public String position;
    public Measure measure;

    private static boolean enforceSend = true;

    public InputData(Task task, String position) {
        this.task = task;
        this.position = position;
    }

    public void update(Measure measure, boolean send) {
        this.measure = measure;
        if(send && InputData.enforceSend) Updater.addMeasure(measure);
    }
}
