package com.stuin.irs_scout;

import android.content.Context;
import android.view.Gravity;
import android.view.View;
import android.widget.LinearLayout;
import android.widget.TextView;
import com.google.gson.Gson;
import com.stuin.irs_scout.Data.Task;
import com.stuin.irs_scout.Views.Counter;
import com.stuin.irs_scout.Views.Label;
import com.stuin.irs_scout.Views.Switcher;

import java.util.ArrayList;
import java.util.List;

class Form extends LinearLayout {
    private List<FormPage> pages = new ArrayList<>();
    private Request request;
    private String position;
    private int current = -1;

    Form(Context context, Request request, String position) {
        //Start Layout
        super(context);
        this.request = request;
        this.position = position;

        //Setup centering
        LayoutParams lp = new LayoutParams(LayoutParams.MATCH_PARENT,LayoutParams.MATCH_PARENT);
        setLayoutParams(lp);
        setGravity(Gravity.CENTER);

        //Prepare for layout file
        Gson gson = new Gson();
        List<Task> tasks = new ArrayList<>();

        //Get layout and translate
        List<String> layout = request.get("Game/layout");
        for(String s : layout) tasks.add(gson.fromJson(s, Task.class));

        for(Task task : tasks) {
            //Create each page
            if((current == -1 || !pages.get(current).name.equals(task.getPage())) && usePage(task.getActor())) {
                current++;
                pages.add(new FormPage(context, task.getPage()));
                pages.get(current).setVisibility(GONE);
                addView(pages.get(current));
            }
            //Add task to page
            pages.get(current).add(makeLabel(task));
        }

        //Set default page
        current = 0;
        setPage();
        if(pages.size() > 1)findViewById(R.id.Next);
    }

    private boolean usePage(String actor) {
        //Check if page is to be used
        return (actor.equals("Robot") && position.substring(position.length() - 1).matches("\\d")) ||
        (actor.equals("Final") && position.charAt(position.length() - 1) == '1') ||
        (actor.equals("Pilot") && position.contains("Pilot"));
    }

    private Label makeLabel(Task task) {
        switch(task.getFormat().charAt(0)) {
            case 'S':
                return new Switcher(getContext(), task);
            case 'C':
                return new Counter(getContext(), task);
        }
        return new Label(getContext(), task);
    }

    void nextPage(View view) {
        //Show next page
        pages.get(current).setVisibility(GONE);
        current++;

        //Set shown buttons
        findViewById(R.id.Previous).setVisibility(VISIBLE);
        if(current + 1 == pages.size()) view.setVisibility(GONE);

        setPage();
    }

    void lastPage(View view) {
        //Show next page
        pages.get(current).setVisibility(GONE);
        current--;

        //Set shown buttons
        findViewById(R.id.Next).setVisibility(VISIBLE);
        if(current == 0) view.setVisibility(GONE);

        setPage();
    }

    private void setPage() {
        pages.get(current).setVisibility(VISIBLE);

        TextView textView = (TextView) findViewById(R.id.PageStatus);
        //textView.setText(pages.get(current).name);

        //Notify server
        request.post("Tablet/" + position, "Page" + current);
    }
}
