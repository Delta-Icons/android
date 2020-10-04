package website.leifs.delta.applications;


import androidx.annotation.NonNull;
import candybar.lib.utils.JsonStructure;

// Remove '//' below to Enable OneSignal
//import com.onesignal.OneSignal;

import candybar.lib.applications.CandyBarApplication;

public class CandyBar extends CandyBarApplication {
    
    @NonNull
    @Override
    public Configuration onInit() {
        //Sample configuration
        Configuration configuration = new Configuration();

        configuration.setGenerateAppFilter(true);
        configuration.setIncludeIconRequestToEmailBody(true);
        configuration.setShowTabAllIcons(true);
        configuration.setShadowEnabled(false);
        configuration.setDashboardThemingEnabled(false);

        
        return configuration;
    }
}
