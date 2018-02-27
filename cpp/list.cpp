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

    List(const List& other);
    List& operator=(const List& other);

    List(List&& other);
    List& operator=(List&& other);

    ~List();


    bool contain(const T& v) const;
    std::size_t len() const;

    void append(const std::initializer_list<T>& l);
    void append(const T& v);

    void remove(const T& v);
    void remove_at(int index);
    void revese();
    void clear();
    void print();

    // sort
    void bubbleSort();
    void insertSort();
private:
    void sortedInsert(Node* iter);

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

// copy constructor
template<typename T>
List<T>::List(const List& other)
    :_head(nullptr)
    ,_tail(nullptr)
    ,_len(0)
{
    cout<<"call list copy constructor"<<endl;
    Node* iter = other._head;
    while(iter){
        append(iter->value);
        iter = iter->next;
    }
}

// move constructor
template<typename T>
List<T>::List(List&& other){
    cout<<"call list move constructor"<<endl;
    _head = other._head;
    _tail = other._tail;
    _len = other._len;

    other._head = nullptr;
    other._tail = nullptr;
    other._len = 0;
}

// move assign operator
template<typename T>
List<T>& List<T>::operator=(List&& other){
    cout<<"call list move assign operator"<<endl;
    if (this != &other) {
        clear();
        _head = other._head;
        _tail = other._tail;
        _len = other._len;

        other._head = nullptr;
        other._tail = nullptr;
        other._len = 0;
    }
    return *this;
}

// copy assign operator
template<typename T>
List<T>& List<T>::operator=(const List& other){
    cout<<"call list copy assign operator"<<endl;
    if (this != &other) {
        clear();
        *this = List(other);
    }
    return *this;
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
void List<T>::print() {
    Node* iter = _head;
    while(iter){
        std::cout<<iter->value<<",";
        iter = iter->next;
    }
    std::cout<<std::endl;
}

template<typename T>
bool List<T>::contain(const T& value) const{
    Node* iter = _head;
    while(iter){
        if (iter->value == value){
            return true;
        }
        iter = iter->next;
    }
    return false;
}

template<typename T>
void List<T>::bubbleSort(){
    Node* end = nullptr;
    cout<<"bubbleSorting: "<<endl;
    while(_head && _head != end){
        print();
        Node* iter = end = _head;
        do {
            Node* next = iter->next;
            if (next && next->value < iter->value) {
                std::swap(iter->value, next->value);
                end = iter;
            }
            iter = next;
        } while(iter && iter != end);
    }
}

template<typename T>
void List<T>::insertSort(){
    List<T> sortedList;
    Node* iter = _head;
    _head = nullptr;
    while(iter) {
        sortedList.print();
        Node* next = iter->next;
        iter->next = nullptr;
        sortedList.sortedInsert(iter);
        iter = next;
    }
    *this = std::move(sortedList);
}

template<typename T>
void List<T>::sortedInsert(Node* p){
    if (!p) {
        return;
    }
    Node* iter = _head;
    Node* prev = nullptr;
    while(iter) {
        if (iter->value > p->value){
            break;
        }
        prev = iter;
        iter = iter->next;
    }
    p->next = iter;
    _len++;
    // insert before _head
    if (prev == nullptr){
        _head = p;
    }
    else {
        prev->next = p;
    }
    if (iter == nullptr){
        _tail = p;
    }
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
        cout<<"test2 contain 3"<<test2.contain(3)<<endl;
        test2.print();
    }

    {
        //test initializer_list
        List<int> test3{10, 2, 3, 4, 5};
        test3.print();
        test3.clear();
        test3.append({1,4,9,3,2,5,7,0});
        test3.print();
    }
    {
        //test move constructor
        List<int> test1{5, 3, 3};
        List<int> test2(std::move(test1));
        cout<<"test 1 is";
        test1.print();
        cout<<"test 2 is";
        test2.print();
    }
    {
        cout<<"test move assignment"<<endl;
        List<int> test1{5, 3, 3};
        List<int> test3{2, 3, 2};
        List<int> test2;

        test3 = test2 = std::move(test1);
        cout<<"test 1 is";
        test1.print();
        cout<<"test 2 is";
        test2.print();

        cout<<"test 3 is";
        test3.print();
    }
    {
        cout<<"test bubbleSort"<<endl;
        List<int> test{8 ,3, 2,7, 2, 3,1,4,56,59, 20,11};
        cout<<"test1 before bubble sort";
        test.print();
        test.bubbleSort();
        cout<<"test1 after bubble sort";
        test.print();
        cout<<"empty link list sort"<<endl;
        List<int> test2;
        test2.bubbleSort();

    }
    {
        cout<<"test insertSort"<<endl;
        List<int> test{8 ,3, 2,7, 2, 3,1,4,56,59, 20,11};
        cout<<"test1 before bubble sort";
        test.print();
        test.insertSort();
        cout<<"test1 after bubble sort";
        test.print();
        cout<<"empty link list sort"<<endl;
        //List<int> test2;
        //test2.insertSort();
    }
}
