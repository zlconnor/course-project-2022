#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include<malloc.h>
/*
梳理一下算法过程
1. 填充m->m'
2. 分组m'->B[0]...B[n-1] 512bit一组
3. 迭代压缩 V(i+1)=CF(V[i],B[i])


*/


static unsigned int IV[8];
static unsigned int T[64];
void init_IV() {
    IV[0] = 0x7380166f;
    IV[1] = 0x4914b2b9;
    IV[2] = 0x172442d7;
    IV[3] = 0xda8a0600;
    IV[4] = 0xa96f30bc;
    IV[5] = 0x163138aa;
    IV[6] = 0xe38dee4d;
    IV[7] = 0xb0fb0e4e;
}
void init_T() {
    int j = 0;
    for (j = 0; j <= 15; j++) {
        T[j] = 0x79cc4519;
    }
    for (j = 16; j <= 63; j++) {
        T[j] = 0x7a879d8a;
    }
}
unsigned int FF(unsigned int X, unsigned int Y, unsigned int Z, int j) {
    int ret = 0;
    if (j >= 0 && j <= 15) {
        ret = X ^ Y ^ Z;
    }
    else if (j >= 16 && j <= 63) {
        ret = (X & Y) | (X ^ Z) | (Y ^ Z);
    }
    return ret;
}
unsigned int GG(unsigned int X, unsigned int Y, unsigned int Z, int j) {
    int ret = 0;
    if (j >= 0 && j <= 15) {
        ret = X ^ Y ^ Z;
    }
    else if (j >= 16 && j <= 63) {
        ret = (X & Y) | (~X | Z);
    }
    return ret;
}
unsigned int left_cycle_shift(unsigned int value, int n) {
    return (value >> (32 - n)) | (value << n);
}
unsigned int P_0(unsigned int X) {
    return X ^ left_cycle_shift(X, 9) ^ left_cycle_shift(X, 17);
}
unsigned int P_1(unsigned int X) {
    return X ^ left_cycle_shift(X, 15) ^ left_cycle_shift(X, 23);
}
void reverse_by_byte(char* const le, int len) {
    for (int i = 0; i < len >> 1; i++) {
        char tmp = le[i];
        le[i] = le[len - 1 - i];
        le[len - 1 - i] = tmp;
    }
}

//借鉴 好好考虑一下
char* padding(char* src, int src_len, int content_len, int* out_len) {
    int l = sizeof(char) * src_len << 3;//m的原始长度bit
    int content_bit_len = sizeof(char) * content_len << 3;
    int k = (448 - ((l % 512) + 1) + 512) % 512;//需要补充的长度bit
    int len_aft_padding = l + 1 + 64 + k;//padding后的长度bit

    char* result = (char*)malloc(sizeof(char) * len_aft_padding / 8);
    memset(result, 0, sizeof(result));
    memcpy(result, src, sizeof(char) * src_len);
    char one = 0x80;
    result[src_len] = one;

    char* big_content_bit_len = (char*)malloc(sizeof(char) << 3);
    memcpy(big_content_bit_len, &content_bit_len, 8);
    reverse_by_byte(big_content_bit_len, 8);
    memcpy(&result[len_aft_padding - 8], big_content_bit_len, 8);
    free(big_content_bit_len);
    if (out_len != NULL) {
        *out_len = len_aft_padding;
    }
    return result;
}
void msg_expansion(char* Bi) {
    unsigned int W[64];
    unsigned int W_p[64];
    for (int j = 0; j < 16; j++) {
        W[j] = Bi[4 * j + 0] << 24 | Bi[4 * j + 1] << 16 | Bi[4 * j + 2] << 8 | Bi[4 * j + 3];
    }
    for (int j = 16; j < 68; j++) {
        W[j] = P_1(W[j - 16] ^ W[j - 9] ^ left_cycle_shift(W[j - 3], 15)) ^ left_cycle_shift(W[j - 13], 7) ^ W[j - 6];
    }
    for (int j = 0; j < 64; j++) {
        W_p[j] = W[j] ^ W[j + 4];
    }


}

    //分组
void block(char* m_p, int l, int k) {
    init_IV();
    for (int i = 0; i < (l + k + 65) / 512; i++) {
        CF(m_p + 512 * i);
    }
}



void CF(char* Bi) {
    unsigned int W[64];
    unsigned int W_p[64];
    for (int j = 0; j < 16; j++) {
        W[j] = Bi[4 * j + 0] << 24 | Bi[4 * j + 1] << 16 | Bi[4 * j + 2] << 8 | Bi[4 * j + 3];
    }
    for (int j = 16; j < 68; j++) {
        W[j] = P_1(W[J - 16] ^ W[j - 9] ^ left_cycle_shift(W[j - 3], 15)) ^ left_cycle_shift(W[j - 13], 7) ^ W[j - 6];
    }
    for (int j = 0; j < 64; j++) {
        W_p[j] = W[j] ^ W[j + 4];
    }
    unsigned int A = IV[0];
    unsigned int B = IV[1];
    unsigned int C = IV[2];
    unsigned int D = IV[3];
    unsigned int E = IV[4];
    unsigned int F = IV[5];
    unsigned int G = IV[6];
    unsigned int H = IV[7];
    unsigned int SS1;
    unsigned int SS2;
    unsigned int TT1;
    unsigned int TT2;
    for (int j = 0; j < 64; j++) {
        SS1 = left_cycle_shift(A, 12) + E + left_cycle_shift(left_cycle_shift(T[i], j % 32), 7);
        SS2 = SS1 ^ left_cycle_shift(A, 12);
        TT1 = FF(A, B, C, i) + D + SS2 + W_p[i];
        TT2 = GG(E, F, G, i) + H + SS1 + W[i];
        D = C;
        C = left_cycle_shift(B, 9);
        B = A;
        A = TT1;
        H = G;
        G = left_cycle_shift(F, 19);
        F = E;
        E = P_0(TT2);
    }
    IV[0] = A ^ IV[0];
    IV[1] = B ^ IV[1];
    IV[2] = C ^ IV[2];
    IV[3] = D ^ IV[3];
    IV[4] = E ^ IV[4];
    IV[5] = F ^ IV[5];
    IV[6] = G ^ IV[6];
    IV[7] = H ^ IV[7];
}







