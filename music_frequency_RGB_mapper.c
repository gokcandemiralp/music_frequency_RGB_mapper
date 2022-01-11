#include <stdio.h>
#include <stdlib.h>
#include <math.h>

// takes the sine value converts into 8 bit color value
unsigned char saturate(float temp_color){
    if(temp_color<0){return 0;}
    else if(temp_color>1){return 255;}
    else{return (unsigned char) 255*temp_color;}
}

void frequency_mapper(float freq){
    float temp_R, temp_G, temp_B;
    unsigned char R, G, B;
    float temp_log;

    temp_log = 2*M_PI*(log2f(freq/20.6025));    //measuring relative to E note

    temp_R = 0.5+sinf(11*(M_PI_2/3)+ temp_log); //120 degrees out of faze from each other
    R = saturate(temp_R); /* for C note */

    temp_G = 0.5+sinf(7*(M_PI_2/3)+ temp_log);  //120 degrees out of faze from each other
    G = saturate(temp_G); /* for G# note */

    temp_B = 0.5+sinf(M_PI_2 + temp_log);       //120 degrees out of faze from each other
    B = saturate(temp_B); /* for E note */

    printf("R:%f    G:%f    B:%f\n",temp_R,temp_G,temp_B);
    printf("R:%d    G:%d    B:%d",R,G,B);
}

int main(){
    frequency_mapper(174.61);
    return 0;
}