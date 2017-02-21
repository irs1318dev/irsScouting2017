package com.stuin.irs_scout;

import android.content.Context;
import com.google.gson.Gson;
import com.stuin.irs_scout.Data.Section;
import com.stuin.irs_scout.Data.Task;
import com.stuin.irs_scout.Views.*;
import com.stuin.irs_scout.Views.Count;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

/**
 * Created by Stuart on 2/12/2017.
 */
class LabelMaker {
    private List<Section> sections = new ArrayList<>();

    Map<String, Page> pages(PageManager pageManager, List<String> layout) {
        //Prepare variables
        Map<String, Page> pageList = new HashMap<>();
        int current = -1;
        Gson gson = new Gson();

        //Translate layout file
        for(String s : layout) sections.add(gson.fromJson(s, Section.class));

        //Build pages
        for(Section section : sections) if(usePage(section.observer, MainActivity.position)) {
            //Create each phase
            if(current == -1 || !pageList.get(current).name.equals(section.phase)) {
                pageList.put(section.phase, pageManager.makePage(section.phase));
                current++;
            }
        }
        return pageList;
    }

    List<Page> taskMake(Context context, List<String> strings, Map<String, Page> pageList) {
        Map<String, Task> tasks = new HashMap<>();
        Gson gson = new Gson();
        List<Page> pages = new ArrayList<>();

        for(String s : strings) {
            Task task = gson.fromJson(s, Task.class);
            tasks.put(task.task, task);
        }

        for(Section s : sections) {
            pageList.get(s.phase).add(new Label(context, new Task(s.category)));
            for(String t : s.tasks) pageList.get(s.phase).add(makeLabel(tasks.get(t), context));

            if(!pages.contains(pageList.get(s.phase))) pages.add(pageList.get(s.phase));
        }

        return pages;
    }

    private boolean usePage(String observer, String position) {
        //Check if phase is to be used
        if(observer.equals("match") && !position.contains("Boiler")) return true;
        if(observer.equals("boiler") && position.contains("Boiler")) return true;
        return false;
    }

    private Label makeLabel(Task task, Context context) {
        //Choose format to create
        switch(task.format.charAt(0)) {
            case 'b':
                return new Switcher(context, task);
            case 'c':
                return new Count(context, task);
            case 'e':
                return new Choice(context, task);
            case 'p':
                return new Enter(context, task);
        }
        return new Label(context, task);
    }
}
