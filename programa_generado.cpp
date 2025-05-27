#include <iostream>
#include <string>
using namespace std;
int main() {
    int goles;
    int i;
    char inicial;
    bool leyenda;
    string nombre;
    float promedio;
    auto t18;
    auto t2;
    auto t22;
    auto t28;
    auto t40;
    auto t44;
    auto t48;
    auto t50;
    auto t52;
    auto t54;
    auto t56;
    auto t58;
    auto t60;
    auto t62;
    int x;
    goles = 10;
    promedio = 7.5;
    inicial = 'M';
    leyenda = true;
    nombre = "Messi";
    goles = goles + 5;
    // INICIO WHILE;
    t2 = goles > 10;
    // INICIO WHILE;
    while (!(t2)) {
        promedio = promedio + 0.5;
        goles = goles - 1;
        promedio = promedio + 0.5;
        goles = goles - 1;
        promedio = promedio + 0.5;
        goles = goles - 1;
        promedio = promedio + 0.5;
        goles = goles - 1;
        promedio = promedio + 0.5;
        goles = goles - 1;
    } // FIN while
    // FIN WHILE;
    // INICIO IF;
    t18 = goles > 11;
    // INICIO WHILE;
    while (!(t18)) {
        promedio = promedio + 1.0;
    } // FIN while
    // ELSE;
    promedio = promedio - 0.5;
    // FIN IF;
    i = 0;
    //INICIO DO-WHILE;
    i = i + 1;
    t22 = i < 5;
    // INICIO WHILE;
    while ((t22)) {
        //FIN DO-WHILE;
        // SWITCH_START goles;
        // CASE 10;
        promedio = promedio + 2.0;
    } // FIN while
    // BREAK;
    // CASE 15;
    promedio = promedio + 5.0;
    // BREAK;
    // DEFAULT;
    promedio = 0;
    // SWITCH_END;
    goles = goles + 5;
    // INICIO WHILE;
    t28 = goles > 10;
    // INICIO WHILE;
    while (!(t28)) {
        goles = goles - 1;
        goles = goles - 1;
        goles = goles - 1;
        goles = goles - 1;
        goles = goles - 1;
    } // FIN while
    // FIN WHILE;
    // INICIO IF;
    t40 = goles > 11;
    // INICIO IF;
    if (!(!(t40))) {
        // ELSE;
        promedio = promedio - 0.5;
        // FIN IF;
        i = 0;
        //INICIO DO-WHILE;
        i = i + 1;
        t44 = i < 5;
        // INICIO WHILE;
        while ((t44)) {
            //FIN DO-WHILE;
            // SWITCH_START goles;
            // CASE 10;
            promedio = promedio + 2.0;
        } // FIN while
        // BREAK;
        // CASE 15;
        promedio = promedio + 5.0;
    } // FIN if
    // BREAK;
    // DEFAULT;
    promedio = 0;
    // SWITCH_END;
    x = 0;
    // INICIO FOR;
    t48 = x < 3;
    // INICIO IF;
    if (!(t48)) {
        x = x + 1;
        t50 = x < 3;
        // INICIO IF;
        if (!(t50)) {
        } // FIN if
        x = x + 1;
        t52 = x < 3;
        // INICIO IF;
        if (!(t52)) {
        } // FIN if
        x = x + 1;
        t54 = x < 3;
        // INICIO WHILE;
        while (!(!(t54))) {
            // FIN FOR;
            x = 0;
            // INICIO FOR;
            t56 = x < 3;
            // INICIO IF;
            if (!(t56)) {
                x = x + 1;
                t58 = x < 3;
                // INICIO IF;
                if (!(t58)) {
                } // FIN if
                x = x + 1;
                t60 = x < 3;
                // INICIO IF;
                if (!(t60)) {
                } // FIN if
                x = x + 1;
                t62 = x < 3;
                // INICIO WHILE;
                while (!(!(t62))) {
                    // FIN FOR;
                } // FIN while
            } // FIN if
        } // FIN while
    } // FIN if
    return 0;
}