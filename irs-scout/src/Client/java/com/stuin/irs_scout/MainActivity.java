package com.stuin.irs_scout;

import android.app.Activity;
import android.os.Bundle;
import android.view.View;
import android.widget.FrameLayout;
import android.widget.TextView;


public class MainActivity extends Activity {
    private PageManager form;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        //Start app
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        getActionBar().hide();
    }

    public void position(View view) {
        //Get tablet position
        TextView textView = (TextView) view;
        String position = textView.getText().toString();

        //Get server address
        textView = (TextView) findViewById(R.id.AddressBar);
        Request request = new Request(textView.getText().toString(), this);

        //Hide start screen
        textView.setVisibility(View.GONE);
        findViewById(R.id.gridLayout).setVisibility(View.GONE);

        //Start
        form = new PageManager(this, request, position);
        FrameLayout frameLayout = (FrameLayout) findViewById(R.id.Frame);
        frameLayout.setVisibility(View.VISIBLE);
        frameLayout.addView(form);
    }

    @Override
    public void onBackPressed() {

    }

    public void nextPage(View view) {
        //Next page button
        form.nextPage(view);
    }

    public void lastPage(View view) {
        //Previous page button
        form.lastPage(view);
    }
}
