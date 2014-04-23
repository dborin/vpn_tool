for session in $(screen -ls | grep -o '[0-9]\{3,5\}.vpntool');do
  screen -S "${session}" -X quit;
done

cd /usr/local/vpn_tool/
screen -dmS vpntool
screen -S vpntool -X screen ./vpn_tool.py
