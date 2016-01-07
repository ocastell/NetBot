package net.iesdeltebre.oscarcastellmarcos.netbot;

import android.content.Context;
import android.graphics.Color;
import android.graphics.PorterDuff;
import android.graphics.drawable.Drawable;
import android.net.wifi.WifiInfo;
import android.net.wifi.WifiManager;
import android.os.Bundle;
import android.os.CountDownTimer;
import android.support.design.widget.FloatingActionButton;
import android.support.design.widget.Snackbar;
import android.support.v4.content.ContextCompat;
import android.support.v7.app.AppCompatActivity;
import android.support.v7.widget.Toolbar;
import android.text.format.Formatter;
import android.util.Log;
import android.view.KeyEvent;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.view.inputmethod.EditorInfo;
import android.view.inputmethod.InputMethodManager;
import android.webkit.WebView;
import android.widget.EditText;
import android.widget.ImageButton;
import android.widget.ImageView;
import android.widget.LinearLayout;
import android.widget.RelativeLayout;
import android.widget.TableLayout;
import android.widget.TextView;

import java.io.IOException;
import java.io.PrintWriter;
import java.net.Socket;
import java.net.UnknownHostException;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

import static android.widget.Toast.LENGTH_LONG;
import static android.widget.Toast.makeText;

public class MainActivity extends AppCompatActivity {

    final int Port = 9001;
    final String VideoPort = "8081";
    final int VelocityChange = 200;
    final int RotationChange = 300;
    final String Clean_Command = "135";
    final String Spot_Command = "134";
    final String Dock_Command = "143";
    final String Safe_Command = "131";
    final String Drive_Command = "145";
    public static String velocity_rigth= "0";
    public static String velocity_left= "0";
    public static int velocity= 0;
    public static int rotation=0;
    public static Socket socket = null;
    public static PrintWriter out;

    @Override
    @SuppressWarnings("deprecation")
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        Toolbar toolbar = (Toolbar) findViewById(R.id.toolbar);
        setSupportActionBar(toolbar);

        // Layout definitions (ALL)
        final FloatingActionButton fab = (FloatingActionButton) findViewById(R.id.fab);
        final FloatingActionButton viewVideo = (FloatingActionButton) findViewById(R.id.viewVideo);
        final RelativeLayout layoutMain = (RelativeLayout) findViewById(R.id.layoutMain);
        final RelativeLayout layoutAboutUs = (RelativeLayout) findViewById(R.id.layoutAboutUs);
        final LinearLayout layoutButtons = (LinearLayout) findViewById(R.id.layoutButtons);
        final TableLayout layoutControls = (TableLayout) findViewById(R.id.layoutControls);
        // widgets definitions (All)
        final ImageButton btnConnect = (ImageButton) findViewById(R.id.btnConnect);
        final ImageButton btnDisconnect = (ImageButton) findViewById(R.id.btnDisconnect);
        final ImageButton btnRefresh = (ImageButton) findViewById(R.id.btnRefresh);
        final ImageButton btnAboutUs = (ImageButton) findViewById(R.id.btnAboutUs);
        final ImageButton btnClean = (ImageButton) findViewById(R.id.btnClean);
        final ImageButton btnSpot = (ImageButton) findViewById(R.id.btnSpot);
        final ImageButton btnDock = (ImageButton) findViewById(R.id.btnDock);
        final ImageButton btnArrowUp = (ImageButton) findViewById(R.id.btnArrowUp);
        final ImageButton btnArrowDown = (ImageButton) findViewById(R.id.btnArrowDown);
        final ImageButton btnArrowUpLeft = (ImageButton) findViewById(R.id.btnArrowUpLeft);
        final ImageButton btnArrowUpRigth = (ImageButton) findViewById(R.id.btnArrowUpRigth);
        final ImageButton btnArrowDownLeft = (ImageButton) findViewById(R.id.btnArrowDownLeft);
        final ImageButton btnArrowDownRight = (ImageButton) findViewById(R.id.btnArrowDownRight);
        final ImageButton btnStop = (ImageButton) findViewById(R.id.btnStop);
        final ImageButton btnSpinLeft = (ImageButton) findViewById(R.id.btnSpinLeft);
        final ImageButton btnSpinRight = (ImageButton) findViewById(R.id.btnSpinRight);
        final EditText txtIPConnect = (EditText) findViewById(R.id.txtIPConnect);
        final ImageView imgAboutUs = (ImageView) findViewById(R.id.imgAboutUs);
        final WebView NetBotView = (WebView) findViewById(R.id.NetBotView);

