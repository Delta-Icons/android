package website.leifs.delta.applications;

import androidx.annotation.NonNull;
import candybar.lib.applications.CandyBarApplication;

public class CandyBar extends CandyBarApplication {

    @NonNull
    @Override
    public Configuration onInit() {

        Configuration configuration = new Configuration();

        configuration.setAutomaticIconsCountEnabled(false);
        configuration.setCustomIconsCount(7795);
        configuration.setDashboardThemingEnabled(false);
        configuration.setGenerateAppFilter(true);
        configuration.setGenerateAppMap(false);
        configuration.setGenerateThemeResources(true);
        configuration.setIncludeIconRequestToEmailBody(true);
        configuration.setShadowEnabled(false);
        configuration.setShowTabAllIcons(true);
        configuration.setTabAllIconsTitle("All");

        configuration.setCategoryForTabAllIcons(new String[] {
            "Google", "System", "Folders", "Calendar", "Alts", "#",
            "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M",
            "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"
        });

        return configuration;
    }
}
