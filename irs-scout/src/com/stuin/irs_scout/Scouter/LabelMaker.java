package com.stuin.irs_scout.Scouter;

import android.content.Context;
import com.google.gson.Gson;
import com.stuin.irs_scout.Data.Section;
import com.stuin.irs_scout.Data.Task;
import com.stuin.irs_scout.MainActivity;
import com.stuin.irs_scout.Scouter.Views.*;

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

    void taskMake(List<String> strings) {
        Map<String, Task> tasks = new HashMap<>();
        Gson gson = new Gson();
        Context context = pageManager.getContext();

        for(String s : strings) {
            Task task = gson.fromJson(s, Task.class);
            tasks.put(task.task, task);
        }

        for(Section s : sections) {
            if(s.newpart.equals("true")) pageList.get(s.phase).newCol();
            if(s.position.isEmpty()) s.position = MainActivity.position;

            Label label = new Label(context, new Task(s.category), s.position);
            label.sectionLabel = true;
            pageList.get(s.phase).add(label);

            for(String t : s.tasks) if(tasks.containsKey(t)) {
                pageList.get(s.phase).add(makeLabel(tasks.get(t), context, s.phase, s.position));
            }
        }
    }

    private boolean usePage(String observer, String position) {
        //Check if phase is to be used
        if(observer.equals("match") && !position.contains("Fuel") && !position.contains("Pit")) return true;
        if(observer.equals("boiler") && position.contains("Fuel")) return true;
        if(observer.equals("pit") && position.contains("Pit")) return true;
        return false;
    }

    private Label makeLabel(Task task, Context context, String phase, String position) {
        String format = task.getFormat(phase);

        //Choose format to create

        switch(format.charAt(0)) {
            case 'b':
                return new Switcher(context, task, position);
            case 'c':
                return new Count(context, task, position);
            case 'e':
                return new Choice(context, task, position);
            case 'p':
                return new Enter(context, task, position);
            case 'l':
                return new Label(context, task, position);
        }
        return new Label(context, new Task(), position);
    }
}
