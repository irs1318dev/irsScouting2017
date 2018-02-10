package com.stuin.irs_scout.Scouter;

import android.content.Context;
import android.view.View;
import com.google.gson.Gson;
import com.stuin.cleanvisuals.Request;
import com.stuin.irs_scout.*;
import com.stuin.irs_scout.Data.InputData;
import com.stuin.irs_scout.Data.Section;
import com.stuin.irs_scout.Data.Task;
import com.stuin.irs_scout.Scouter.Inputs.*;
import com.stuin.irs_scout.Scouter.Page;
import com.stuin.irs_scout.Scouter.PageManager;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

/**
 * Created by Stuart on 2/12/2017.
 */
class LabelMaker {
    private ArrayList<Section> sections = new ArrayList<>();
    private PageManager pageManager;
    private Map<String, Page> pageList = new HashMap<>();

    LabelMaker(PageManager pageManager) {
        this.pageManager = pageManager;
    }

    void load(View status) {
        //Download layout from server
        class Layout extends Request {
            @Override
            public void run(List<String> s) {
                //Create list of pages
                pagesMake(s);

                class Tasks extends Request {
                    @Override
                    public void run(List<String> s) {
                        //Create all buttons
                        taskMake(s);

                        //Get Match
                        MatchMaker matchMaker;
                        if(MainActivity.position.contains("Pit")) {
                            //Set up pit scouter
                            matchMaker = new PitMatchMaker(pageManager, status);
                            TeamMenu teamMenu = (TeamMenu) pageManager.getChildAt(0);
                            teamMenu.pitMaker = (PitMatchMaker) matchMaker;
                        } else matchMaker = new MatchMaker(pageManager, status);

                        pageManager.setUpdater(matchMaker);
                    }
                }
                new Tasks().start("/gametasks");
            }
        }
        new Layout().start("/gamelayout");
    }

    private void pagesMake(List<String> layout) {
        //Prepare variables
        String current = "";
        Gson gson = new Gson();

        //Translate layout file
        for(String s : layout) {
            Section section = gson.fromJson(s, Section.class);
            if(usePage(section.observer, MainActivity.position)) sections.add(section);
        }

        //Build pagesMake
        for(Section section : sections)  {
            //Create each phase
            if(current.isEmpty() || !pageList.get(current).name.equals(section.phase)) {
                pageList.put(section.phase, pageManager.makePage(section.phase));
                current = section.phase;
            }
        }
    }

    private void taskMake(List<String> strings) {
        //Prepare variables for generation
        Map<String, Task> tasks = new HashMap<>();
        Gson gson = new Gson();
        Context context = pageManager.getContext();

        //Make list of tasks
        for(String s : strings) {
            Task task = gson.fromJson(s, Task.class);
            tasks.put(task.task, task);
        }

        //Check each section
        for(Section s : sections) {
            //Set column
            if(s.newpart.equals("true"))
                pageList.get(s.phase).newCol();

            //Set position
            if(s.position.isEmpty())
                s.position = MainActivity.position;
            else
                MainActivity.alliance = true;

            //Create label for section
            Input label = new Label(context, new InputData(new Task(s.category), s.position));
            pageList.get(s.phase).add(label);

            //Create inputs for section
            for(String t : s.tasks) if(tasks.containsKey(t)) {
                pageList.get(s.phase).add(makeLabel(tasks.get(t), context, s.phase, s.position));
            }
        }
    }

    private boolean usePage(String observer, String position) {
        //Check if phase is to be used
        if(position.toLowerCase().contains(observer)) return true;
        return observer.equals("match") && position.contains("Red") || position.contains("Blue");
    }

    private Input makeLabel(Task task, Context context, String phase, String position) {
        //Get special variables
        String format = task.getFormat(phase);
        InputData id = new InputData(task, position);

        //Choose format to create
        switch(format.charAt(0)) {
            case 'b':
                return new Switcher(context, id);
            case 'c':
                return new Count(context, id);
            case 'e':
                return new Choice(context, id);
            case 'p':
                return new Enter(context, id);
            case 'r':
                return new Rating(context, id);
            case 'l':
                return new Label(context, id);
        }
        return new Label(context, id);
    }
}
