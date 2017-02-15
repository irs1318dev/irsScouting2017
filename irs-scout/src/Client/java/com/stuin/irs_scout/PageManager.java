package com.stuin.irs_scout;

import android.app.Activity;
import android.content.Context;
import android.view.Gravity;
import android.view.View;
import android.widget.LinearLayout;
import android.widget.TextView;
import com.stuin.irs_scout.Views.Page;

import java.util.ArrayList;
import java.util.List;

class PageManager extends LinearLayout {
    private List<Page> pages = new ArrayList<>();
    private int current = 0;
    private Activity activity;
    private MatchMaker matchMaker;

    PageManager(Activity activity) {
        //Start Layout
        super(activity);
        this.activity = activity;

        //Setup centering
        LayoutParams lp = new LayoutParams(LayoutParams.MATCH_PARENT,LayoutParams.MATCH_PARENT);
        setLayoutParams(lp);
        setGravity(Gravity.CENTER);

        //Download layout
        class Generate extends Next {
            @Override
            public void run(List<String> s) {
                generate(s);
            }
        }
        new Request("/game",new Generate());
    }

    private void generate(List<String> s) {
        //Generate pages
        pages = new LabelMaker().pages(this, s);

        //Set default page
        setPage();
        if(pages.size() > 1) activity.findViewById(R.id.Next).setVisibility(VISIBLE);

        //Get Match
        matchMaker = new MatchMaker(pages, activity.findViewById(R.id.Status));
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
        current++;

        //Set shown buttons
        activity.findViewById(R.id.Previous).setVisibility(VISIBLE);
        if(current + 1 == pages.size()) view.setVisibility(GONE);

        setPage();
    }

    void lastPage(View view) {
        //Hide old page
        pages.get(current).setVisibility(GONE);

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
        textView.setText(pages.get(current).name);

        //Notify server

    }
}
