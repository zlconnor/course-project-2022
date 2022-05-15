#pragma once
#include<stdio.h>
#include<stdlib.h>
#include<malloc.h>

static unsigned int IV[8] = { 0 };//initial vector
static unsigned int T[64] = { 0 };//T array
static unsigned char B[64] = { 0 };//block B(i)

unsigned int left_cycle_shift(unsigned int val, unsigned int n);
void init_T();
void init_IV();
unsigned int FF(unsigned int X, unsigned int Y, unsigned int Z, int j);
unsigned int GG(unsigned int X, unsigned int Y, unsigned int Z, int j);
unsigned int P_0(unsigned int X);
unsigned int P_1(unsigned int X);
void CF(unsigned char* Bi);
void block_and_compress(unsigned char* m, int len);
void char2hex();
void char2str(unsigned char* value);
int SM3(unsigned char* m, unsigned int len, unsigned char* hash_val);
