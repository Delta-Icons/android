package website.leifs.delta.applications;

import androidx.annotation.NonNull;

// TODO: Remove `//` below to enable OneSignal
//import com.onesignal.OneSignal;

import candybar.lib.applications.CandyBarApplication;

public class CandyBar extends CandyBarApplication {

    // TODO: Remove `/*` and `*/` below to enable OneSignal
    /*
    @Override
    public void onCreate() {
        super.onCreate();

        // OneSignal Initialization
        OneSignal.initWithContext(this);
        OneSignal.setAppId("YOUR_ONESIGNAL_APP_ID_HERE");
    }
     */

    @NonNull
    @Override
    public Configuration onInit() {
        //Sample configuration
        Configuration configuration = new Configuration();

        configuration.setGenerateAppFilter(true);
        configuration.setGenerateAppMap(false);
        configuration.setGenerateThemeResources(true);
        configuration.setIncludeIconRequestToEmailBody(true);
        configuration.setShowTabAllIcons(true);
        configuration.setShadowEnabled(false);
        configuration.setDashboardThemingEnabled(false);
        configuration.setCategoryForTabAllIcons(new String[] {
                "Google", "System", "Folders", "Calendar", "Alts", "#", "A", "B", "C", "D", "E", "F", "G", "H", "I",
                "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"
        });

        return configuration;
    }
}
