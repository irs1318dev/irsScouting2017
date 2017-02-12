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
    final public int id;

    public Task() {
        this.Task = "";
        this.Actor = "";
        this.Page = "";
        this.Format = "";
        this.Success = "";
        this.Miss = "";
        this.Additions = "";
        this.Compacting = 0;
        this.id = 0;
    }

    public String getName() { return Task; }
    public String getActor() { return Actor; }
    public String getPage() { return Page; }
    public String getFormat() { return Format; }
    public String getSuccess() { return Success; }
    public String getMiss() { return Miss; }
    public int getCompacting() {return Compacting;}



}
