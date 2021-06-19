#!/bin/bash
# Simple bash script to update the header from icon_requests

# Credit: Marc Bernstein
# https://stackoverflow.com/questions/2495459/formatting-the-date-in-unix-to-include-suffix-on-day-st-nd-rd-and-th
DaySuffix() {
    if [ "x`date +%-d | cut -c2`x" = "xx" ]
    then
        DayNum=`date +%-d`
    else
        DayNum=`date +%-d | cut -c2`
    fi

    CheckSpecialCase=`date +%-d`
    case $DayNum in
    0 )
      echo "th" ;;
    1 )
      if [ "$CheckSpecialCase" = "11" ]
      then
        echo "th"
      else
        echo "st"
      fi ;;
    2 )
      if [ "$CheckSpecialCase" = "12" ]
      then
        echo "th"
      else
        echo "nd"
      fi ;;
    3 )
      if [ "$CheckSpecialCase" = "13" ]
      then
        echo "th"
      else
        echo "rd"
      fi ;;
    [4-9] )
      echo "th" ;;
    * )
      return 1 ;;
    esac
}

old_count=$(sed '2!d' "icon_requests.txt")
old_count=${old_count:0:4}
current_date=$(LANG=en_us_88591; date "+%B %-d`DaySuffix` %Y")
new_count=$(< $"icon_requests.txt" wc -l)
new_count="$(( (new_count - 2) / 5))"
sed -i "2s/.*/$new_count Requests Pending (Updated $current_date)/" icon_requests.txt
if ((new_count >= old_count)); then
  echo "$new_count Requests Pending (+$(( (new_count - old_count))))"
else
    echo "$new_count Requests Pending (-$(( (old_count - new_count))))"
fi

if [[ -f new_apps.txt ]]
then
    while true; do
        read -p "Delete new_apps (y/n)?" -n 1 -r
        case "$REPLY" in 
          [Yy]* ) rm new_apps.txt
                  printf "\nDeleted file new_apps.txt\n"
                  break;;
          [Nn]* ) echo
                  exit ;;
          * ) echo " Please input valid answer.";;
        esac
    done
fi