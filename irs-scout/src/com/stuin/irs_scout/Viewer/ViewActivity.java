package com.stuin.irs_scout.Viewer;

import android.app.Activity;
import android.os.Bundle;
import com.stuin.irs_scout.R;

/**
 * Created by Stuart on 3/21/2017.
 */
public class ViewActivity extends Activity {
    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_view);
        getActionBar().hide();
    }
}