#! /bin/sh


#shopt -s -o nounset

declare -a KEY
declare -a VALUE

declare -i k=0

echo "hello"
#echo "ret:${KEY[0]} = ${VALUE[0]}"



echo "******"
awk  'BEGIN{FS=": "} /\w: \w/  {print $1, $2}'  app.conf  | while read N V
do
	KEY[$k]=$N
	VALUE[$k]=$V
	echo "${KEY[$k]} = ${VALUE[$k]}  $k"
	((k++))
done  

echo "k:$k  ${KEY[*]}"
echo "${KEY[$k]} = ${VALUE[$k]}  $k"
echo "${KEY[0]} = ${VALUE[1]}"


