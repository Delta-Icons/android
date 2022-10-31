# Contributing

In case you want to contribute to Delta by providing icons please do so by creating a vector-based icon, cloning this repo and issuing a pull request with regards to these points:

- Vectors (SVG, EPS, PDF, …) go to the [contributed-vectors](https://github.com/Delta-Icons/android/tree/master/contributed-vectors) folder (_please keep filenames in lowercase alphabet with underscores!_)

- 192×192 pixel PNG file `icon_name.png` goes to [app/src/main/res/drawable-nodpi](https://github.com/Delta-Icons/android/tree/master/app/src/main/res/drawable-nodpi)

- Name of the icon in these files, in this format `<item drawable="icon_name" />` in its respective category as well as a duplicate line inside `New` category to show latest icons to users:
	- [app/src/main/assets/drawable.xml](https://github.com/Delta-Icons/android/tree/master/app/src/main/assets/drawable.xml)
	- [app/src/main/res/xml/drawable.xml](https://github.com/Delta-Icons/android/tree/master/app/src/main/res/xml/drawable.xml)

- ComponentInfo has to be in the following files according to their format (at the end preferably for readability purpose):
	- [app/src/main/assets/appfilter.xml](https://github.com/Delta-Icons/android/tree/master/app/src/main/assets/appfilter.xml)
	- [app/src/main/res/xml/appfilter.xml](https://github.com/Delta-Icons/android/tree/master/app/src/main/res/xml/appfilter.xml)
	- ~~[app/src/main/res/xml/appmap.xml](https://github.com/Delta-Icons/android/tree/master/app/src/main/res/xml/appmap.xml)~~ (dropped support as of March 2021)
	- ~~[app/src/main/res/xml/theme_resources.xml](https://github.com/Delta-Icons/android/tree/master/app/src/main/res/xml/theme_resources.xml)~~ (dropped support as of July 2022)

- Give yourself an entry at the bottom of [app/src/main/res/xml/contributors.xml](https://github.com/Delta-Icons/android/tree/master/app/src/main/res/xml/contributors.xml)

# Resources

> _For saving templates/palettes locally do: **Right-Click** &rarr; **Save As**_

## Colors

### Notes

- Davy's grey ( ${\color{#56595B}▉}$ `#56595B` ) as default Black

- Coral pink ( ${\color{#FF837D}▉}$ `#FF837D` ) as default Red and Fuzzy Wuzzy  ( ${\color{#BA6561}▉}$ `#BA6561` ) as default Dark Red. Shades of Red are specifically for shading purposes

- Transparencies — White (25%, 50%, 70%) and Black (15%, 25%) can be used as overlay for additional shading

### Palette

![Delta Palette](https://github.com/Delta-Icons/android/raw/master/resources/Palette.svg)

### Misc

- [Adobe Swatch Exchange Palette](https://github.com/Delta-Icons/android/raw/master/resources/Palette.ase) (Illustrator, Photoshop)

- [GPL Pallete](https://github.com/Delta-Icons/android/raw/master/resources/Palette.gpl) (Inkscape, Karbon)

## Icon Template

|<img src="https://github.com/Delta-Icons/android/raw/master/resources/template.svg" width="177" height="177">|<img src="https://github.com/Delta-Icons/android/raw/master/resources/template_tutorial.svg" width="547,705" height="600">|
|---|---|

## Font

- [Now Font](https://www.1001fonts.com/now-font.html?text=Delta%20Icons) (_use Now Alt from the same family for alternate lowercase 'a' letter_)

## Gathering ComponentInfo from Apps

- [Icon Pusher](https://iconpusher.com/) by [Southpaw](https://southpaw.dev)

- [Icon Request](https://github.com/Kaiserdragon2/IconRequest/releases) by [Kaiserdragon2](https://github.com/Kaiserdragon2)
