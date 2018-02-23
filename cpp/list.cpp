#include <cstddef>
#include <iostream>
#include <initializer_list>

using namespace std;

template<typename T>
class List{
    struct Node {
        T value;
        Node *next;
        Node():next(nullptr){}
    };

public:
    List():_head(nullptr), _tail(nullptr), _len(0){}
    List(const std::initializer_list<T>& l);
    ~List();

    void append(const std::initializer_list<T>& l);
    void append(const T& v);
    void remove(const T& v);
    void remove_at(int index);
    void revese();
    void clear();
    void bubbleSort();
    void print();
    std::size_t len() const;

private:
    Node* _head;
    Node* _tail;
    std::size_t _len;
};

template<typename T>
List<T>::List(const std::initializer_list<T>& values)
    :_head(nullptr),
    _tail(nullptr),
    _len(0)
{
    append(values);
}

template<typename T>
List<T>::~List(){
    clear();
}

template<typename T>
void List<T>::clear() {
    Node* iter = _head;
    while(iter){
        Node* p = iter;
        iter = iter->next;
        delete p;
    }
    _head = _tail = nullptr;
    _len = 0;
}

template<typename T>
void List<T>::append(const std::initializer_list<T>& values) {
    for(const T& i: values) {
        append(i);
    }
}

template<typename T>
void List<T>::append(const T& v) {
    Node* node = new Node();
    node->value = v;
    _len++;

    if (_head == nullptr) {
        _head = node;
        _tail = node;
        return;
    }
    _tail->next = node;
    _tail = node;
}


template<typename T>
void List<T>::revese() {
    if (_head == nullptr) {
        return;
    }
    Node* prev = _head;
    Node* iter = prev->next;
    while (iter != nullptr) {
        Node* next = iter->next;
        iter->next = prev;
        prev = iter;
        iter = next;
    }

    _head->next = nullptr;

    Node* tmp = _head;
    _head = _tail;
    _tail = tmp;
}

template<typename T>
void List<T>::print(){
    Node* iter = _head;
    while(iter){
        std::cout<<iter->value<<",";
        iter = iter->next;
    }
    std::cout<<std::endl;
}


int main(){
    {
        List<int> test;
        test.append(10);
        test.append(11);
        test.append(12);
        cout<<"before revese"<<endl;
        test.print();
        test.revese();
        cout<<"after revese"<<endl;
        test.print();
    }

    {
        List<int> test2 = {1, 2, 3, 4, 5};
        test2.print();
        test2.revese();
        test2.print();
    }

    {
        List<int> test3{10, 2, 3, 4, 5};
        test3.print();
        test3.clear();
        test3.append({1,4,9,3,2,5,7,0});
        test3.print();
    }
}
