pid=`cat .tmp.txt`
kill $pid
rm .tmp.txt
echo "Server stopped"

