#include<iostream>
#include<cstring>

class String
{
    public:
        String():_data(nullptr){}
        String(const char* data);
        String(const String& other);
        String& operator= (const String& other);
        ~String();
    private:
        char* _data;
};

String::String(const char* data){
    _data = nullptr;
    if(data){
        size_t len = strlen(data) + 1;
        // will throw std::bad_alloc ?
        _data = new char[len];
        strcpy(_data, data);
    }
}

String::~String(){
    if (_data){
        delete _data;
    }
}

String::String(const String& other){
    size_t len = strlen(other._data) + 1;
    _data = new char[len];
    strcpy(_data, other._data);
}

String& String::operator= (const String& other){
    if (this != &other){
        String tmp(other);
        std::swap(tmp._data, _data);
    }
    return *this;
}

int main(){
    String a("abc");
    String b(a);
    String c=b;
    return 0;
}
