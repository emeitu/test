#! /bin/sh


while read key value
do
	echo $key,$value
done < < (cat ip.txt)
