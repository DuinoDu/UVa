#include <iostream> 
#include <vector> 
#include <string>
#include <memory.h>

using namespace std;

int main()
{ 
    int row, col;
    int times = 0;
    vector<string> Miner;
    int result[103][103];
    int dxdy[8][2] = {1,0, 0,1, -1,0, 0,-1, 1,-1, -1,1, 1,1, -1,-1};

    while(cin >> row >> col && row+col){ 
        Miner.clear();
        memset(result, 0, sizeof(result));
        
        for(int i=0; i<row; i++){
            string s;
            cin >> s;
            Miner.push_back(s);
        }
        for(int j=0; j<row; j++){
            for(int k=0; k<col; k++){
                if(Miner[j][k] == '*'){
                    for(int l=0; l<8; l++){
                        int x = j + dxdy[l][0];
                        int y = k + dxdy[l][1];
                        if(x>=0 && x<row && y>=0 && y<col){
                            ++result[x][y];
                        }
                    }
                }
            }
        }
        if(times >0) cout<<endl;
        cout << "Field #"<< ++times<<":"<<endl;
        for(int i=0; i<row; i++){
            for(int j=0; j<col; j++){
                if(Miner[i][j] == '*')
                    cout << "*";
                else
                    cout << result[i][j];
            }
            cout << endl;
        }
    }
    return 0;
}

