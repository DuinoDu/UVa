#include "list.h"
#include <cassert>
#include <cstdio>
#include <cstdlib>

struct Node
{
    ElementType Element;
    Position Next;    
};

List MakeEmpty( List L ){
    if(L!=NULL){
        DeleteList(L);
    }
    L = (List)malloc(sizeof(struct Node));
    assert(L!=NULL);
    L->Next = NULL;
    return L;
}


int IsEmpty( List L ){
    return L->Next == NULL;
}


int IsLast( Position P, List L){
   return P->Next == NULL; 
}

// if X is the first element of L, will it break down?
Position Find( ElementType X, List L){
    assert(L);
    Position P;
    P = L->Next;
    while( P!=NULL && P->Element!=X )
         P = P->Next;   
    return P;
}


void Delete( ElementType X, List L){
    Position P = FindPrevious(X, L);
    Position TmpCell;
    if( !IsLast(P, L) ){
        TmpCell = P->Next;
        P->Next = TmpCell->Next;
        free(TmpCell);
    }
}


Position FindPrevious( ElementType X, List L){
    Position P = L;
    while( P->Next!=NULL && P->Next->Element!=X){
        P = P->Next;
    }
    return P;
}


void Insert( ElementType X, List L, Position P){
    Position TmpCell = (Position)malloc(sizeof(struct Node));
    assert(TmpCell!=NULL);   
    TmpCell->Element = X;
    TmpCell->Next = P->Next;
    P->Next = TmpCell;
}


void DeleteList( List L){
    Position P, Tmp;
    P = L->Next;
    while(P!=NULL){
        Tmp = P->Next;
        free(P);
        P = Tmp;
    }
    L->Next = NULL;
    L->Element = 0;
}



Position First( List L){
    return L;
}

Position Last(List L){
    Position P = L;
    while(P->Next!=NULL){
        P = P->Next;
    }
    return P;
}


Position Next(Position P){
    return P->Next;
}

void Append(ElementType X, List L){
    Position P = Last(L);
    Insert(X, L, P);
}



void SetValue(Position P, ElementType X){
    P->Element = X;
}


void PrintList(List L){
    if(L!=NULL){
        Position P = L;
        while(P->Next!=NULL){
            printf("%d\t",P->Element); 
            P = P->Next;
        }
        printf("%d\t",P->Element); 
        printf("\n");   
    }
}


void PrintElement(Position P){
    if(P!=NULL){
        printf("P is not null\n");
        printf("%d\n", P->Element);
    }
}


/*
 * Test


int main()
{
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
    p->Element = 100;
    PrintElement(p);
    return 0;
}
*/
