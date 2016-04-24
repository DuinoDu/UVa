#ifndef _LIST_H
#define _LIST_H

struct Node;
typedef struct Node *PtrToNode;
typedef PtrToNode List;
typedef PtrToNode Position;
typedef int ElementType;


List MakeEmpty( List L );
int IsEmpty( List L );
int IsLast( Position P, List L);
Position Find( ElementType X, List L);
void Delete( ElementType X, List L);
Position FindPrevious( ElementType X, List L);
void Insert( ElementType X, List L, Position P);
void DeleteList( List L);
Position First( List L);
Position Last(List L);
Position Next(Position P);
void Append(ElementType X, List L);
void SetValue(Position P, ElementType X);
void PrintList(List L);
void PrintElement(Position P);


#endif
