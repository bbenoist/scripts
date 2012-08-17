#!/bin/sh

iwconfig wlan0 2>&1 | grep -q no\ wireless\ extensions\. && {
  echo Wired
  exit 0
}

essid=`iwconfig wlan0 | awk -F '"' '/ESSID/ {print $2}'`
stngth=`iwconfig wlan0 | awk -F '=' '/Quality/ {print $2}' | cut -d '/' -f 1`
bars=`expr $stngth / 10`

if [$1 = ]; then
  case $bars in
    0)  bar='[----------]' ;;
    1)  bar='[/---------]' ;;
    2)  bar='[//--------]' ;;
    3)  bar='[///-------]' ;;
    4)  bar='[////------]' ;;
    5)  bar='[/////-----]' ;;
    6)  bar='[//////----]' ;;
    7)  bar='[///////---]' ;;
    8)  bar='[////////--]' ;;
    9)  bar='[/////////-]' ;;
    10) bar='[//////////]' ;;
    *)  bar='[----!!----]' ;;
  esac
else
  case $bars in
    0)  bar='[<fc=#FF0000>----------</fc>]' ;;
    1)  bar='[<fc=#FF3300>/---------</fc>]' ;;
    2)  bar='[<fc=#FF6600>//--------</fc>]' ;;
    3)  bar='[<fc=#FF9900>///-------</fc>]' ;;
    4)  bar='[<fc=#FFCC00>////------</fc>]' ;;
    5)  bar='[<fc=#FFFF00>/////-----</fc>]' ;;
    6)  bar='[<fc=#CCFF00>//////----</fc>]' ;;
    7)  bar='[<fc=#99FF00>///////---</fc>]' ;;
    8)  bar='[<fc=#66FF00>////////--</fc>]' ;;
    9)  bar='[<fc=#33FF00>/////////-</fc>]' ;;
    10) bar='[<fc=#00FF00>//////////</fc>]' ;;
    *)  bar='[<fc=#ff0000>----!!----</fc>]' ;;
  esac
fi

echo $essid: $bar

exit 0
