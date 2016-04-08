#include <iostream>
#include <string>
#include <math.h>
#include <cstring>
#include <cctype>
#include <vector>
#include <list>
#include <stack>
#include <utility>

using namespace std;

int main()
{
    unsigned char Q = 0;
    unsigned char N[10] = {0};
    float A[50] = {0};
    unsigned char B[50] = {0};
    float price = 0;
    int hopeness = 0;

    float A_int[50] = {0};
    float A_float[50] = {0};

    cout << "#####start#####"<<endl;

    int ia[3] = {0,1,2};
    string sa[3] = {"a","b","c"};
    
    cout << (int)(sa[0][4]) << endl;

    vector<int> ivec(ia, ia+10);
    for(auto it:ivec)  cout << it;
    cout << endl;
 
    vector<string> svec(sa, sa+2); // why does it throw an error while ivec doesn't?
    for(auto it:svec)  cout << it;
    cout << endl;

    /*
    cin >> Q;
    for(int i=0; i<Q; ++i){
        cin >> N[i];
        int p_AInt = 0;
        int p_AFloat = 0;
        for(int j=0; j<N[i]; ++j){
            cin >> A[j] >> B[j];
            if(floor(A[j]) == A[j]){
                A_int[p_AInt++] = A[j];
            }
            else{
                A_float[p_AFloat++] = A[j];
            }

        }
        
    }
    */

}
