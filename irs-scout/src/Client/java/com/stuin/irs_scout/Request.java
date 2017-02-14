package com.stuin.irs_scout;

import android.os.AsyncTask;

import java.io.BufferedInputStream;
import java.io.BufferedReader;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;
import java.util.ArrayList;
import java.util.List;
import java.util.Scanner;

/**
 * Created by Stuart on 2/11/2017.
 */
class Request {
    private Next next;

    Request(String query, Next next) {
        this.next = next;
        new serverRequest().execute(query, "http://" + MainActivity.address + ":8080");
    }

    private class serverRequest extends AsyncTask<String, String, List<String>> {
        @Override
        protected List<String> doInBackground(String ... params) {
            BufferedReader reader;
            List<String> out = new ArrayList<>();
            if(true) {
                try {
                    URL url = new URL(params[1] + params[0]);
                    HttpURLConnection connection = (HttpURLConnection) url.openConnection();

                    try {
                        reader = new BufferedReader(new InputStreamReader(connection.getInputStream()));
                        String s = reader.readLine();
                        while(s != null) {
                            out.add(s);
                            s = reader.readLine();
                        }
                    } finally {
                        connection.disconnect();
                    }
                    return out;
                } catch(Exception e) {
                    //No connection
                    e.toString();
                }
            }
            return out;
        }

        @Override
        protected void onPostExecute(List<String> strings) {
            if(!strings.isEmpty()) next.run(strings);
        }
    }
}
