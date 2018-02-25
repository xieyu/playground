/**
 * Definition for singly-linked list.
 * struct ListNode {
 *     int val;
 *     ListNode *next;
 *     ListNode(int x) : val(x), next(NULL) {}
 * };
 */
// Input: (2 -> 4 -> 3) + (5 -> 6 -> 4)
// Output: 7 -> 0 -> 8
// Explanation: 342 + 465 = 807.

 struct ListNode {
     int val;
     ListNode *next;
     ListNode(int x) : val(x), next(nullptr) {}
 };

class Solution {
public:
    ListNode* addTwoNumbers(ListNode* l1, ListNode* l2) {
         if (!l1 && ! l2){
            return nullptr;
        }
        ListNode* sum = nullptr;
        ListNode* p_sum  = sum;
        int val = 0;
        int carry = 0;
        while(l1 && l2) {
            val = l1->val + l2->val + carry;
            carry = val / 10;
            val = val % 10;
            ListNode* node = new ListNode(val);
            if (p_sum) {
                p_sum->next = node;
                p_sum = node;
            }
            else{
                p_sum = node;
                sum = node;
            }
            l1 = l1->next;
            l2 = l2->next;
        }

        ListNode* p = l1 ? l1 : l2;
        while(p) {
            val = p->val + carry;
            carry = val / 10;
            val = val % 10;
            p_sum->next = new ListNode(val);
            p_sum = p_sum->next;
            p = p->next;
        }

        if (carry > 0) {
            ListNode* node = new ListNode(carry);
            p_sum->next = node;
            p_sum = node;
        }
        return sum;
    }
};


