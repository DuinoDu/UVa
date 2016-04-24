#include "list.h"
#include <cstdio>

int main()
{
    printf("hello\n");
    List l = NULL;
    l = MakeEmpty(l);
    int i = 10;
    while(i){
        Append(i, l);
        i--; 
    }
    PrintList(l);

    Position p = Last(l);
    PrintElement(p);
    return 0;
}
