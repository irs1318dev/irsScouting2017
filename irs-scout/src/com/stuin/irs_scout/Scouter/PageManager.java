package com.stuin.irs_scout.Scouter;

import android.app.Activity;
import android.content.Context;
import android.util.AttributeSet;
import android.view.View;
import android.widget.FrameLayout;
import android.widget.TextView;
import com.stuin.cleanvisuals.Slide.Endings;
import com.stuin.irs_scout.*;
import com.stuin.cleanvisuals.Request;

import java.util.List;

public class PageManager extends FrameLayout {
    private Updater updater;
    private int current = -1;
    private Activity activity;
    private boolean moving;

    public PageManager(Context context, AttributeSet attributeSet) {
        super(context, attributeSet);
    }

    public void start(Activity activity) {
        //Start Layout
        setVisibility(VISIBLE);
        this.activity = activity;
        activity.findViewById(R.id.Status).setVisibility(VISIBLE);

        //Create input from server
        new LabelMaker(this).load(activity.findViewById(R.id.Status));
    }

    void setUpdater(MatchMaker matchMaker) {
        updater = new Updater(matchMaker, activity.findViewById(R.id.PageStatus));
    }

    public void reset() {
        //Set default phase
        if(current != -1) getChildAt(current).setVisibility(GONE);

        //Set page variables
        current = 0;
        confirmPage();

        //Set button visibility
        activity.findViewById(R.id.Previous).setVisibility(GONE);
        if(getChildCount() > 1) activity.findViewById(R.id.Next).setVisibility(VISIBLE);
    }

    public void setStatus() {
        updater.setStatus();
    }

    Page makePage(String name) {
        //Create phase object
        Page page = new Page(getContext(), name);
        if(name.equals("pit")) page = new TeamMenu(getContext());

        //Hide created page
        page.setVisibility(GONE);
        addView(page);

        //Set animation endings
        if(getChildCount() > 1) page.link((Page) getChildAt(getChildCount() - 2), new Endings() {
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

            //Set new phase
            current++;
            confirmPage();
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
            confirmPage();
        }
    }

    private void confirmPage() {
        //Show new phase
        getChildAt(current).setVisibility(VISIBLE);

        //Set phase title
        String name =  ((Page) getChildAt(current)).name;
        name = name.substring(0,1).toUpperCase() + name.substring(1);
        ((TextView) activity.findViewById(R.id.PageStatus)).setText(MainActivity.position + ": " + name);
    }
}
