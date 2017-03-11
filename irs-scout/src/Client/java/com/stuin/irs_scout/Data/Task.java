package com.stuin.irs_scout.Data;

/**
 * Created by Stuart on 2/10/2017.
 */
public class Task {
    final public String task;
    final public String observer;
    final public String claim;
    final public String auto;
    final public String teleop;
    final public String finish;
    final public String success;
    final public String miss;
    final public String enums;

    public Task() {
        task = "";
        observer = "";
        claim = "";
        auto = "";
        teleop = "";
        finish = "";
        success = "";
        miss = "";
        enums = "";
    }

    public Task(String name) {
        task = "";
        observer = "robot";
        claim = "label";
        auto = "label";
        teleop = "label";
        finish = "label";
        success = name;
        miss = "";
        enums = "";
    }

    public String getFormat(String phase) {
        //Get format from phase
        String format = "na";
        switch(phase.charAt(0)) {
            case 'c':
                format = claim;
                break;
            case 'a':
                format = auto;
                break;
            case 't':
                format = teleop;
                break;
            case 'f':
                format = finish;
                break;
        }
        return format;
    }
}
