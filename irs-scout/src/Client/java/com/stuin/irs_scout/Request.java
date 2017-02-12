package com.stuin.irs_scout;

import android.content.Context;

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
    private Context context;

    Request(String url, Context context) {
        address = url;
        this.context = context;
    }

    List<String> get(String query) {
        Scanner scanner;
        if(false) scanner = http(query);
        else scanner = test(query);

        List<String> out = new ArrayList<>();
        while(scanner.hasNext()) out.add(scanner.nextLine());
        return out;
    }

    void post(String query, String value) {

    }

    private Scanner http(String query) {
        try {
            URL url = new URL(address + query);
            HttpURLConnection urlConnection = (HttpURLConnection) url.openConnection();
            try {
                InputStream in = new BufferedInputStream(urlConnection.getInputStream());
                return new Scanner(in);
            } finally {
                urlConnection.disconnect();
            }
        } catch(Exception e) {
            //No connection!!
        }
        return new Scanner("");
    }

    private Scanner test(String query) {
        if(query.equals("Game/layout")) return new Scanner(context.getResources().openRawResource(R.raw.layout));
        return new Scanner("");
    }
}
