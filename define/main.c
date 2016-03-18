/*************************************************************************
	> File Name: main.c
	> Author: 
	> Mail: 
	> Created Time: Mon 06 Jul 2015 04:44:15 PM CST
 ************************************************************************/

#include<stdio.h>
#define BEFORE_TIME\
    int beforeTime = 10;

#define AFTER_TIME\
    int afterTime=1;\
    printf("%d\n", (afterTime-beforeTime));
int main()
{
    BEFORE_TIME
    AFTER_TIME

    return 0;
}
