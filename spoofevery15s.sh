#!/bin/bash
while true; do
	python iq_transmitter.py &
	sleep 10

	killall -9 python

	python /home/user/SDR/txstop.py &
	sleep 5
	killall -9 python

	sleep 15


done
