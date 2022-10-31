# Contributing
In case you want to contribute to Delta by providing icons please do so by creating a vector-based icon, cloning this repo and issuing a pull request with regards to these points:
- Vectors (SVG, EPS, PDF, ...) go to the `contributed-vectors` folder 
	-  Please keep filenames in lowercase alphabet with underscores
- 192 * 192 pixel PNG file `icon_name.png` goes to `app/src/main/res/drawable-nodpi`
- Name of the icon in these files, in this format `<item drawable="icon_name" />` in its respective category as well as a duplicate line inside `New` Category to show latest icons to users:
	- `app/src/main/assets/drawable.xml` 
	- `app/src/main/res/xml/drawable.xml`
- ComponentInfo has to be in the following files according to their format (At the end preferably for readability purpose):
	- `app/src/main/assets/appfilter.xml`
	- `app/src/main/res/xml/appfilter.xml`
	- ~~`app/src/main/res/xml/appmap.xml`~~ - Dropped support as of March 2021
	- ~~`app/src/main/res/xml/theme_resources.xml`~~ - Dropped support as of July 2022
- Give yourself an entry at the bottom of `app/src/main/res/xml/contributors.xml`

## Resources for Contributions
### Color palette
Usage notes:
- Davy's grey (#56595B) as default Black
- Coral pink (#FF837D) as default Red and Fuzzy Wuzzy (#BA6561) as default Dark Red. Shades of Red are specifically for shading purposes
- Transparencies - White (25%, 50%, 70%) and Black (15%, 25%) can be used as overlay for additional shading

![Palette for Delta](https://github.com/Delta-Icons/android/raw/master/resources/Palette.svg) (Right-Click &rarr; Save as)

[Adobe Swatch Exchange Palette](https://github.com/Delta-Icons/android/raw/master/resources/Palette.ase) (Right-Click &rarr; Save as)

[GPL pallete](https://github.com/Delta-Icons/android/raw/master/resources/Palette.gpl) (Inkscape, Karbon) (Right-Click &rarr; Save as)

### Icon template
<img src="https://github.com/Delta-Icons/android/raw/master/resources/template.svg" width="177" height="177">
(Right-Click &rarr; Save as)

### Icon template tutorial
<img src="https://github.com/Delta-Icons/android/raw/master/resources/template_tutorial.svg" width="547,705" height="600">
(Right-Click &rarr; Save as)

### Font
[Now](https://www.1001fonts.com/now-font.html) (Use Now Alt from the same family for alternate lowercase "a")

### Gathering ComponentInfo from apps
- [Icon Pusher](https://iconpusher.com/) by southpaw.dev
- [Icon Request](https://github.com/Kaiserdragon2/IconRequest/releases) by [Kaiserdragon2](https://github.com/Kaiserdragon2)
