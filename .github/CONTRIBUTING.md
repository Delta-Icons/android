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

#### SVG

![Delta Palette](https://github.com/Delta-Icons/android/raw/master/resources/Palette.svg)

#### HTML

> _For quick reference without transparencies_

<table>
  <thead>
    <tr>
    <th>Greys</th>
    <th>Basic Colors / Shades</th>
    <th>Shades of Red</th>
    <th>Lighter Skintones</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td valign="top">
        ${\color{#FFFFFF}▉}$ <code>#FFFFFF</code> <i>White</i><br>
        ${\color{#ECECEC}▉}$ <code>#ECECEC</code> <i>Isabelline</i><br>
        ${\color{#D8D8D8}▉}$ <code>#D8D8D8</code> <i>Timberwolf</i><br>
        ${\color{#D2D2D2}▉}$ <code>#D2D2D2</code> <i>Light gray</i><br>
        ${\color{#CCCCCC}▉}$ <code>#CCCCCC</code> <i>Pastel gray</i><br>
        ${\color{#B1B5BD}▉}$ <code>#B1B5BD</code> <i>Ash grey</i><br>
        ${\color{#A0A5AF}▉}$ <code>#A0A5AF</code> <i>Dark gray</i><br>
        ${\color{#979797}▉}$ <code>#979797</code> <i>Manatee</i><br>
        ${\color{#83868C}▉}$ <code>#83868C</code> <i>Taupe gray</i><br>
        ${\color{#56595B}▉}$ <code>#56595B</code> <i>Davy's grey</i><br>
        ${\color{#4A4A4A}▉}$ <code>#4A4A4A</code> <i>Quartz</i><br>
        ${\color{#000000}▉}$ <code>#000000</code> <i>Black</i><br>
      </td>
      <td valign="top">
        ${\color{#FFD6D4}▉}$ <code>#FFD6D4</code> <i>Pastel pink</i><br>
        ${\color{#FF837D}▉}$ <code>#FF837D</code> <i>Coral pink</i><br>
        ${\color{#BA6561}▉}$ <code>#BA6561</code> <i>Fuzzy Wuzzy</i><br>
        ${\color{#D3B69A}▉}$ <code>#D3B69A</code> <i>Tan</i><br>
        ${\color{#8E6F60}▉}$ <code>#8E6F60</code> <i>Shadow</i><br>
        ${\color{#FCECDC}▉}$ <code>#FCECDC</code> <i>Antique white</i><br>
        ${\color{#F8C18C}▉}$ <code>#F8C18C</code> <i>Pale gold</i><br>
        ${\color{#FDF5D9}▉}$ <code>#FDF5D9</code> <i>Cornsilk</i><br>
        ${\color{#F9DE81}▉}$ <code>#F9DE81</code> <i>Jasmine</i><br>
        ${\color{#C39A54}▉}$ <code>#C39A54</code> <i>Camel</i><br>
        ${\color{#E0F4E0}▉}$ <code>#E0F4E0</code> <i>Platinum</i><br>
        ${\color{#98DC9A}▉}$ <code>#98DC9A</code> <i>Granny Smith Apple</i><br>
        ${\color{#71A372}▉}$ <code>#71A372</code> <i>Asparagus</i><br>
        ${\color{#96DFD3}▉}$ <code>#96DFD3</code> <i>Pale robin egg blue</i><br>
        ${\color{#73ADA4}▉}$ <code>#73ADA4</code> <i>Cadet blue</i><br>
        ${\color{#9ABEFF}▉}$ <code>#9ABEFF</code> <i>Baby blue eyes</i><br>
        ${\color{#728DBE}▉}$ <code>#728DBE</code> <i>Dark pastel blue</i><br>
        ${\color{#54688C}▉}$ <code>#54688C</code> <i>UCLA Blue</i><br>
        ${\color{#ABABFF}▉}$ <code>#ABABFF</code> <i>Baby blue eyes</i><br>
        ${\color{#BD9AFF}▉}$ <code>#BD9AFF</code> <i>Bright lavender</i><br>
        ${\color{#8C72BD}▉}$ <code>#8C72BD</code> <i>Ube</i><br>
      </td>
      <td valign="top">
        ${\color{#FFB0AC}▉}$ <code>#FFB0AC</code> <i>Melon</i><br>
        ${\color{#F58F8A}▉}$ <code>#F58F8A</code> <i>Light coral</i><br>
        ${\color{#F4806D}▉}$ <code>#F4806D</code> <i>Coral pink</i><br>
        ${\color{#E85E5C}▉}$ <code>#E85E5C</code> <i>Terra cotta</i><br>
        ${\color{#DC505E}▉}$ <code>#DC505E</code> <i>Dark terra cotta</i><br>
        ${\color{#B02A3C}▉}$ <code>#B02A3C</code> <i>Deep carmine</i><br>
        ${\color{#7A1B1C}▉}$ <code>#7A1B1C</code> <i>Falu red</i><br>
        ${\color{#511119}▉}$ <code>#511119</code> <i>Dark scarlet</i><br>
      </td>
      <td valign="top">
        ${\color{#F1E9E0}▉}$ <code>#F1E9E0</code> <i>Eggshell</i><br>
        ${\color{#D6C8BA}▉}$ <code>#D6C8BA</code> <i>Pastel gray</i><br>
        ${\color{#D4C6B8}▉}$ <code>#D4C6B8</code> <i>Pale silver</i><br>
        ${\color{#D7D0B8}▉}$ <code>#D7D0B8</code> <i>Pastel gray</i><br>
        ${\color{#E2C9B0}▉}$ <code>#E2C9B0</code> <i>Desert sand</i><br>
        ${\color{#D4B79A}▉}$ <code>#D4B79A</code> <i>Tan</i><br>
        ${\color{#BF9E73}▉}$ <code>#BF9E73</code> <i>Camel</i><br>
      </td>
    </tr>
  </tbody>
</table>

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
