package com.stuin.irs_scout;

import android.app.Activity;
import android.view.Gravity;
import android.view.View;
import android.widget.LinearLayout;
import android.widget.TextView;
import com.stuin.irs_scout.Views.Page;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

class PageManager extends LinearLayout {
    Map<String, Page> fullPages = new HashMap<>();
    List<Page> pages = new ArrayList<>();
    Updater updater;

    private int current = -1;
    private Activity activity;
    private PageManager pageManager;

    PageManager(Activity newActivity) {
        super(newActivity);
        //Start Layout
        pageManager = this;
        this.activity = newActivity;

        //Setup centering
        LayoutParams lp = new LayoutParams(LayoutParams.MATCH_PARENT,LayoutParams.MATCH_PARENT);
        setLayoutParams(lp);
        setGravity(Gravity.CENTER);

        //Download layout
        class Layout extends Request {
            @Override
            public void run(List<String> s) {
                fullPages = new LabelMaker().pages(pageManager, s);

                class Tasks extends Request {
                    @Override
                    public void run(List<String> s) {
                        pages = new LabelMaker().taskMake(getContext(), s, fullPages);

                        //Get Match
                        MatchMaker matchMaker = new MatchMaker(pageManager, activity.findViewById(R.id.Status));
                        updater = new Updater(matchMaker, activity.findViewById(R.id.PageStatus));
                    }
                }
                new Tasks().start("/gametasks");
            }
        }
        new Layout().start("/gamelayout");
    }

    void reset() {
        //Set default phase
        if(current != -1) pages.get(current).setVisibility(GONE);

        current = 0;
        setPage();

        activity.findViewById(R.id.Previous).setVisibility(GONE);
        if(pages.size() > 1) activity.findViewById(R.id.Next).setVisibility(VISIBLE);
    }

    Page makePage(String name) {
        //Create phase object
        Page page = new Page(getContext(), name);
        page.setVisibility(GONE);
        addView(page);
        return page;
    }

    void nextPage(View view) {
        //Show next phase
        pages.get(current).setVisibility(GONE);
        pages.get(current).send();

        //Set shown buttons
        activity.findViewById(R.id.Previous).setVisibility(VISIBLE);
        if(current + 2 == pages.size()) view.setVisibility(GONE);

        current++;
        setPage();
    }

    void lastPage(View view) {
        //Hide old phase
        pages.get(current).setVisibility(GONE);
        pages.get(current).send();

        //Set shown buttons
        activity.findViewById(R.id.Next).setVisibility(VISIBLE);
        if(current == 1) view.setVisibility(GONE);

        //Set new phase
        current--;
        setPage();
    }

    private void setPage() {
        //Show new phase
        pages.get(current).setVisibility(VISIBLE);

        //Set phase title
        TextView textView = (TextView) activity.findViewById(R.id.PageStatus);
        textView.setText(MainActivity.position + ": " + pages.get(current).name);

        //Notify server
        if(updater != null) updater.setStatus();
    }
}
