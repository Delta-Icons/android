# Introduction

## Requirements

In case you wanna contribute to Delta you need:

- basic knowledge of `git`
- a fork of this repo
- a SVG icon
- a 192x192px PNG icon
- ComponentInfo(s) of the target app ([?](#gathering-componentinfo))

## Info

We have two methods of adding icons:
  - [Auto method](#auto-method) is a new method of adding icons. You only need to add PNG and SVG to a specific folder and append the icon name with ComponentInfo(s) to a specific YAML file. These files will be automatically handled by our CI/CD every release. [Go to full instruction](#auto-method). 
  - [Manual method](#manual-method) implies editing four XML files and adding icons to two specific folders. [Go to full instruction](#manual-method).

We also have such a thing as alternative icons —  we mainly use it to move an existing icon to an alternative one after rebranding, but there's nothing stopping you to make alternative icons for any app in different shapes as you wish. You can select an alternative icon for the target app via your icon launcher if it supports that feature.

Description of categories and what they are for:

- `New`: for new icons obviously (new icons always must be duplicated there)
- `Alts`: for alternative icons
- `Calendar`: for calendar icons
- `Folders`: for folder icons
- `Google`: for Google apps (Chrome, YouTube, etc.)
- `System`: for system icons (Camera, Settings, etc.)
- `#`: icons whose name starts with a number (or, to be more clear, with an underscore followed by a number, e.g. `_2048`)
- `A-Z`: icons which don't fit in previous categories must be placed in a category based on the first letter of its name

## Tips

- Keep `LF` line endings in files (`CLRF` breaks our CI/CD)
- SVG, PNG and drawable names must be the same
- Keep filenames in alphanumeric lowercase with underscores
- If the icon name starts with a number, it must have a leading underscore (e.g. `_9gag`) and be placed in `#` category
- Keep the next naming format of alternative icons: `new_icon_alt_x`, where `x` is a number of current alternative version (yes, we have multiple of them, e.g. `old_icon_alt_1`, `old_icon_alt_2`, etc.

# Contributing

> _`new_icon` will be used as the icon name_ <br>
> _`new_icon_alt_1` will be used as the alternative icon for `new_icon`_ <br>
> _`com.example/com.example.MainActivity` will be used as the 1st ComponentInfo for `new_icon`_ <br>
> _`com.example/com.example.StartActivity` will be used as the 2nd ComponentInfo for `new_icon`_

Don't forget to give yourself an entry at the bottom of [app/src/main/res/xml/contributors.xml](https://github.com/Delta-Icons/android/tree/master/app/src/main/res/xml/contributors.xml) if this is your first contribution!

## Auto Method

> **This method is only for adding new icons or linking ComponentInfo(s) with existing icons!** 

1. Add `new_icon.svg` and `new_icon.png` to [resources/utilities/icons](https://github.com/Delta-Icons/android/tree/master/resources/utilities/icons) directory

2. Append the icon name with ComponentInfo(s) to [resources/new_icons.yaml](https://github.com/Delta-Icons/android/blob/master/resources/new_icons.yaml) with any of the next formats:

    2.1. The new icon with the ComponentInfo.

    > Can be used for linking the ComponentInfo with the existing icon

    ```yaml
    # lines omitted for example

    new_icon:
        - com.example/com.example.MainActivity
    ```
    
    2.2. The new icon with multiple ComponentInfos:
    > Can be used for linking ComponentInfos with the existing icon
    ```yaml
    # lines omitted for example

    new_icon:
        - com.example/com.example.MainActivity
        - com.example/com.example.StartActivity
    ```

    2.3. The icon without the ComponentInfo (the alternative icon):
    
    ```yaml
    # lines omitted for example

    new_icon_alt_1: {}
    ```

And we're done! Repeat the process for adding new icons.

## Manual Method

1. Add `new_icon.svg` to [resources/vectors](https://github.com/Delta-Icons/android/tree/master/resources/vectors) directory

2. Add `new_icon.png` to [app/src/main/res/drawable-nodpi](https://github.com/Delta-Icons/android/tree/master/app/src/main/res/drawable-nodpi) directory

3. Append the line `<item drawable="new_icon" />` in `New` and named categories (the named category is based on the first letter of the icon name; `N` in our case) to [app/src/main/assets/drawable.xml](https://github.com/Delta-Icons/android/tree/master/app/src/main/assets/drawable.xml) and [app/src/main/res/xml/drawable.xml](https://github.com/Delta-Icons/android/tree/master/app/src/main/res/xml/drawable.xml). How it should look:

    ```xml
        <!-- lines omitted -->
        <category title="New" />
        <!-- lines omitted -->
        <item drawable="latest_entry">
        <item drawable="new_icon" />
        
        <category title="Alts" />
        <!-- lines omitted -->

        <category title="N" />
        <!-- lines omitted -->
        <item drawable="latest_entry">
        <item drawable="new_icon" />
        
        <category title="O" />
        <!-- lines omitted -->
    ```
    > You can edit one file and overwrite another with it to keep them identical.

4. Append the line `<item component="ComponentInfo{com.example/com.example.MainActivity}" drawable="new_icon" />` to [app/src/main/assets/appfilter.xml](https://github.com/Delta-Icons/android/tree/master/app/src/main/assets/appfilter.xml) and [app/src/main/res/xml/appfilter.xml](https://github.com/Delta-Icons/android/tree/master/app/src/main/res/xml/appfilter.xml). How it should look:

    ```xml
        <!-- lines omitted -->
        <item component="ComponentInfo{com.google/com.google.MainActivity}" drawable="latest_entry" />
        <item component="ComponentInfo{com.example/com.example.MainActivity}" drawable="new_icon" />
    </resources>
    ```
    > You can edit one file and overwrite another with it to keep them identical.

The end. More complicated than Auto method, but it's a base method, you can modify/fix current icons by this method.

## Other Cases

### Alternative Icons

If the existing icon rebranded, don't overwrite it with a new one, do the following:

> `old_icon` will be used as an existing icon name

> `old_icon_alt_1` will be used as an alternative icon name for the existing icon name

1. Determine if alternative icons exist for the target app by checking `Alts` category in [app/src/main/res/xml/drawable.xml](https://github.com/Delta-Icons/android/tree/master/app/src/main/res/xml/drawable.xml). If no alternative icons then start numbering from `1` (e.g. `old_icon_alt_1`), otherwise continue numbering based on latest alternative icon number (e.g. `old_icon_alt_2`)

2. Rename `old_icon.svg` to `old_icon_alt_1.svg` in [resources/vectors](https://github.com/Delta-Icons/android/tree/master/resources/vectors) directory (if SVG not found there just skip this step)

3. Rename `old_icon.png` to `old_icon_alt_1.png` in [app/src/main/res/drawable-nodpi](https://github.com/Delta-Icons/android/tree/master/app/src/main/res/drawable-nodpi) directory

4. Add `old_icon_alt_1` to `Alts` category and `old_icon` to `New` category in [app/src/main/assets/drawable.xml](https://github.com/Delta-Icons/android/tree/master/app/src/main/assets/drawable.xml) and [app/src/main/res/xml/drawable.xml](https://github.com/Delta-Icons/android/tree/master/app/src/main/res/xml/drawable.xml)

5. If the ComponentInfo also changed after rebranding, replace `old_icon` with `old_icon_alt_1` in [app/src/main/assets/appfilter.xml](https://github.com/Delta-Icons/android/tree/master/app/src/main/assets/appfilter.xml) and [app/src/main/res/xml/appfilter.xml](https://github.com/Delta-Icons/android/tree/master/app/src/main/res/xml/appfilter.xml) (the alternative icon will be linked with the old ComponentInfos for back compability)

# Resources

> _For saving templates/palettes locally do: **Right-Click** &rarr; **Save As**_

## Font

- [Now Font](https://www.1001fonts.com/now-font.html?text=Delta%20Icons) (_use Now Alt from the same family for alternate lowercase 'a' letter_)
- [Aleo Font](https://www.1001fonts.com/aleo-font.html?text=Delta%20Icons) (_optionally use it when Serif is needed_)

## Gathering ComponentInfo

- [Icon Pusher](https://iconpusher.com/) by [Southpaw](https://southpaw.dev)
- [Icon Request](https://github.com/Kaiserdragon2/IconRequest/releases) by [Kaiserdragon2](https://github.com/Kaiserdragon2)

## Icon Template

### Tips

- If the original logo doesn't contain small details or doesn't make up most of the background layer (circle/square/etc.) as designed, keep the logo size between 73-80px

|<img src="https://github.com/Delta-Icons/android/raw/master/resources/templates/template.svg" width="177" height="177">|<img src="https://github.com/Delta-Icons/android/raw/master/resources/templates/template_tutorial.svg" width="547,705" height="600">|
|---|---|

## Colors

### Tips 

- Davy's grey ( <img src="https://placehold.co/15x15/56595B/56595B.png" height="8"> `#56595B` ) as default Black

- Coral pink ( <img src="https://placehold.co/15x15/FF837D/FF837D.png" height="8"> `#FF837D` ) as default Red and Fuzzy Wuzzy  ( <img src="https://placehold.co/15x15/BA6561/BA6561.png" height="8"> `#BA6561` ) as default Dark Red. Shades of Red are specifically for shading purposes

- Transparencies — White (25%, 50%, 70%) and Black (15%, 25%) can be used as overlay for additional shading

### Palette

> Palette variants are hidden under spoilers below

<details>
  <summary>Full</summary>
  <br>
  <img src="https://github.com/Delta-Icons/android/raw/master/resources/palettes/palette.svg">
</details>

<details>
  <summary>Simple</summary>
  <br>
  <center><img src="https://github.com/Delta-Icons/android/raw/master/resources/palettes/palette_simplified.svg"></center>
</details>

<details>
<summary>HTML</summary>
  <br>
  <table>
    <thead>
      <tr>
      <th>Greys</th>
      <th>Basic</th>
      <th>Reds</th>
      <th>Skintones</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td valign="top">
          <img src="https://placehold.co/15x15/FFFFFF/FFFFFF.png" height="8"> <code>#FFFFFF</code> <i>White</i><br>
          <img src="https://placehold.co/15x15/ECECEC/ECECEC.png" height="8"> <code>#ECECEC</code> <i>Isabelline</i><br>
          <img src="https://placehold.co/15x15/D8D8D8/D8D8D8.png" height="8"> <code>#D8D8D8</code> <i>Timberwolf</i><br>
          <img src="https://placehold.co/15x15/D2D2D2/D2D2D2.png" height="8"> <code>#D2D2D2</code> <i>Light gray</i><br>
          <img src="https://placehold.co/15x15/CCCCCC/CCCCCC.png" height="8"> <code>#CCCCCC</code> <i>Pastel gray</i><br>
          <img src="https://placehold.co/15x15/B1B5BD/B1B5BD.png" height="8"> <code>#B1B5BD</code> <i>Ash grey</i><br>
          <img src="https://placehold.co/15x15/A0A5AF/A0A5AF.png" height="8"> <code>#A0A5AF</code> <i>Dark gray</i><br>
          <img src="https://placehold.co/15x15/979797/979797.png" height="8"> <code>#979797</code> <i>Manatee</i><br>
          <img src="https://placehold.co/15x15/83868C/83868C.png" height="8"> <code>#83868C</code> <i>Taupe gray</i><br>
          <img src="https://placehold.co/15x15/56595B/56595B.png" height="8"> <code>#56595B</code> <i>Davy's grey</i><br>
          <img src="https://placehold.co/15x15/4A4A4A/4A4A4A.png" height="8"> <code>#4A4A4A</code> <i>Quartz</i><br>
          <img src="https://placehold.co/15x15/000000/000000.png" height="8"> <code>#000000</code> <i>Black</i><br>
        </td>
        <td valign="top">
          <img src="https://placehold.co/15x15/FFD6D4/FFD6D4.png" height="8"> <code>#FFD6D4</code> <i>Pastel pink</i><br>
          <img src="https://placehold.co/15x15/FF837D/FF837D.png" height="8"> <code>#FF837D</code> <i>Coral pink</i><br>
          <img src="https://placehold.co/15x15/BA6561/BA6561.png" height="8"> <code>#BA6561</code> <i>Fuzzy Wuzzy</i><br>
          <img src="https://placehold.co/15x15/D3B69A/D3B69A.png" height="8"> <code>#D3B69A</code> <i>Tan</i><br>
          <img src="https://placehold.co/15x15/8E6F60/8E6F60.png" height="8"> <code>#8E6F60</code> <i>Shadow</i><br>
          <img src="https://placehold.co/15x15/FCECDC/FCECDC.png" height="8"> <code>#FCECDC</code> <i>Antique white</i><br>
          <img src="https://placehold.co/15x15/F8C18C/F8C18C.png" height="8"> <code>#F8C18C</code> <i>Pale gold</i><br>
          <img src="https://placehold.co/15x15/FDF5D9/FDF5D9.png" height="8"> <code>#FDF5D9</code> <i>Cornsilk</i><br>
          <img src="https://placehold.co/15x15/F9DE81/F9DE81.png" height="8"> <code>#F9DE81</code> <i>Jasmine</i><br>
          <img src="https://placehold.co/15x15/C39A54/C39A54.png" height="8"> <code>#C39A54</code> <i>Camel</i><br>
          <img src="https://placehold.co/15x15/E0F4E0/E0F4E0.png" height="8"> <code>#E0F4E0</code> <i>Platinum</i><br>
          <img src="https://placehold.co/15x15/98DC9A/98DC9A.png" height="8"> <code>#98DC9A</code> <i>Granny Smith Apple</i><br>
          <img src="https://placehold.co/15x15/71A372/71A372.png" height="8"> <code>#71A372</code> <i>Asparagus</i><br>
          <img src="https://placehold.co/15x15/96DFD3/96DFD3.png" height="8"> <code>#96DFD3</code> <i>Pale robin egg blue</i><br>
          <img src="https://placehold.co/15x15/73ADA4/73ADA4.png" height="8"> <code>#73ADA4</code> <i>Cadet blue</i><br>
          <img src="https://placehold.co/15x15/9ABEFF/9ABEFF.png" height="8"> <code>#9ABEFF</code> <i>Baby blue eyes</i><br>
          <img src="https://placehold.co/15x15/728DBE/728DBE.png" height="8"> <code>#728DBE</code> <i>Dark pastel blue</i><br>
          <img src="https://placehold.co/15x15/54688C/54688C.png" height="8"> <code>#54688C</code> <i>UCLA Blue</i><br>
          <img src="https://placehold.co/15x15/ABABFF/ABABFF.png" height="8"> <code>#ABABFF</code> <i>Baby blue eyes</i><br>
          <img src="https://placehold.co/15x15/BD9AFF/BD9AFF.png" height="8"> <code>#BD9AFF</code> <i>Bright lavender</i><br>
          <img src="https://placehold.co/15x15/8C72BD/8C72BD.png" height="8"> <code>#8C72BD</code> <i>Ube</i><br>
        </td>
        <td valign="top">
          <img src="https://placehold.co/15x15/FFB0AC/FFB0AC.png" height="8"> <code>#FFB0AC</code> <i>Melon</i><br>
          <img src="https://placehold.co/15x15/F58F8A/F58F8A.png" height="8"> <code>#F58F8A</code> <i>Light coral</i><br>
          <img src="https://placehold.co/15x15/F4806D/F4806D.png" height="8"> <code>#F4806D</code> <i>Coral pink</i><br>
          <img src="https://placehold.co/15x15/E85E5C/E85E5C.png" height="8"> <code>#E85E5C</code> <i>Terra cotta</i><br>
          <img src="https://placehold.co/15x15/DC505E/DC505E.png" height="8"> <code>#DC505E</code> <i>Dark terra cotta</i><br>
          <img src="https://placehold.co/15x15/B02A3C/B02A3C.png" height="8"> <code>#B02A3C</code> <i>Deep carmine</i><br>
          <img src="https://placehold.co/15x15/7A1B1C/7A1B1C.png" height="8"> <code>#7A1B1C</code> <i>Falu red</i><br>
          <img src="https://placehold.co/15x15/511119/511119.png" height="8"> <code>#511119</code> <i>Dark scarlet</i><br>
        </td>
        <td valign="top">
          <img src="https://placehold.co/15x15/F1E9E0/F1E9E0.png" height="8"> <code>#F1E9E0</code> <i>Eggshell</i><br>
          <img src="https://placehold.co/15x15/D6C8BA/D6C8BA.png" height="8"> <code>#D6C8BA</code> <i>Pastel gray</i><br>
          <img src="https://placehold.co/15x15/D4C6B8/D4C6B8.png" height="8"> <code>#D4C6B8</code> <i>Pale silver</i><br>
          <img src="https://placehold.co/15x15/D7D0B8/D7D0B8.png" height="8"> <code>#D7D0B8</code> <i>Pastel gray</i><br>
          <img src="https://placehold.co/15x15/E2C9B0/E2C9B0.png" height="8"> <code>#E2C9B0</code> <i>Desert sand</i><br>
          <img src="https://placehold.co/15x15/D4B79A/D4B79A.png" height="8"> <code>#D4B79A</code> <i>Tan</i><br>
          <img src="https://placehold.co/15x15/BF9E73/BF9E73.png" height="8"> <code>#BF9E73</code> <i>Camel</i><br>
        </td>
      </tr>
    </tbody>
  </table>
</details>

### Misc

- [Adobe Swatch Exchange Palette](https://github.com/Delta-Icons/android/raw/master/resources/palettes/palette.ase) (Illustrator, Photoshop)

- [GPL Pallete](https://github.com/Delta-Icons/android/raw/master/resources/palettes/palette.gpl) (Inkscape, Karbon)

## Other

- [Figma](https://www.figma.com/file/ELcekhhNH5GAT8Xw5jZhZC/Delta-Icons)
