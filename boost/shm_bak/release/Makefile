main:
	g++ producer.cpp ShmMap.cpp  -lpthread -lboost_program_options -o producer  -g
	g++ consumer.cpp ShmMap.cpp  -lpthread -lboost_program_options -o consumer  -g

clean:
	rm -rf producer
	rm -rf consumer

