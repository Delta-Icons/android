# Contributing
In case you want to contribute to Delta by providing icons please do so by creating a vector-based icon, cloning this repo and issuing a pull request with regards to these points:
- Vectors (SVG, EPS, PDF, ...) go to the `contributed-vectors` folder 
	-  Please keep filenames in lowercase alphabet with underscores
- 192 * 192 pixel PNG file `icon_name.png` goes to `app/src/main/res/drawable-nodpi`
- Name of the icon in these files, in this format `<item drawable="icon_name" />` (Add a duplicate line inside `New` Category)
	- `app/src/main/assets/drawable.xml` 
	- `app/src/main/res/xml/drawable.xml`
- ComponentInfo has to be in the following files according to their format (At the end preferably for readability purpose):
	- `app/src/main/assets/appfilter.xml`
	- `app/src/main/res/xml/appfilter.xml`
	- ~~`app/src/main/res/xml/appmap.xml`~~ - Dropped support as of March 2021
	- `app/src/main/res/xml/theme_resources.xml`
- Give yourself an entry at the bottom of `app/src/main/res/xml/contributors.xml`

## Resources for Contributions
Color palette
![Palette for Delta](https://github.com/Delta-Icons/android/raw/master/Palette.svg) (Right-Click &rarr; Save as)

![Adobe Swatch Exchange Palette](https://github.com/Delta-Icons/android/raw/master/Palette.ase) (Right-Click &rarr; Save as)

![GPL pallete](https://github.com/Delta-Icons/android/raw/master/Palette.gpl) (Inkscape, Karbon) (Right-Click &rarr; Save as)

Icon template
![Icon Template for Delta](https://github.com/Delta-Icons/android/raw/master/template.svg) (Right-Click &rarr; Save as)

Icon template tutorial
![Icon Template Tutorial for Delta](https://github.com/Delta-Icons/android/raw/master/template_tutorial.svg) (Right-Click &rarr; Save as)

Font: [Now](https://www.1001fonts.com/now-font.html) (Use Now Alt from the same family for alternate lowercase "a")

Gathering ComponentInfo from apps: [Icon Pusher](https://iconpusher.com/) by southpaw.dev
