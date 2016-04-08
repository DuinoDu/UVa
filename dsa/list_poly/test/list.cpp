#include "list.h"
#include <cstdio>
#include <cstdlib>
#include <cassert>

struct Node{
    int Coefficient;
    int Exponent;
    PtrToNode Next;
};


List CreateList(int length, CoeType* coe, ExpType* exp){
    List L = NULL;
    Position P = NULL;
    Position Last = NULL;
    int i = 0;
    while(i < length){
        P = (Position)malloc(sizeof(struct Node));
        assert(P!=NULL);
        P->Coefficient = coe[i];
        P->Exponent = exp[i];
        P->Next = NULL; // this potential error is discovered by unittest. 
        if(i==0){
            L=P;
        }else{
            Last->Next = P;
        }
        Last = P;
        i++;
    }
    return L;
}


void Insert(ExpType X, CoeType C, List L, Position P){
    Position Cell = (Position)malloc(sizeof(struct Node));
    assert(Cell!=NULL);
    Cell->Exponent = X;
    Cell->Coefficient = C;   
    Cell->Next = P->Next;
    P->Next = Cell; 
}

void Append(ExpType X, CoeType C, List L){
    Insert(X, C, L, Last(L));
}

Position Find(ExpType X, List L){
    assert(L!=NULL);
    Position P = L;
    while(P->Next!=NULL && P->Exponent!=X){
        P = P->Next;
    }
    return P;
}

Position FindPrevious(ExpType X, List L){
    Position P = L;

    while(P!=NULL && P->Next->Exponent!=X){
        P = P->Next;
    }
    return P;
}

void Delete(ExpType X, List L){
    Position Previous = FindPrevious(X, L);
    if(Previous->Next==NULL){
        return;
    }
    Position Tmp = Previous->Next;
    Previous->Next = Tmp->Next;
    free(Tmp);
}


Position First(List L){
    assert(L!=NULL);
    return L;
}

Position Last(List L){
    assert(L!=NULL);
    Position P = L;
    while(P->Next != NULL){ 
        P = P->Next;
    }
    return P;
}

bool IsLast(ExpType X, List L){
    Position P = Find(X, L);            
    if(P!=NULL){
        return P->Next == NULL;
    }
    return false;
}

void PrintList(List L){
    Position P = L;
    assert(P!=NULL);
    while(P!=NULL){
        printf("%d%s%d%s",P->Coefficient, "exp(",P->Exponent,") ");
        P = P->Next;
    }
    printf("\n");
}


void Copy(const List src, List &dst){
    Position pSrc = src;
    Position item;
    Position previous = NULL;
    while(pSrc!=NULL){
        item = (Position)malloc(sizeof(struct Node));
        item->Exponent = pSrc->Exponent;
        item->Coefficient = pSrc->Coefficient;
        if(previous!=NULL){
            previous->Next = item;
        }else{
            dst = item;
        }
        previous = item;
        pSrc = pSrc->Next;
    }
}


void Release(List &L){
    if(L==NULL)
        return;
    Position P = L->Next;
    Position Tmp = NULL;
    while(P!=NULL){
        Tmp = P->Next;
        free(P);
        P = Tmp;
    }
    free(L);
    L = NULL;
}


int Length(const List L){
    Position P = L;
    int length = 0;
    while(P!=NULL){
        P = P->Next;
        length++;
    }
    return length;
}


void GetCoe(const List L, int *coe){
    assert(L!=NULL);
    Position P = L;
    while(P!=NULL){
        *coe = P->Coefficient;
        P = P->Next;
        ++coe;
    }
}
void GetExp(const List L, int *exp){
    assert(L!=NULL);
    Position P = L;
    while(P!=NULL){
        *exp = P->Exponent;
        P = P->Next;
        ++exp;
    }
}


void AddPolynomial(const List l1, const List l2, List &l3){
    Position p1 = l1;
    Position p2 = l2;
    Position previous = l3; 
    Position item = l3;
   
    while(p1!=NULL || p2!=NULL){
        item = (List)malloc(sizeof(struct Node));
        assert(item!=NULL); 
        // add each in l1 and l2, save in item
        if(p1!=NULL && p2!=NULL){
            if(p1->Exponent == p2->Exponent){
                item->Exponent = p1->Exponent;
                item->Coefficient = p1->Coefficient + p2->Coefficient;
                p1 = p1->Next;
                p2 = p2->Next;
            }
            else if(p1->Exponent > p2->Exponent){
                item->Exponent = p1->Exponent;
                item->Coefficient = p1->Coefficient;
                p1 = p1->Next;
            }else{
                item->Exponent = p2->Exponent;
                item->Coefficient = p2->Coefficient;
                p2 = p2->Next;
            }
        }else if(p1!=NULL){
            item->Exponent = p1->Exponent;
            item->Coefficient = p1->Coefficient;
            p1 = p1->Next;
        }else if(p2!=NULL){
            item->Exponent = p2->Exponent;
            item->Coefficient = p2->Coefficient;
            p2 = p2->Next;
        }
        item->Next = NULL;

        // if is not fisrt
        if(previous!=NULL){
            previous->Next = item;
        }// if first, keep l3 = begin of the List
        else{
            l3 = item;
        }
        previous = item;   
    }
}


void MultiPolynomial(const List l1, const List l2, List &l3){
    int l1Len = Length(l1);
    int l2Len = Length(l2);
    int coe[l1Len][l2Len];
    int exp[l1Len][l2Len];
   
    int i,j;
    for(i=0;i<l1Len;++i){
        for(j=0;j<l2Len;++j){
            coe[i][j] = 0;
            exp[i][j] = 0;
        }
    }

    List pList[l1Len] = {0};
    Position p1 = l1;
    Position p2 = l2;
    int cnt1 = 0;
    int cnt2 = 0;
    while(p1!=NULL) {
        while(p2!=NULL){
            coe[cnt1][cnt2] = p1->Coefficient * p2->Coefficient;
            exp[cnt1][cnt2] = p1->Exponent + p2->Exponent;
            p2 = p2->Next;
            ++cnt2;
            assert( cnt2 <= l2Len );
        }
        cnt2=0;
        // save each result in pList.    
        pList[cnt1] = CreateList(l2Len, coe[cnt1], exp[cnt1]);
        p2 = l2;
        p1 = p1->Next;
        cnt1++;
        assert( cnt1 <= l1Len );
    } 

    AddPolynomial(pList[0], pList[1], l3);
    int cnt3 = 2;
    List tmp = NULL;
    while(cnt3 < l1Len){
        AddPolynomial(l3, pList[cnt3], tmp);
        Copy(tmp, l3);
        Release(tmp); 
        cnt3++;
    } 
}

