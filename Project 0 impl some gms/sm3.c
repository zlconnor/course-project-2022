
#include "sm3.h"



unsigned int left_cycle_shift(unsigned int val, unsigned int n)//cycle shift left
{
	n = n % 32;
	return ((val << n) & 0xFFFFFFFF) | ((val & 0xFFFFFFFF) >> (32 - n));
}


void init_T()                   //initialize the T array
{
	for (int j = 0; j <= 15; j++)
	{
		T[j] = 0x79cc4519;
	}
	for (int j = 16; j <= 63; j++)
	{
		T[j] = 0x7a879d8a;
	}
}

unsigned int FF(unsigned int X, unsigned int Y, unsigned int Z, int j)
{
	unsigned int ret = 0;
	if (j >= 0 && j <= 15)
	{
		ret = X ^ Y ^ Z;
	}
	else if (j >= 16 && j <= 63)
	{
		ret = (X & Y) | (X & Z) | (Y & Z);
	}
	return ret;
}



unsigned int GG(unsigned int X, unsigned int Y, unsigned int Z, int j)
{
	unsigned int ret = 0;
	if (j >= 0 && j <= 15)
	{
		ret = X ^ Y ^ Z;
	}
	else if (j >= 16 && j <= 63)
	{
		ret = (X & Y) | ((~X) & Z);
	}
	return ret;
}

unsigned int P_0(unsigned int X)
{
	return X ^ left_cycle_shift(X, 9) ^ left_cycle_shift(X, 17);
}

unsigned int P_1(unsigned int X)
{
	return X ^ left_cycle_shift(X, 15) ^ left_cycle_shift(X, 23);
}


void CF(unsigned char* Bi) //compress func
{
	unsigned int W[68];
	unsigned int W_p[64];
	for (int j = 0; j <= 15; j++)
	{
		W[j] = Bi[4 * j + 0] << 24 | Bi[4 * j + 1] << 16 | Bi[4 * j + 2] << 8 | Bi[4 * j + 3];
	}
	for (int j = 16; j <= 67; j++)
	{
		W[j] = P_1(W[j - 16] ^ W[j - 9] ^ left_cycle_shift(W[j - 3], 15)) ^ left_cycle_shift(W[j - 13], 7) ^ W[j - 6];
	}
	for (int j = 0; j <= 63; j++)
	{
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
	for (int j = 0; j <= 63; j++)
	{
		SS1 = left_cycle_shift((left_cycle_shift(A, 12) + E + left_cycle_shift(T[j], j % 32)) & 0xffffffff, 7);//modulo 32

		SS2 = SS1 ^ left_cycle_shift(A, 12);
		TT1 = (FF(A, B, C, j) + D + SS2 + W_p[j]) & 0xffffffff;//modulo 32
		TT2 = (GG(E, F, G, j) + H + SS1 + W[j]) & 0xffffffff;//modulo 32
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

void init_IV()//initialize IV 32*8 256bit
{

	IV[0] = 0x7380166f;
	IV[1] = 0x4914b2b9;
	IV[2] = 0x172442d7;
	IV[3] = 0xda8a0600;
	IV[4] = 0xa96f30bc;
	IV[5] = 0x163138aa;
	IV[6] = 0xe38dee4d;
	IV[7] = 0xb0fb0e4e;
}

void block_and_compress(unsigned char* m, int len) {//block and then into compress func
	int byte_remain = 0;
	unsigned long long bit_length = 0;

	for (int i = 0; i < len / 64; i++) {//get len/64 blocks
		memcpy(B, m + i * 64, 64);
		CF(B);
	}

	bit_length = len * 8;
	byte_remain = len % 64;
	memset(&B[byte_remain], 0, 64 - byte_remain);
	memcpy(B, m + (len/64)*64, byte_remain);
	B[byte_remain] = 0x80;
	if (byte_remain <= 55) {//padding and compression <=448
		for (int i = 0; i < 8; i++)
			B[56 + i] = (bit_length >> ((8 - 1 - i) * 8)) & 0xFF;
		CF(B);
	}
	else {
		CF(B); //>48 CF(B), then pad and CF(B)
		memset(B, 0, 64);
		for (int i = 0; i < 8; i++)
			B[56 + i] = (bit_length >> ((8 - 1 - i) * 8)) & 0xFF;
		CF(B);
	}

}


void char2hex() {
	for (int i = 0; i < 8; i++) {
		printf("%08x ", IV[i]);
	}
	printf("\n");
}

void char2str(unsigned char* value) {
	for (int i = 0; i < 8; i++) {
		value[4 * i] = (IV[i] >> 24) & 0xff;
		value[4 * i + 1] = (IV[i] >> 16) & 0xff;
		value[4 * i + 2] = (IV[i] >> 8) & 0xff;
		value[4 * i + 3] = IV[i] & 0xff;
	}
	for (int i = 0; i < 32; i++)
		printf("%c", value[i]);
	printf("\n");
}

int SM3(unsigned char* m, unsigned int len, unsigned char* hash_val)
{
	init_IV();
	init_T();
	block_and_compress(m, len);
	char2hex();
	char2str(hash_val);
	return 1;
}