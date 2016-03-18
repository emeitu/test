#ifndef _KAFKACONSUMERCLIENT_ICE_
#define _KAFKACONSUMERCLIENT_ICE_
module bfd{
module kafkaconsumerclient{

	class RetInfo{
		string message;
		int ret;//0:no message;-1: has an error;1: message
	};
	sequence<RetInfo> RetInfoSeq;
	interface KafkaConsumerClientManager{
		/*************************************************************************************
		特别提示：
		目前一下接口中只有部分函数能够使用，其余函数作为接口保留。
		能够使用的接口函数有：
		close，closeAndDelete，getUserID，get，getArray，setConsumeMethod
		**************************************************************************************/

		/***********************************************
		getUserID函数为客户端启动时必须调用的
		初始化函数。此函数返回一个序列号
		用于标识本客户端。当客户端使用
		下面的其它函数时，需要传递此参数

		close函数用于关闭实例使用。客户端
		如果已经获得了所需的数据，那么
		需要调用函数来释放服务器上的资源
		closeAndDelete函数除了进行close函数
		的工作外，还将删除zk中注册的group信息。
		如果使用getFromBegin系列或使用getPeriod
		系列函数，需要使用此函数。
		
		setConsumeMethod函数针对group设定，对应新的topic时，
		是从数据的开始端读数据，还是从数据的末尾段读数据。
		method为1，表示从开始端读数据，为0，从末尾端读数据。
		程序默认为从数据的末尾端读数据。
		************************************************/
		long getUserID();
		void close(string topic, string group, long userid);
		void closeAndDelete(string topic, string group, long userid);
		int setConsumeMethod(string group, int method);
		/***********************************************
		以下函数为常规调用函数，有自动
		提交数据偏移的功能
		************************************************/
		RetInfo get(string topic, string group, long userid);//return one message per call;
		RetInfo getFromBegin(string topic, string group, long userid);//return one message per call;
		RetInfo getPeriod(string topic, string group, string date, long userid);//return one message per call;date:2012-03-02
		RetInfo getPeriodFromBegin(string topic, string group, string date, long userid);
		
		/*Array系列函数为批函数，调用一次返回一组消息。参数seqlen为限定每次最大返回的消息条数*/
		RetInfoSeq getArray(string topic, string group, long userid, int seqlen);//return an array messages per call;
		RetInfoSeq getArrayFromBegin(string topic, string group, long userid, int seqlen);//return an array messages per call;
		RetInfoSeq getArrayPeriod(string topic, string group, string date, long userid, int seqlen);//return an array messages per call;date:2012-03-02
		RetInfoSeq getArrayPeriodFromBegin(string topic,string group,string date, long userid, int seqlen);
		
		RetInfo getBlock(string topic, string group, long userid);
		RetInfo getFromBeginBlock(string topic, string group, long userid);
		RetInfoSeq getArrayBlock(string topic, string group, long userid, int seqlen);
		RetInfoSeq getArrayFromBeginBlock(string topic, string group, long userid, int seqlen);

		/***********************************************
		以下函数供hadoop离线分析使用
		hadoop需要手动提交数据偏移，初始化
		与以上函数不同，需要使用hadoopGet
		函数获得数据
		************************************************/
		void commitoffset(string topic, string group, long userid);
		RetInfo hadoopGet(string topic, string group, long userid);
		RetInfoSeq hadoopGetTopicList(string prefix, string password);
	};
};
};

#endif
