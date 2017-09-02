<p align="center">
	<div style="text-align: center; margin: 120px 0">
	<img src="https://github.com/Delta-Icons/android/raw/master/delta-logo.png" alt="">
</div>
</p>

# Delta Icons
Matted out icon pack for custom Android launchers.

## Contributing
In case you want to contribute to Delta by providing icons please do so by creating a vector-based icon, cloning this repo and issuing a pull request with regards to these points:
- Vectors (SVG, EPS, PDF, ...) go to the `contributed-vectors` folder
- 192 * 192 pixel PNG file `icon_name.png` goes to `app/src/main/res/drawable-nodpi`
- Name of the icon in these files, in this format `<item drawable="icon_name" />`
	- `app/src/main/assets/drawable.xml` 
	- `app/src/main/res/xml/drawable.xml`
- ComponentInfo has to be in the following files according to their format:
	- `app/src/main/assets/appfilter.xml`
	- `app/src/main/res/xml/appfilter.xml`
	- `app/src/main/res/xml/appmap.xml`
	- `app/src/main/res/xml/theme_resources.xml`
- Give yourself an entry at the bottom of `app/src/main/res/xml/contributors.xml`

### Resources for Contributions
The color palette
![Palette for Delta](https://github.com/Delta-Icons/android/raw/master/palette.svg)

Icon template
![Icon Template for Delta](https://github.com/Delta-Icons/android/raw/master/template.svg)

Licensed under [Creative Commons Attribution-NonCommercial-NoDerivatives License 4.0](https://creativecommons.org/licenses/by-nc-nd/4.0/)