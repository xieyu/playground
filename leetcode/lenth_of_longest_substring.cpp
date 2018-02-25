#include<string>
#include<iostream>
#include<map>
#include<vector>

using namespace std;

class Solution {
public:
    int lengthOfLongestSubstring(string s) {
        int max_length = 0, i = 0, j = 0;
        for(j = 0; j  < s.size(); j++){
            char next = s[j];
            for(int k = i; k < j; k++){
                if (s[k] == next){
                    max_length = std::max(j - i, max_length);
                    i = k + 1;
                }
            }
        }
        max_length = std::max(j - i, max_length);
        return max_length;
    }
};

int main(){
    Solution s;
    int max_len = s.lengthOfLongestSubstring("dvdvdf");
    std::cout <<max_len<<endl;;
}
