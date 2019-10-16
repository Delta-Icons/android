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

        /*configuration.setWallpaperJsonStructure(
                new JsonStructure.Builder(null)   //-->  Array's Name
                        .name("name")             //-->  Wallpaper's Name
                        .author("author")         //-->  Author's Name
                        .url("url")               //-->  Wallpaper's URL
                        .thumbUrl("thumbUrl")     //-->  Wallpaper's Thumbnail's URL
                        .build());*/

        
        return configuration;
    }
}
