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
    List<Page> pages(PageManager pageManager, List<String> layout) {
        //Prepare variables
        List<Page> pageList = new ArrayList<>();
        List<Task> tasks = new ArrayList<>();
        int current = -1;
        Gson gson = new Gson();

        //Translate layout file
        for(String s : layout) tasks.add(gson.fromJson(s, Task.class));

        //Build pages
        for(Task task : tasks) if(usePage(task.actor, MainActivity.position)) {
            //Create each page
            if(current == -1 || !pageList.get(current).name.equals(task.page)) {
                pageList.add(pageManager.makePage(task.page));
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
        //Choose format to create
        switch(task.format.charAt(0)) {
            case 'S':
                return new Switcher(context, task);
            case 'C':
                return new Counter(context, task);
        }
        return new Label(context, task);
    }
}
