#include <iostream> 
#include <vector> 
#include <string>
#include <memory.h>

using namespace std;
void inputData(vector<int> &Row, vector<int> &Col, vector< vector< vector<char> > > &Miner, vector< vector< vector<char> > > &Result)
{ 
    int row,col;

    vector< vector<char> > M; 
    vector<char> T; 
    
    while(cin >> row >> col){ 
        if(row==0 && col==0){ 
            break;
        }
        else{
            Row.push_back(row);
            Col.push_back(col); 
            M.clear();  
            for(int i=0; i<row; i++){ 
                T.clear();
                char str;
                for(int j=0; j<col; j++){
                    cin >> str;
                    T.push_back(str);
                }
                M.push_back(T);
            }
            Miner.push_back(M);
            Result.push_back(M); 
        } 
    }
}


void proccessData(vector<int> &Row, vector<int> &Col, vector< vector< vector<char> > > &Miner, vector< vector< vector<char> > > &Result){
     for(int i=0; i<Miner.size(); i++){ 
         for(int j=0; j<Row[i]; j++){
            for(int k=0; k<Col[i]; k++){
                if(Miner[i][j][k] == '*')
                    Result[i][j][k] = '*';            
                else{
                    int number = 0;
                    if(j-1>=0){
                        if(k-1>=0){
                            number = (Miner[i][j-1][k-1]=='*') ? (number+1) : number; 
                        }
                        if(k+1 < Col[i]){
                            number = (Miner[i][j-1][k+1]=='*') ? (number+1) : number; 
                        }
                        number = (Miner[i][j-1][k]=='*') ? (number+1) : number; 
                    }

                    if(j+1 < Row[i]){
                        if(k-1 >= 0){
                            number = (Miner[i][j+1][k-1]=='*') ? (number+1) : number; 
                        }
                        if(k+1 < Col[i]){
                            number = (Miner[i][j+1][k+1]=='*') ? (number+1) : number; 
                        }
                        number = (Miner[i][j+1][k]=='*') ? (number+1) : number; 
                    }

                    if(k-1 >= 0){
                        number = (Miner[i][j][k-1]=='*') ? (number+1) : number; 
                    }
                    if(k+1 < Col[i]){
                        number = (Miner[i][j][k+1]=='*') ? (number+1) : number; 
                    }

                    Result[i][j][k] = number + 48;
                }
            }
        }
    }
}

void outputData(vector<int> &Row, vector<int> &Col, vector< vector< vector<char> > > &Result){
    for(int i=0; i<Result.size(); i++){
        cout << "Field #"<< i+1 <<":"<<endl;
        for(int j=0; j<Row[i]; j++){
            for(int k=0; k<Col[i]; k++){
                cout<< Result[i][j][k];
            }
            cout<< endl;
        }
        cout << endl;
    }
}
    


int main()
{ 
    int row, col;
    //vector< vector< vector<char> > > Miner; 
    //vector< vector< vector<char> > > Result; 
    //vector<int> Row;
    //vector<int> Col;

    int times = 0;
    vector<string> Miner;
    //vector<string> Result;
    int result[103][103];
    int dxdy[8][2] = {1,0, 0,1, -1,0, 0,-1, 1,-1, -1,1, 1,1, -1,-1};

    while(cin >> row >> col && row+col){ 
        Miner.clear();
        memset(result, 0, sizeof(result));
        
        string s;
        for(int i=0; i<row; i++){
            s.clear();
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

/*
        for(int j=0; j<row; j++){
            for(int k=0; k<col; k++){
                if(Miner[j][k] == '*')
                    Result[j][k] = '*';            
                else{
                    int number = 0;
                    if(j-1>=0){
                        if(k-1>=0){
                            number = (Miner[j-1][k-1]=='*') ? (number+1) : number; 
                        }
                        if(k+1 < col){
                            number = (Miner[j-1][k+1]=='*') ? (number+1) : number; 
                        }
                        number = (Miner[j-1][k]=='*') ? (number+1) : number; 
                    }

                    if(j+1 < row){
                        if(k-1 >= 0){
                            number = (Miner[j+1][k-1]=='*') ? (number+1) : number; 
                        }
                        if(k+1 < col){
                            number = (Miner[j+1][k+1]=='*') ? (number+1) : number; 
                        }
                        number = (Miner[j+1][k]=='*') ? (number+1) : number; 
                    }

                    if(k-1 >= 0){
                        number = (Miner[j][k-1]=='*') ? (number+1) : number; 
                    }
                    if(k+1 < col){
                        number = (Miner[j][k+1]=='*') ? (number+1) : number; 
                    }

                    Result[j][k] = number + 48;
                }
            }
        }
        cout << "Field #"<< ++times<<":"<<endl;
        for(int i=0; i<row; i++){
            cout << Result[i] <<endl;
        }
*/
    } 
      
    //inputData(Row, Col, Miner, Result);
    //proccessData(Row, Col, Miner, Result);
    //outputData(Row, Col, Result);

    return 0;
}
