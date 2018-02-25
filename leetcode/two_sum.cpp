#include<vector>
#include<iostream>
#include<algorithm>
#include<map>

using namespace std;


class Solution {
public:
    vector<int> twoSum(vector<int>& nums, int target) {
        //time cost O(n^2)
        //space cost O(1)
        for(int i =0; i < nums.size(); i++){
            int v = target - nums[i];
            for(int j = i + 1; j < nums.size(); j++){
                if (v == nums[j]) {
                    return {i, j};
                }
            }
        }
        throw std::runtime_error("no solution find");
    }

    vector<int> twoSum_withMap(vector<int>& nums, int target) {
        std::map<int, int> dict;
        for(int i =0; i < nums.size(); i++){
            int v = target - nums[i];
            auto iter = dict.find(v);
            if (iter != dict.end() && iter->second != i){
                return {iter->second, i};
            }
            dict[nums[i]] = i;
        }
        throw std::runtime_error("no solution find");
    }
};

int main(){
    Solution s;
    vector<int> nums = {1, 2, 4, 7};
    auto result = s.twoSum(nums, 6);
    cout<<"results:"<<endl;
    for(auto r: result){
        cout<<r<<endl;
    }

    result = s.twoSum_withMap(nums, 6);
    cout<<"results:"<<endl;
    for(auto r: result){
        cout<<r<<endl;
    }
}
