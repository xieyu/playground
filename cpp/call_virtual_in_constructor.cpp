#include<string>
#include<iostream>
using namespace std;

class B {
    public:
        B(const string& ss) { cout << "B constructor\n"; f(ss); }
        virtual void f(const string&) { cout << "B::f\n";}
};
class D : public B {
    public:
        D(const string & ss) :B(ss) { cout << "D constructor\n"; f(ss);}
        void f(const string& ss) { cout << "D::f\n"; s = ss; }
    private:
        string s;
};
int main()
{
    D d("Hello");
}
