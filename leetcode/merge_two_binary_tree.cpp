#include<iostream>

struct TreeNode {
    int val;
    TreeNode *left;
    TreeNode *right;
    TreeNode(int x) : val(x), left(nullptr), right(nullptr) {}
};

class Solution {
public:
    TreeNode* mergeTrees(TreeNode* t1, TreeNode* t2) {
        if (!t1 && !t2) {
            return nullptr;
        }
        int val = 0;
        val += t1 ? t1->val : 0;
        val += t2 ? t2->val : 0;
        TreeNode* p = new TreeNode(val);
        p->left = mergeTrees(t1 ? t1->left : nullptr, t2 ? t2->left : nullptr);
        p->right = mergeTrees(t1 ? t1->right : nullptr, t2 ? t2->right: nullptr);
        return p;
    }
};
