#include<iostream>
using namespace std;

class Solution {
public:
    int hammingDistance(int x, int y) {
        int ret = x ^ y;
        int count = 0;
        while (ret){
            count += ret&1;
            ret >>= 1;
        }
        return count;
    }
};

int main(){
    Solution s;
    int result = s.hammingDistance(1, 4);
    cout <<result<<endl;

}
