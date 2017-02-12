package com.stuin.irs_scout;

import android.content.Context;
import com.google.gson.Gson;
import com.stuin.irs_scout.Data.Task;
import com.stuin.irs_scout.Views.Counter;
import com.stuin.irs_scout.Views.Label;
import com.stuin.irs_scout.Views.Page;
import com.stuin.irs_scout.Views.Switcher;

import java.util.ArrayList;
import java.util.List;

/**
 * Created by Stuart on 2/12/2017.
 */
class LabelMaker {
    List<Page> pages(Request request, PageManager pageManager) {
        List<Page> pageList = new ArrayList<>();
        int current = -1;

        //Prepare for layout file
        Gson gson = new Gson();
        List<Task> tasks = new ArrayList<>();

        //Get layout and translate
        List<String> layout = request.get("Game/layout");
        for(String s : layout) tasks.add(gson.fromJson(s, Task.class));

        for(Task task : tasks) if(usePage(task.getActor(), pageManager.position)) {
            //Create each page
            if(current == -1 || !pageList.get(current).name.equals(task.getPage())) {
                pageList.add(pageManager.makePage(task.getPage()));
                current++;
            }
            //Add task to page
            pageList.get(current).add(makeLabel(task, pageManager.getContext()));
        }
        return pageList;
    }

    private boolean usePage(String actor, String position) {
        //Check if page is to be used
        if(actor.equals("Robot") && !position.contains("Pilot")) return true;
        if(actor.equals("Final") && position.charAt(position.length() - 1) == '1') return true;
        if(actor.equals("Pilot") && position.contains("Pilot")) return true;
        return false;
    }

    private Label makeLabel(Task task, Context context) {
        switch(task.getFormat().charAt(0)) {
            case 'S':
                return new Switcher(context, task);
            case 'C':
                return new Counter(context, task);
        }
        return new Label(context, task);
    }
}
