#include<iostream>
#include<string>
#include<vector>
#include <cctype>
using namespace std;


int i, j;

struct TrieNode {
    public:
        TrieNode* child[26]; //26 letter
        int mid;    //record movie ID
        bool wordEnd;   //wheter end leaf or not
        string wholeword;

        TrieNode() {
            wordEnd = false;
            for(i=0; i<26; i++){
                child[i] = nullptr; //nullptr -> NULL Pointer
            }
            mid = 0;
            wholeword = "";
        }
};

class TrieTree{
    public:
        TrieNode* root;

        TrieTree() {
            root = new TrieNode();
        }

        void insert(const string& word, int movieID){
            TrieNode* node = root;
            // bool validchar = false;

            for(char c : word){
                if(isalpha(c)){ //if not a letter will return 0
                    c = tolower(c); //change into lowercase
                    // validchar = true;

                    // determine the node is exist or not
                if(node -> child[c - 'a'] == nullptr){
                    node -> child[c - 'a'] = new TrieNode(); // 創建新節點
                }

                node = node -> child[c - 'a']; // 更新指標指向子節點
        
                }
            }

            // if(validchar){
            node -> wordEnd = true;
            node -> mid = movieID;
            node -> wholeword = word;
            // cout << "wholeword: " << node -> wholeword << endl;
            // cout << "NOW is: " << 
            // }
        }

        void dfs(TrieNode* node, vector<string>& result){
            if(node == nullptr) return;
            // vector<string> result;   -> cannot declare in here
            if(node -> wordEnd){ //the end of the wholeword 
                result.push_back(node -> wholeword);
                // cout << "NOW PUSH: " << node -> wholeword << endl;
            }

            for(int i=0; i<26; i++){
                if(node -> child[i] != nullptr){ //has this letter
                    // cout << "LETTER:" << (char)(i+65) << endl;
                    dfs(node -> child[i], result); //search deep letter
                }
            }
            // return result;
        }

        vector<string> search(const string& word){
            TrieNode* node = root;

            for(char c : word){
                if(isalpha(c)){
                    c = tolower(c);

                    if(node -> child[c - 'a'] == nullptr) //letter not in tree
                        return {};

                    node = node -> child[c - 'a'];
                    // cout << "LETTER: " << c << endl;
                }
            }

            vector<string> result;
            dfs(node, result);
            return result;
        }
};


int main(){
    TrieTree trie;

    trie.insert("The Shawshank Redemption", 1);
    trie.insert("The Godfather", 2);
    trie.insert("The Dark Knight", 3);
    trie.insert("12 Angry Men", 4);
    trie.insert("Schindler's List", 5);
    trie.insert("Pulp Fiction", 65);
    trie.insert("Fight Club", 66);
    trie.insert("Star Wars", 67);
    trie.insert("Back to the Future", 68);
    trie.insert("Shichinin no samurai", 69);
    trie.insert("Saving Private Ryan", 70);


    // trie.insert("Hello", 1);
    // trie.insert("Hi", 2);
    // trie.insert("Hey", 3);
    // trie.insert("Goodbye", 4);
    // trie.insert("Good", 5);

    string search_word;

    while(cin >> search_word && search_word != "q"){
        // vector<string> results = search(search_word);
        // -> search function is belonged to TrieTree class, so need to add the declare calss infront of it.
        vector<string> results = trie.search(search_word);

        if(results.empty()){
            printf("No match movie.");
        }
        else{
            cout << "RESULT:" << endl;

            for(const string result: results){
                cout << result << endl;
            }
        }
    }
}