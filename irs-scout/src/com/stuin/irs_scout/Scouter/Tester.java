package com.stuin.irs_scout.Scouter;

import android.app.Activity;
import com.stuin.irs_scout.R;

import java.util.Arrays;


public class Tester {
    public Tester(PageManager form, Activity activity) {
        //Set up updater class
        MatchMaker matchMaker = new MatchMaker(form.labelMaker.pageManager, activity.findViewById(R.id.Status));
        form.updater = new Updater(matchMaker, activity.findViewById(R.id.PageStatus));

        form.labelMaker.pagesMake(Arrays.asList(pages));
        form.labelMaker.taskMake(Arrays.asList(tasks));
    }

    private String[] pages = {

    };

    private String[] tasks = {

    };
}
