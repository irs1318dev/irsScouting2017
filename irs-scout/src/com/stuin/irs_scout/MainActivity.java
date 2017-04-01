package com.stuin.irs_scout;

import android.app.Activity;
import android.content.Context;
import android.content.Intent;
import android.content.SharedPreferences;
import android.net.Uri;
import android.os.Bundle;
import android.view.View;
import android.widget.TextView;
import com.stuin.irs_scout.Scouter.PageManager;
import com.stuin.cleanvisuals.Request;

import java.util.List;


public class MainActivity extends Activity {
    private PageManager form;

    public static String position;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        //Start app
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        getActionBar().hide();

        //Retrieve last ip
        Request.address = getPreferences(Context.MODE_PRIVATE).getString("Address", getResources().getString(R.string.form_ip));
        TextView textView = (TextView) findViewById(R.id.AddressBar);
        textView.setText(Request.address);
    }

    public void position(View view) {
        //Get tablet position
        TextView textView = (TextView) view;
        position = textView.getText().toString();

        //Get server address
        textView = (TextView) findViewById(R.id.AddressBar);
        Request.address = textView.getText().toString();

        //Check connection
        class Connected extends Request {
            public void run(List<String> s) {
                connected();
            }
        }
        new Connected().start("");
    }

    private void connected() {
        //Save correct address
        SharedPreferences.Editor editor = getPreferences(Context.MODE_PRIVATE).edit();
        editor.putString("Address", Request.address);
        editor.apply();

        //Hide start screen
        findViewById(R.id.AddressBar).setVisibility(View.GONE);
        findViewById(R.id.gridLayout).setVisibility(View.GONE);
        findViewById(R.id.PageStatus).setVisibility(View.VISIBLE);

        //Start
        form = (PageManager) findViewById(R.id.Form);
        form.start(this);
    }

    @Override
    public void onBackPressed() {

    }

    public void status(View view) {
        form.updater.setStatus();
    }

    public void nextPage(View view) {
        //Next phase button
        form.nextPage(view);
    }

    public void lastPage(View view) {
        //Previous phase button
        form.lastPage(view);
    }

    public void site(View view) {
        Uri url = Uri.parse("http://" + Request.address + ":8080/");
        Intent launchBrowser = new Intent(Intent.ACTION_VIEW, url);
        startActivity(launchBrowser);
    }
}