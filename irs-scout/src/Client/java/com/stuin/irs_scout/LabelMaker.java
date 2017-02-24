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
    PageManager pageManager;
    private Map<String, Page> pageList = new HashMap<>();

    LabelMaker(PageManager pageManager) {
        this.pageManager = pageManager;
    }

    void pages(List<String> layout) {
        //Prepare variables
        String current = "";
        Gson gson = new Gson();

        //Translate layout file
        for(String s : layout) {
            Section section = gson.fromJson(s, Section.class);
            if(usePage(section.observer, MainActivity.position)) sections.add(section);
        }

        //Build pages
        for(Section section : sections)  {
            //Create each phase
            if(current.isEmpty() || !pageList.get(current).name.equals(section.phase)) {
                pageList.put(section.phase, pageManager.makePage(section.phase));
                current = section.phase;
            }
        }
    }

    List<Page> taskMake(List<String> strings) {
        Map<String, Task> tasks = new HashMap<>();
        Gson gson = new Gson();
        Context context = pageManager.getContext();
        List<Page> pages = new ArrayList<>();

        for(String s : strings) {
            Task task = gson.fromJson(s, Task.class);
            tasks.put(task.task, task);
        }

        for(Section s : sections) {
            if(s.newpart.equals("true")) pageList.get(s.phase).newCol();
            pageList.get(s.phase).add(new Label(context, new Task(s.category)));

            for(String t : s.tasks) if(tasks.containsKey(t)) {
                pageList.get(s.phase).add(makeLabel(tasks.get(t), context, s.phase));
            }

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

    private Label makeLabel(Task task, Context context, String phase) {
        //Get format from phase
        String format = "na";
        switch(phase.charAt(0)) {
            case 'c':
                format = task.claim;
                break;
            case 'a':
                format = task.auto;
                break;
            case 't':
                format = task.teleop;
                break;
            case 'f':
                format = task.finish;
                break;
        }

        //Choose format to create

        switch(format.charAt(0)) {
            case 'b':
                return new Switcher(context, task);
            case 'c':
                return new Count(context, task);
            case 'e':
                return new Choice(context, task);
            case 'p':
                return new Enter(context, task);
            case 'l':
                return new Label(context, task);
        }
        return new Label(context, new Task());
    }
}
