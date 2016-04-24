#include <iostream> 
#include <map> 
using namespace std; 
map<long long, long long> coll; 

long loopLength(const long long* right){
    long length = 1;
    long long current = *right;
    while(current > 1){
        if(current % 2 == 0){
            current /= 2;
        }
        else{ 
            current = current * 3 + 1;
        }
        length++;
    }
    return length;
}

long loopLength_speedup(const long long* right){ 
    long long length = 0;
    map<long long, long long>::iterator it = coll.find(*right);
    if(it == coll.end()){ 
        length = loopLength(right);
        coll[*right] = length;
    }
    else{ 
        length = it->second;
    }
    return length;
}


int maxLength(const long long* left, const long long* right){ 
    long long min = *left < *right ? *left : *right;
    long long max = *left > *right ? *left : *right;
        
    long long current = min;
    int maxLength = 0;
    while(current <= max){ 
        int length = loopLength_speedup(&current);
        maxLength = length > maxLength ? length : maxLength;
        current++;
    }
    return maxLength;
}


int main(){ 
    long long left, right;
    while(cin >> left >> right){ 
        cout << left << " " << right << " " << maxLength(&left, &right) << endl;
    }
    return 0;
}
