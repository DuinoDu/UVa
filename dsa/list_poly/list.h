#ifndef _LIST_H
#define _LIST_H

struct Node;
typedef struct Node *PtrToNode;
typedef PtrToNode List;
typedef PtrToNode Position;
typedef int ExpType;
typedef int CoeType;

List CreateList(int length, CoeType* coe, ExpType* exp);
void Insert(ExpType X, CoeType C, List L, Position P);
void Append(ExpType X, CoeType C, List L);
Position Find(ExpType X, List L);
Position FindPrevious(ExpType X, List L);
void Delete(List L, Position P);
Position First(List L);
Position Last(List L);
bool IsLast(ExpType  X, List L);
void PrintList(List L);
void Copy(const List src, List &dst);
void Release(List &L);
int Length(const List L);
void GetCoe(const List L, int *coe);
void GetExp(const List L, int *exp);

void AddPolynomial(const List l1, const List l2, List &l3);
void MultiPolynomial(const List l1, const List l2, List &l3);

#endif

