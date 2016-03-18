#include <iostream>
#include <stdio.h>
#include <string.h>
#include <string>
#include <json/value.h>
#include <json/reader.h>
#include <json/writer.h>


using namespace std;
using namespace Json;

int main()
{
    const char *jsonStr ="{}";
    //const char* str = "{\"uploadid\": \"UP000000\",\"code\": \"100.00\",\"msg\": \"\",\"files\": \"\"}";  
    const char* str = "{\"uploadid\": \"UP000000\",\"code\": \"100.00\",\"msg\": \"\",\"files\": \"\"}";  
//    const char *str = "{\"required\": {\"imei\": \"value1\", \"bfd_nid\": \"value2\"}}";

    Json::Reader reader;  
    Json::Value root;  
    if (reader.parse(str, root))  // reader将Json字符串解析到root，root将包含Json里所有子元素  
    {  
#if 0
        Json::Value required_ = root["required"];
        for (Json::ValueIterator iter=required_.begin(); iter!=required_.end(); iter++) {
            string dict=(*iter).asString();
            string key = iter.key().asString();
                cout<<"dict:"<<dict<<"code:"<<key<<endl;
        }
#endif
        cout<<"-------------"<<endl;
        for (Json::ValueIterator iter=root.begin(); iter!=root.end(); iter++) {
            //string dict=*iter;
            string dict=iter.key().asString();
            //string code = (*iter)[code].asString();
            string code = root[dict].asString();
                cout<<"dict:"<<dict<<"code:"<<code<<endl;
        }


        Json::Value::Members members = root.getMemberNames();
        for (Json::Value::Members::iterator it=members.begin(); it!=members.end(); ++it) {
            string name = *it;
            string value_str = root[name].asString();

            cout<<"name:"<<name<<":"<<value_str<<endl;   

        }
        cout<<"-------------------------"<<endl;
#if 0
        std::string upload_id = root["uploadid"].asString();  // 访问节点，upload_id = "UP000000"  
        string code = root["code"].asInt();    // 访问节点，code = 100 
        cout<<"code:"<<code
            <<" isInt:"<<root["code"].isInt()<<" value:"<<root["code"].asInt()
            <<" isDouble:"<<root["code"].isDouble()<<"  value:"<<root["code"].asInt()

            <<endl;
#endif
    }  
#if 0

    Value root;
    FastWriter fast_writer;
    StyledWriter styled_writer;
    root["REGION_ID"]= "600901";
    root["DATA_TOTAL_NUM"]= "456278";
    cout<< fast_writer.write(root) << endl;
    cout<< styled_writer.write(root) << endl;

    Json::Value root1;
    Json::Value arrayObj;
    Json::Value item;
    for (int i=0; i<10; i++)
    {
        item["key"] = i;
        arrayObj.append(item);
    }

    root1["key1"] = "value1";
    root1["key2"] = "value2";
    root1["array"] = arrayObj;
    root1.toStyledString();
    std::string out = root1.toStyledString();
    std::cout << out << std::endl;
#endif
}
