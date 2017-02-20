package com.stuin.irs_scout;

import android.app.Activity;
import android.view.Gravity;
import android.view.View;
import android.widget.LinearLayout;
import android.widget.TextView;
import com.stuin.irs_scout.Data.Task;
import com.stuin.irs_scout.Views.Label;
import com.stuin.irs_scout.Views.Number;
import com.stuin.irs_scout.Views.Page;

import java.util.ArrayList;
import java.util.List;

class PageManager extends LinearLayout {
    List<Page> pages = new ArrayList<>();
    Updater updater;

    private int current = -1;
    private Activity activity;

    PageManager(Activity activity) {
        //Start Layout
        super(activity);
        this.activity = activity;

        //Setup centering
        LayoutParams lp = new LayoutParams(LayoutParams.MATCH_PARENT,LayoutParams.MATCH_PARENT);
        setLayoutParams(lp);
        setGravity(Gravity.CENTER);

        //Download layout
        class Generate extends Request {
            @Override
            public void run(List<String> s) {
                generate(s);
            }
        }
        new Generate().start("/gamelayout");
    }

    private void generate(List<String> s) {
        //Generate pages
        pages = new LabelMaker().pages(this, s);

        //Get Match
        MatchMaker matchMaker = new MatchMaker(this, activity.findViewById(R.id.Status));
        updater = new Updater(matchMaker, activity.findViewById(R.id.PageStatus));
    }

    void reset() {
        //Set default page
        if(current != -1) pages.get(current).setVisibility(GONE);

        current = 0;
        setPage();

        activity.findViewById(R.id.Previous).setVisibility(GONE);
        if(pages.size() > 1) activity.findViewById(R.id.Next).setVisibility(VISIBLE);
    }

    Page makePage(String name) {
        //Create page object
        Page page = new Page(getContext(), name);
        page.setVisibility(GONE);
        addView(page);
        return page;
    }

    void nextPage(View view) {
        //Show next page
        pages.get(current).setVisibility(GONE);
        pages.get(current).send();

        //Set shown buttons
        activity.findViewById(R.id.Previous).setVisibility(VISIBLE);
        if(current + 2 == pages.size()) view.setVisibility(GONE);

        current++;
        setPage();
    }

    void lastPage(View view) {
        //Hide old page
        pages.get(current).setVisibility(GONE);
        pages.get(current).send();

        //Set shown buttons
        activity.findViewById(R.id.Next).setVisibility(VISIBLE);
        if(current == 1) view.setVisibility(GONE);

        //Set new page
        current--;
        setPage();
    }

    private void setPage() {
        //Show new page
        pages.get(current).setVisibility(VISIBLE);

        //Set page title
        TextView textView = (TextView) activity.findViewById(R.id.PageStatus);
        textView.setText(MainActivity.position + ": " + pages.get(current).name);

        //Notify server
        if(updater != null) updater.setStatus();
    }
}
