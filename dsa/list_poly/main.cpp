#include "list.h"
#include <cstdio>

int main(int argc, char** argv)
{
    // Get Polynomial

    // Data
    int length = 3;
    int coe[length] = {1,1,1};
    int exp[length] = {2,1,0};
    int coe2[length] = {1,1,1};
    int exp2[length] = {2,1,0};
    List l1 = CreateList(length, coe, exp);
    List l2 = CreateList(length, coe2, exp2);

    // Calculate
    List l3 = NULL;
    AddPolynomial(l1, l2, l3); 
    List l4 = NULL;
    MultiPolynomial(l1, l2 ,l4);

    // Print
    PrintList(l3);
    printf("%d\n", Length(l3));
    PrintList(l4);
    printf("%d\n", Length(l4));
   
     

    // Copy Test
    //List lCopy = NULL;
    //Copy(l3, lCopy);
    //PrintList(lCopy);
    //printf("%d\n", Length(lCopy));

    // Release Test
    //Release(lCopy);
    //printf("%d\n", lCopy);

    return 0;
}

