#include<iostream>
#include<vector>
#include<string>
using namespace std;

class Solution {
public:
    vector<int> partitionLabels(string S) {
        vector<int> partion_lens;
        vector<int> dict = vector<int>(26, -1);
        for (int i = 0; i < S.size(); i++) {
            int ch  = S[i] - 'a';
            dict[ch] = std::max(dict[ch], i);
        }

        for (int i = 0; i < S.size();) {
            int j = dict[S[i] - 'a'];
            for(int k = i; k < j; k++) {
                j = std::max(j, dict[S[k] - 'a']);
            }
            partion_lens.push_back(j - i + 1);
            i = j + 1;
        }
        return partion_lens;
    }
};

int main(){
    Solution s;
    auto result = s.partitionLabels("ntswuqqbidunnixxpoxxuuupotaatwdainsotwvpxpsdvdbwvbtdiptwtxnnbtqbdvnbowqitudutpsxsbbsvtipibqpvpnivottsxvoqqaqdxiviidivndvdtbvadnxboiqivpusuxaaqnqaobutdbpiosuitdnopoboivopaapadvqwwnnwvxndpxbapixaspwxxxvppoptqxitsvaaawxwaxtbxuixsoxoqdtopqqivaitnpvutzchkygjjgjkcfzjzrkmyerhgkglcyffezmehjcllmlrjghhfkfylkgyhyjfmljkzglkklykrjgrmzjyeyzrrkymccefggczrjflykclfhrjjckjlmglrmgfzlkkhffkjrkyfhegyykrzgjzcgjhkzzmzyejycfrkkekmhzjgggrmchkeclljlyhjkchmhjlehhejjyccyegzrcrerfzczfelzrlfylzleefgefgmzzlggmejjjygehmrczmkrc");
    for(auto i: result){
        cout<<i<<endl;
    }
}
