package com.stuin.irs_scout.Data;

/**
 * Created by Stuart on 2/10/2017.
 */
public class Task {
    final public String Task;
    final public String Actor;
    final public String Page;
    final public String Format;
    final public String Success;
    final public String Miss;
    final public String Additions;
    final public int Compacting;
    final public boolean NewPart;

    public Task() {
        Task = "";
        Actor = "";
        Page = "";
        Format = "";
        Success = "";
        Miss = "";
        Additions = "";
        Compacting = 0;
        NewPart = false;
    }
}
