package website.leifs.delta.applications;

import androidx.annotation.NonNull;
import candybar.lib.applications.CandyBarApplication;
import website.leifs.delta.R;

public class CandyBar extends CandyBarApplication {

    @NonNull
    @Override
    public Class<?> getDrawableClass() {
        return R.drawable.class;
    }

    @NonNull
    @Override
    public Configuration onInit() {

        Configuration configuration = new Configuration();

        configuration.setAutomaticIconsCountEnabled(false);
        configuration.setCustomIconsCount(13235);
        configuration.setDashboardThemingEnabled(true);
        configuration.setGenerateAppFilter(true);
        configuration.setGenerateAppMap(false);
        configuration.setGenerateThemeResources(true);
        configuration.setIncludeIconRequestToEmailBody(true);
        configuration.setShadowEnabled(false);
        configuration.setShowTabAllIcons(true);
        configuration.setTabAllIconsTitle("All");
        configuration.setExcludedCategoryForSearch(new String[] {
            "New"
        });
        configuration.setCategoryForTabAllIcons(new String[] {
            "Google", "System", "Folders", "Calendar", "Alts", "#",
            "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M",
            "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"
        });

        configuration.setFilterRequestHandler((request) -> {
            String pkg = request.getPackageName();
            if (pkg == null) return true;
            return !(pkg.startsWith("org.chromium.webapk") || pkg.startsWith("com.sec.android.app.sbrowser.webapk"));
        });

        return configuration;
    }
}
