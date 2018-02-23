#include<iostream>
struct A {};

struct B{
    virtual  ~B(){}
};

struct Foo: A{};

enum TestEnum{};

using namespace std;
int main(){
    A test[10];
    cout<<"the size of A test[10] is"<<sizeof(test)<<endl;
    cout<<"the sizeof(A) is "<<sizeof(A)<<endl;
    cout<<"the struct with virtual function: sizeof(B) is "<<sizeof(B)<<endl;
    cout<<"empty based struct size is"<<sizeof(Foo)<<endl;
    cout<<"sizeof emtpy enum is"<<sizeof(TestEnum)<<endl;
}
