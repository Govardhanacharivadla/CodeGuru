#include <stdio.h>
#include <stdlib.h>

typedef struct {
    int x;
    int y;
} Point;

int add(int a, int b) {
    return a + b;
}

int subtract(int a, int b) {
    return a - b;
}

Point* createPoint(int x, int y) {
    Point* p = (Point*)malloc(sizeof(Point));
    p->x = x;
    p->y = y;
    return p;
}

void printPoint(Point* p) {
    printf("Point(%d, %d)\n", p->x, p->y);
}

int main() {
    int sum = add(10, 5);
    int diff = subtract(10, 5);
    
    printf("Sum: %d\n", sum);
    printf("Difference: %d\n", diff);
    
    Point* p = createPoint(3, 4);
    printPoint(p);
    free(p);
    
    return 0;
}
