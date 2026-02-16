#include <iostream>
#include <string>
using namespace std;

class Calculator {
private:
    string name;

public:
    Calculator(string n) : name(n) {}
    
    int add(int a, int b) {
        return a + b;
    }
    
    int multiply(int a, int b) {
        return a * b;
    }
    
    void displayName() {
        cout << "Calculator: " << name << endl;
    }
};

int main() {
    Calculator calc("MyCalc");
    calc.displayName();
    cout << "5 + 3 = " << calc.add(5, 3) << endl;
    cout << "5 * 3 = " << calc.multiply(5, 3) << endl;
    return 0;
}
