package com.stuin.irs_scout;

import android.app.Activity;
import android.os.AsyncTask;
import android.widget.RadioButton;

import java.io.BufferedInputStream;
import java.io.InputStream;
import java.net.HttpURLConnection;
import java.net.URL;
import java.util.ArrayList;
import java.util.List;
import java.util.Scanner;

/**
 * Created by Stuart on 2/11/2017.
 */
class Request {
    final private String address;
    private Next next;

    Request(String query, Next next) {
        address = "http://" + MainActivity.address + ":8080/";
        this.next = next;
        new serverRequest().execute(query);
    }

    private class serverRequest extends AsyncTask<String, String, List<String>> {
        @Override
        protected List<String> doInBackground(String ... params) {
            Scanner scanner = new Scanner("");
            if(true) {
                try {
                    URL url = new URL(address + params[0]);
                    HttpURLConnection urlConnection = (HttpURLConnection) url.openConnection();
                    try {
                        InputStream in = new BufferedInputStream(urlConnection.getInputStream());
                        scanner = new Scanner(in);
                    } finally {
                        urlConnection.disconnect();
                    }
                } catch(Exception e) {
                    //No connection
                }
            }

            List<String> out = new ArrayList<>();
            while(scanner.hasNext()) out.add(scanner.nextLine());
            return out;
        }

        @Override
        protected void onPostExecute(List<String> strings) {
            if(strings.isEmpty()) next.run(strings);
        }
    }
}
