package com.stuin.irs_scout.Scouter;

import android.app.Activity;
import android.content.Context;
import android.util.AttributeSet;
import android.view.View;
import android.widget.FrameLayout;
import android.widget.TextView;
import com.stuin.cleanvisuals.Slider;
import com.stuin.irs_scout.MainActivity;
import com.stuin.irs_scout.R;
import com.stuin.irs_scout.Scouter.Views.Page;
import com.stuin.irs_scout.Scouter.Views.TeamMenu;
import com.stuin.cleanvisuals.Request;

import java.util.List;

public class PageManager extends FrameLayout {
    public Updater updater;

    private int current = -1;
    private Activity activity;
    private LabelMaker labelMaker;
    private boolean moving;

    public PageManager(Context context, AttributeSet attributeSet) {
        super(context, attributeSet);
    }

    public void start(Activity activity) {
        //Start Layout
        labelMaker = new LabelMaker(this);
        setVisibility(VISIBLE);
        this.activity = activity;
        activity.findViewById(R.id.Status).setVisibility(VISIBLE);

        //Download layout
        class Layout extends Request {
            @Override
            public void run(List<String> s) {
                labelMaker.pages(s);

                class Tasks extends Request {
                    @Override
                    public void run(List<String> s) {
                        labelMaker.taskMake(s);

                        //Get Match
                        MatchMaker matchMaker;
                        if(MainActivity.position.contains("it")) {
                            matchMaker = new PitMaker(labelMaker.pageManager, activity.findViewById(R.id.Status));
                            TeamMenu teamMenu = (TeamMenu) getChildAt(0);
                            teamMenu.pitMaker = (PitMaker) matchMaker;
                        } else matchMaker = new MatchMaker(labelMaker.pageManager, activity.findViewById(R.id.Status));

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
        if(current != -1) getChildAt(current).setVisibility(GONE);

        current = 0;
        setPage();

        activity.findViewById(R.id.Previous).setVisibility(GONE);
        if(getChildCount() > 1) activity.findViewById(R.id.Next).setVisibility(VISIBLE);
    }

    Page makePage(String name) {
        //Create phase object
        Page page = new Page(getContext(), name);
        if(name.equals("pit")) page = new TeamMenu(getContext());

        page.setVisibility(GONE);
        addView(page);

        if(getChildCount() > 1) page.link((Page) getChildAt(getChildCount() - 2), new Slider.Endings() {
            @Override
            public void enter() {
                //Notify server
                if(updater != null) updater.setStatus();
                moving = false;
            }

            @Override
            public void exit() {
                //Notify server
                if(updater != null) updater.setStatus();
                moving = false;
            }
        });
        return page;
    }

    public void nextPage(View view) {
        if(!moving) {
            //Show next phase
            moving = true;
            ((Page) getChildAt(current + 1)).sliderSync.showPrimary();

            //Set shown buttons
            activity.findViewById(R.id.Previous).setVisibility(VISIBLE);
            if(current + 2 == getChildCount()) view.setVisibility(GONE);

            current++;
            setPage();
        }
    }

    public void lastPage(View view) {
        if(!moving) {
            //Hide old phase
            moving = true;
            ((Page) getChildAt(current)).sliderSync.showSecondary();

            //Set shown buttons
            activity.findViewById(R.id.Next).setVisibility(VISIBLE);
            if(current == 1) view.setVisibility(GONE);

            //Set new phase
            current--;
            setPage();
        }
    }

    private void setPage() {
        //Show new phase
        getChildAt(current).setVisibility(VISIBLE);

        //Set phase title
        String name =  ((Page) getChildAt(current)).name;
        name = name.substring(0,1).toUpperCase() + name.substring(1);
        ((TextView) activity.findViewById(R.id.PageStatus)).setText(MainActivity.position + ": " + name);

        updater.setStatus();
    }
}