        NetBotView.loadUrl("file:///android_asset/videooff.png");
        layoutMain.setVisibility(View.VISIBLE);
        layoutAboutUs.setVisibility(View.INVISIBLE);
        imgAboutUs.setImageResource(getResources().getIdentifier("about_us_info", "drawable", getPackageName()));

        fab.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Snackbar.make(view, "Send e-mail to ocastell@mac.com", Snackbar.LENGTH_LONG)
                        .setAction("Action", null).show();
            }
        });
        viewVideo.setEnabled(false);
        viewVideo.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                final String IP_Server = txtIPConnect.getText().toString();
                String url = "http://" + IP_Server + ":" + VideoPort;
                NetBotView.loadUrl(url);
                makeText(getApplicationContext(), "Video from: " + url, LENGTH_LONG).show();
            }
        });
        viewVideo.setOnLongClickListener(new View.OnLongClickListener() {
            @Override
            public boolean onLongClick(View v) {
                NetBotView.loadUrl("file:///android_asset/videooff.png");
                makeText(getApplicationContext(), "Disabling Video ... " , LENGTH_LONG).show();
                return false;
            }
        });
        int iconResId = getResources().getIdentifier("connect" , "drawable", getPackageName());
        setImageButtonEnabled(MainActivity.this,false, btnConnect,iconResId);
        btnConnect.setOnClickListener(new View.OnClickListener() {
            // Connect with de Server Socket at IP_Server and port 9001
            public void onClick(View view) {
                final String IP_Server = txtIPConnect.getText().toString();
                //
                // Connect with Server & send String initial strings
                //
                connectToServer(IP_Server, Port);
                //
                // After connecting send de save command and Hello
                String message = "Hello";
                makeText(getApplicationContext(), "Sending: " + message,LENGTH_LONG).show();
                //
                // Disable txtIPConnect & btnConnect
                //
                int iconResId = getResources().getIdentifier("connect" , "drawable", getPackageName());
                setImageButtonEnabled(MainActivity.this,false, btnConnect,iconResId);
                txtIPConnect.setEnabled(false);
                //
                // Enable the rest of widgets (Good Luck!!!!)
                //
                viewVideo.setEnabled(true);
                iconResId = getResources().getIdentifier("disconnect" , "drawable", getPackageName());
                setImageButtonEnabled(MainActivity.this, true, btnDisconnect, iconResId);
                iconResId = getResources().getIdentifier("refresh" , "drawable", getPackageName());
                setImageButtonEnabled(MainActivity.this, true, btnRefresh, iconResId);
                iconResId = getResources().getIdentifier("about_us" , "drawable", getPackageName());
                setImageButtonEnabled(MainActivity.this, true, btnAboutUs, iconResId);
                iconResId = getResources().getIdentifier("clean" , "drawable", getPackageName());
                setImageButtonEnabled(MainActivity.this,true, btnClean,iconResId);
                iconResId = getResources().getIdentifier("spot" , "drawable", getPackageName());
                setImageButtonEnabled(MainActivity.this,true, btnSpot,iconResId);
                iconResId = getResources().getIdentifier("dock" , "drawable", getPackageName());
                setImageButtonEnabled(MainActivity.this,true, btnDock,iconResId);
                iconResId = getResources().getIdentifier("arrow_up" , "drawable", getPackageName());
                setImageButtonEnabled(MainActivity.this,true, btnArrowUp,iconResId);
                iconResId = getResources().getIdentifier("arrow_down" , "drawable", getPackageName());
                setImageButtonEnabled(MainActivity.this,true, btnArrowDown,iconResId);
                iconResId = getResources().getIdentifier("arrow_upleft" , "drawable", getPackageName());
                setImageButtonEnabled(MainActivity.this,true, btnArrowUpLeft,iconResId);
                iconResId = getResources().getIdentifier("arrow_upright" , "drawable", getPackageName());
                setImageButtonEnabled(MainActivity.this,true, btnArrowUpRigth,iconResId);
                iconResId = getResources().getIdentifier("arrow_downleft" , "drawable", getPackageName());
                setImageButtonEnabled(MainActivity.this,true, btnArrowDownLeft,iconResId);
                iconResId = getResources().getIdentifier("arrow_downright" , "drawable", getPackageName());
                setImageButtonEnabled(MainActivity.this,true, btnArrowDownRight,iconResId);
                iconResId = getResources().getIdentifier("stop" , "drawable", getPackageName());
                setImageButtonEnabled(MainActivity.this,true, btnStop,iconResId);
                iconResId = getResources().getIdentifier("arrowspinleft" , "drawable", getPackageName());
                setImageButtonEnabled(MainActivity.this,true, btnSpinLeft,iconResId);
                iconResId = getResources().getIdentifier("arrowspinright" , "drawable", getPackageName());
                setImageButtonEnabled(MainActivity.this,true, btnSpinRight,iconResId);
            }
        });

        iconResId = getResources().getIdentifier("disconnect" , "drawable", getPackageName());
        setImageButtonEnabled(MainActivity.this, false, btnDisconnect, iconResId);
        btnDisconnect.setOnClickListener(new View.OnClickListener() {
            public void onClick(View view) {

                disConnecttoServer();
                //
                // Enable txtIPConnect & btnConnect
                //
                int iconResId = getResources().getIdentifier("connect" , "drawable", getPackageName());
                setImageButtonEnabled(MainActivity.this,true, btnConnect,iconResId);
                txtIPConnect.setEnabled(true);
                NetBotView.loadUrl("file:///android_asset/videooff.png");
                //
                // Disable the rest of widgets (Good Luck!!!!)
                //
                viewVideo.setEnabled(false);
                iconResId = getResources().getIdentifier("disconnect" , "drawable", getPackageName());
                setImageButtonEnabled(MainActivity.this, false, btnDisconnect, iconResId);
                iconResId = getResources().getIdentifier("refresh" , "drawable", getPackageName());
                setImageButtonEnabled(MainActivity.this, false, btnRefresh, iconResId);
                iconResId = getResources().getIdentifier("about_us" , "drawable", getPackageName());
                setImageButtonEnabled(MainActivity.this, false, btnAboutUs, iconResId);
                iconResId = getResources().getIdentifier("clean" , "drawable", getPackageName());
                setImageButtonEnabled(MainActivity.this,false, btnClean,iconResId);
                iconResId = getResources().getIdentifier("spot" , "drawable", getPackageName());
                setImageButtonEnabled(MainActivity.this,false, btnSpot,iconResId);
                iconResId = getResources().getIdentifier("dock" , "drawable", getPackageName());
                setImageButtonEnabled(MainActivity.this,false, btnDock,iconResId);
                iconResId = getResources().getIdentifier("arrow_up" , "drawable", getPackageName());
                setImageButtonEnabled(MainActivity.this,false, btnArrowUp,iconResId);
                iconResId = getResources().getIdentifier("arrow_down" , "drawable", getPackageName());
                setImageButtonEnabled(MainActivity.this,false, btnArrowDown,iconResId);
                iconResId = getResources().getIdentifier("arrow_upleft" , "drawable", getPackageName());
                setImageButtonEnabled(MainActivity.this,false, btnArrowUpLeft,iconResId);
                iconResId = getResources().getIdentifier("arrow_upright" , "drawable", getPackageName());
                setImageButtonEnabled(MainActivity.this,false, btnArrowUpRigth,iconResId);
                iconResId = getResources().getIdentifier("arrow_downleft" , "drawable", getPackageName());
                setImageButtonEnabled(MainActivity.this,false, btnArrowDownLeft,iconResId);
                iconResId = getResources().getIdentifier("arrow_downright" , "drawable", getPackageName());
                setImageButtonEnabled(MainActivity.this,false, btnArrowDownRight,iconResId);
                iconResId = getResources().getIdentifier("stop" , "drawable", getPackageName());
                setImageButtonEnabled(MainActivity.this,false, btnStop,iconResId);
                iconResId = getResources().getIdentifier("arrowspinleft" , "drawable", getPackageName());
                setImageButtonEnabled(MainActivity.this,false, btnSpinLeft,iconResId);
                iconResId = getResources().getIdentifier("arrowspinright" , "drawable", getPackageName());
                setImageButtonEnabled(MainActivity.this,false, btnSpinRight,iconResId);
                makeText(getApplicationContext(), "Disconnecting ... " ,LENGTH_LONG).show();
            }
        });
        iconResId = getResources().getIdentifier("refresh" , "drawable", getPackageName());
        setImageButtonEnabled(MainActivity.this, false, btnRefresh, iconResId);
        btnRefresh.setOnClickListener(new View.OnClickListener() {
            public void onClick(View view) {
                final String IP_Server = txtIPConnect.getText().toString();
                sendMessagetoServer(Safe_Command);
                makeText(getApplicationContext(), "Sending: " + Safe_Command,LENGTH_LONG).show();
            }
        });
        iconResId = getResources().getIdentifier("about_us" , "drawable", getPackageName());
        setImageButtonEnabled(MainActivity.this, false, btnAboutUs, iconResId);
        btnAboutUs.setOnClickListener(new View.OnClickListener() {
            public void onClick(View view) {
                new CountDownTimer(5000, 1000) {
                    public void onTick(long millisUntilFinished) {
                        layoutAboutUs.setVisibility(View.VISIBLE);
                     }
                    public void onFinish() {
                        layoutAboutUs.setVisibility(View.INVISIBLE);
                    }
                }.start();
            }
        });
        iconResId = getResources().getIdentifier("clean" , "drawable", getPackageName());
        setImageButtonEnabled(MainActivity.this,false, btnClean,iconResId);
        btnClean.setOnClickListener(new View.OnClickListener() {
            public void onClick(View view) {
                final String IP_Server = txtIPConnect.getText().toString();
                sendMessagetoServer(Clean_Command);
                makeText(getApplicationContext(), "Sending: " + Clean_Command,LENGTH_LONG).show();
            }
        });
        iconResId = getResources().getIdentifier("spot" , "drawable", getPackageName());
        setImageButtonEnabled(MainActivity.this,false, btnSpot,iconResId);
        btnSpot.setOnClickListener(new View.OnClickListener() {
            public void onClick(View view) {
                final String IP_Server = txtIPConnect.getText().toString();
                sendMessagetoServer(Spot_Command);
                makeText(getApplicationContext(), "Sending: " + Spot_Command,LENGTH_LONG).show();
            }
        });
        iconResId = getResources().getIdentifier("dock" , "drawable", getPackageName());
        setImageButtonEnabled(MainActivity.this,false, btnDock,iconResId);
        btnDock.setOnClickListener(new View.OnClickListener() {
            public void onClick(View view) {
                final String IP_Server = txtIPConnect.getText().toString();
                sendMessagetoServer(Dock_Command);
                makeText(getApplicationContext(), "Sending: " + Dock_Command,LENGTH_LONG).show();
            }
        });
        iconResId = getResources().getIdentifier("arrow_up" , "drawable", getPackageName());
        setImageButtonEnabled(MainActivity.this,false, btnArrowUp,iconResId);
        btnArrowUp.setOnClickListener(new View.OnClickListener() {
            public void onClick(View view) {
                int vel[];
                velocity=0;
                velocity += VelocityChange;
                rotation=0;
                vel=Velocity(velocity,rotation);
                velocity_rigth=String.valueOf(vel[0]);
                velocity_left=String.valueOf(vel[1]);
                final String IP_Server = txtIPConnect.getText().toString();
                String message=Drive_Command+" "+velocity_rigth+" "+velocity_left;
                sendMessagetoServer(message);
                makeText(getApplicationContext(), "Sending: " + message,LENGTH_LONG).show();
            }
        });
        iconResId = getResources().getIdentifier("arrow_down" , "drawable", getPackageName());
        setImageButtonEnabled(MainActivity.this,false, btnArrowDown,iconResId);
        btnArrowDown.setOnClickListener(new View.OnClickListener() {
            public void onClick(View view) {
                int vel[];
                velocity=0;
                velocity -= VelocityChange;
                rotation=0;
                vel=Velocity(velocity,rotation);
                velocity_rigth=String.valueOf(vel[0]);
                velocity_left=String.valueOf(vel[1]);
                final String IP_Server = txtIPConnect.getText().toString();
                String message=Drive_Command+" "+velocity_rigth+" "+velocity_left;
                sendMessagetoServer(message);
                makeText(getApplicationContext(), "Sending: " + message,LENGTH_LONG).show();
            }
        });
        iconResId = getResources().getIdentifier("arrow_upleft" , "drawable", getPackageName());
        setImageButtonEnabled(MainActivity.this,false, btnArrowUpLeft,iconResId);
        btnArrowUpLeft.setOnClickListener(new View.OnClickListener() {
            public void onClick(View view) {
                int vel[];
                velocity=0;
                velocity += VelocityChange;
                rotation=0;
                rotation += RotationChange/2;
                vel=Velocity(velocity,rotation);
                velocity_rigth=String.valueOf(vel[0]);
                velocity_left=String.valueOf(vel[1]);
                final String IP_Server = txtIPConnect.getText().toString();
                String message=Drive_Command+" "+velocity_rigth+" "+velocity_left;
                sendMessagetoServer(message);
                makeText(getApplicationContext(), "Sending: " + message,LENGTH_LONG).show();
            }
        });
        iconResId = getResources().getIdentifier("arrow_upright" , "drawable", getPackageName());
        setImageButtonEnabled(MainActivity.this,false, btnArrowUpRigth,iconResId);
        btnArrowUpRigth.setOnClickListener(new View.OnClickListener() {
            public void onClick(View view) {
                int vel[];
                velocity=0;
                velocity += VelocityChange;
                rotation=0;
                rotation -= RotationChange/2;
                vel=Velocity(velocity,rotation);
                velocity_rigth=String.valueOf(vel[0]);
                velocity_left=String.valueOf(vel[1]);
                final String IP_Server = txtIPConnect.getText().toString();
                String message=Drive_Command+" "+velocity_rigth+" "+velocity_left;
                sendMessagetoServer(message);
                makeText(getApplicationContext(), "Sending: " + message,LENGTH_LONG).show();
            }
        });
        iconResId = getResources().getIdentifier("arrow_downleft" , "drawable", getPackageName());
        setImageButtonEnabled(MainActivity.this,false, btnArrowDownLeft,iconResId);
        btnArrowDownLeft.setOnClickListener(new View.OnClickListener() {
            public void onClick(View view) {
                int vel[];
                velocity=0;
                velocity -= VelocityChange;
                rotation=0;
                rotation -= RotationChange/2;
                vel=Velocity(velocity,rotation);
                velocity_rigth=String.valueOf(vel[0]);
                velocity_left=String.valueOf(vel[1]);
                final String IP_Server = txtIPConnect.getText().toString();
                String message=Drive_Command+" "+velocity_rigth+" "+velocity_left;
                sendMessagetoServer(message);
                makeText(getApplicationContext(), "Sending: " + message,LENGTH_LONG).show();
            }
        });
        iconResId = getResources().getIdentifier("arrow_downright" , "drawable", getPackageName());
        setImageButtonEnabled(MainActivity.this,false, btnArrowDownRight,iconResId);
        btnArrowDownRight.setOnClickListener(new View.OnClickListener() {
            public void onClick(View view) {
                int vel[];
                velocity=0;
                velocity -= VelocityChange;
                rotation=0;
                rotation += RotationChange/2;
                vel=Velocity(velocity,rotation);
                velocity_rigth=String.valueOf(vel[0]);
                velocity_left=String.valueOf(vel[1]);
                final String IP_Server = txtIPConnect.getText().toString();
                String message=Drive_Command+" "+velocity_rigth+" "+velocity_left;
                sendMessagetoServer(message);
                makeText(getApplicationContext(), "Sending: " + message,LENGTH_LONG).show();
            }
        });
        iconResId = getResources().getIdentifier("stop" , "drawable", getPackageName());
        setImageButtonEnabled(MainActivity.this,false, btnStop,iconResId);
        btnStop.setOnClickListener(new View.OnClickListener() {
            public void onClick(View view) {
                int vel[];
                velocity=0;
                rotation=0;
                vel=Velocity(velocity,rotation);
                velocity_rigth=String.valueOf(vel[0]);
                velocity_left=String.valueOf(vel[1]);
                final String IP_Server = txtIPConnect.getText().toString();
                String message=Drive_Command+" "+velocity_rigth+" "+velocity_left;
                sendMessagetoServer(message);
                makeText(getApplicationContext(), "Sending: " + message,LENGTH_LONG).show();
            }
        });
        iconResId = getResources().getIdentifier("arrowspinleft" , "drawable", getPackageName());
        setImageButtonEnabled(MainActivity.this,false, btnSpinLeft,iconResId);
        btnSpinLeft.setOnClickListener(new View.OnClickListener() {
            public void onClick(View view) {
                int vel[];
                velocity=0;
                rotation=0;
                rotation += RotationChange;
                vel=Velocity(velocity,rotation);
                velocity_rigth=String.valueOf(vel[0]);
                velocity_left=String.valueOf(vel[1]);
                final String IP_Server = txtIPConnect.getText().toString();
                String message=Drive_Command+" "+velocity_rigth+" "+velocity_left;
                sendMessagetoServer(message);
                makeText(getApplicationContext(), "Sending: " + message,LENGTH_LONG).show();
            }
        });
        iconResId = getResources().getIdentifier("arrowspinright" , "drawable", getPackageName());
        setImageButtonEnabled(MainActivity.this,false, btnSpinRight,iconResId);
        btnSpinRight.setOnClickListener(new View.OnClickListener() {
            public void onClick(View view) {
                int vel[];
                velocity=0;
                rotation=0;
                rotation -= RotationChange;
                vel=Velocity(velocity,rotation);
                velocity_rigth=String.valueOf(vel[0]);
                velocity_left=String.valueOf(vel[1]);
                final String IP_Server = txtIPConnect.getText().toString();
                String message=Drive_Command+" "+velocity_rigth+" "+velocity_left;
                sendMessagetoServer(message);
                makeText(getApplicationContext(), "Sending: " + message,LENGTH_LONG).show();
            }
        });

        txtIPConnect.setSelectAllOnFocus(true);

        txtIPConnect.setOnEditorActionListener(new TextView.OnEditorActionListener() {
            @Override
            public boolean onEditorAction(TextView v, int actionId, KeyEvent event) {
                WifiManager wifiMgr = (WifiManager) getSystemService(WIFI_SERVICE);
                WifiInfo wifiInfo = wifiMgr.getConnectionInfo();
                int ip = wifiInfo.getIpAddress();
                String IP_Local = Formatter.formatIpAddress(ip);
                if (actionId == EditorInfo.IME_ACTION_DONE) {
                    String IP_Server = txtIPConnect.getText().toString();
                    if (IP_Server.length() == 0) {
                        txtIPConnect.setError( "IP of the Server Socket is required!" );
                    }
                    if (isValidIP(IP_Server)) {
                        InputMethodManager imm = (InputMethodManager) getSystemService(Context.INPUT_METHOD_SERVICE);
                        imm.hideSoftInputFromWindow(txtIPConnect.getWindowToken(), 0);
                        makeText(getApplicationContext(), "The IP of the ServerSocket is: " + IP_Server + " local IP: " + IP_Local,
                                LENGTH_LONG).show();
                        int iconResId = getResources().getIdentifier("connect", "drawable", getPackageName());
                        setImageButtonEnabled(getApplicationContext(), true, btnConnect, iconResId);
                    } else {
                        txtIPConnect.setError( "The IP of the Server Socket is not correct!");
                    }
                    return true;
                }
                return false;
            }
        });
    }

    public int[] Velocity(int vel, int rot) {
        int velocity[] = new int[2];
        velocity[0]=vel+(rot/2);
        velocity[1]=vel-(rot/2);
        return velocity;
    }

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        // Inflate the menu; this adds items to the action bar if it is present.
        getMenuInflater().inflate(R.menu.menu_main, menu);
        return true;
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        // Handle action bar item clicks here. The action bar will
        // automatically handle clicks on the Home/Up button, so long
        // as you specify a parent activity in AndroidManifest.xml.
        int id = item.getItemId();

        //noinspection SimplifiableIfStatement
        if (id == R.id.action_settings) {
            return true;
        }

        return super.onOptionsItemSelected(item);
    }

    /**
     * @param ip the ip
     * @return check if the ip is valid ipv4
     */
    @SuppressWarnings("deprecation")
    private static final String PATTERN =
            "^([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\." +
                    "([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\." +
                    "([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\." +
                    "([01]?\\d\\d?|2[0-4]\\d|25[0-5])$";
    public static boolean isValidIP(final String ip){
        Pattern pattern = Pattern.compile(PATTERN);
        Matcher matcher = pattern.matcher(ip);
        return matcher.matches();
    }
    /**
     * Sets the image button to the given state and grays-out the icon.
     *
     * @param enabled The state of the button
     * @param item The button item to modify
     * @param iconResId The button's icon ID
     */
    public static void setImageButtonEnabled(Context context, boolean enabled,
                                             ImageButton item, int iconResId) {

        item.setEnabled(enabled);
        Drawable originalIcon = ContextCompat.getDrawable(context, iconResId);
        Drawable icon = enabled ? originalIcon : convertDrawableToGrayScale(originalIcon);
        item.setImageDrawable(icon);
    }

    /**
     * Mutates and applies a filter that converts the given drawable to a Gray
     * image. This method may be used to simulate the color of disable icons in
     * Honeycomb's ActionBar.
     *
     * @return a mutated version of the given drawable with a color filter applied.
     */
    public static Drawable convertDrawableToGrayScale(Drawable drawable) {
        if (drawable == null)
            return null;

        Drawable res = drawable.mutate();
        //res.setColorFilter(Color.parseColor("#B7B2B0"), PorterDuff.Mode.MULTIPLY);
        res.setColorFilter(Color.GRAY, PorterDuff.Mode.MULTIPLY);
        return res;
    }

    public void connectToServer(final String dstAdress, final int Port) {

        new Thread(new Runnable() {

            @Override
            public void run() {

                try {
                    socket = new Socket(dstAdress, Port);
                    out = new PrintWriter(socket.getOutputStream());

                    // After connecting send de save command and Hello
                    sendMessagetoServer(Safe_Command);
                    String message = "Hello";
                    sendMessagetoServer(message);

                } catch (UnknownHostException e) {
                    // TODO Auto-generated catch block
                    e.printStackTrace();
                    Log.d("", "Error: UnknownHostException");
                } catch (IOException e) {
                    // TODO Auto-generated catch block
                    e.printStackTrace();
                    Log.d("", "Error: IOException");
                }
            }
        }).start();
    }
    public void sendMessagetoServer(final String str) {
        try {
            out = new PrintWriter(socket.getOutputStream());
            out.println(str);
            out.flush();
        } catch (UnknownHostException e) {
            // TODO Auto-generated catch block
            e.printStackTrace();
            Log.d("", "Error sending: "+str);
        } catch (IOException e) {
            // TODO Auto-generated catch block
            e.printStackTrace();
            Log.d("", "Error sending: "+str);
        }
    }
    public void disConnecttoServer() {
        try {
            out = new PrintWriter(socket.getOutputStream());
            out.println("Bye, bye ...");
            out.flush();
            socket.close();
        } catch (UnknownHostException e) {
            // TODO Auto-generated catch block
            e.printStackTrace();
            Log.d("", "Error in: Bye, bye ...");
        } catch (IOException e) {
            // TODO Auto-generated catch block
            e.printStackTrace();
            Log.d("", "Error in: Bye, bye ...");
        }
    }
}

