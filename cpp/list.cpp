#include <cstddef>

template<typename T>
class List{
    struct Node {
        T value;
        Node *next;
    };

public:
    List():_head(nullptr), _tail(nullptr), _len(0){}
    void append(const T& v);
    void remove(const T& v);
    void remove_at(int index);
    std::size_t len() const;
private:
    Node* _head;
    Node* _tail;
    std::size_t _len;
};

template<typename T>
void List<T>::append(const T& v){
    Node* node = new Node();
    node->value = v;
    _len += 1;

    if (_head == nullptr) {
        _head = node;
        _tail = node;
        return;
    }
    _tail->next = node;
    _tail = node;
}


int main(){
    List<int> test;
    test.append(10);
    test.append(11);
    test.append(12);
}
