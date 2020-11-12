portVal=`grep PORT ./config/config.py`
port=`echo $portVal | cut -d " " -f 3`
python3 server.py $port &
echo $! > .tmp.txt

