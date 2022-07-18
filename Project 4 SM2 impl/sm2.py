# SM2 impl
# 参数定义
import math
params={
    'p':'FFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF00000000FFFFFFFFFFFFFFFF',
    'a':'FFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF00000000FFFFFFFFFFFFFFFC',
    'b':'28E9FA9E9D9F5E344D5A9E4BCF6509A7F39789F515AB8F92DDBCBD414D940E93',
    'n':'FFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFF7203DF6B21C6052B53BBF40939D54123',
    'xg':'32C4AE2C1F1981195F9904466A39C9948FE30BBFF2660BE1715A4589334C74C7',
    'yg':'BC3736A2F4F6779C59BDCEE36B692153D0A9877CC62A474002DF32E52139F0A0'
}
# 有限域上的椭圆曲线在点加运算下构成优先交换群 阶与基域规模相近
# 倍点运算构成单向函数 多倍点与基点 椭圆曲线离散对数问题

# 4.2数据类型转换
# 4.2.2 整数到字节串
# input:非负整数x和字节串目标长度k
# output:长度为k的字节串M
def int2bytes(x,k):
    M=[]
    # 每次取出最低8位并右移8位 高位补0
    for i in range(0,k):
        M.append(x>>(i*8)&0xff)
    M.reverse()
    return M

# 4.2.3 字节串到整数
# input:长度为k的字节串M
# output:整数x
def bytes2int(M):
    x=0
    for b in M:
        # 对每一个字节左移8位并加上新的字节串对应的整数值
        x=x*256+int(b)
    return x
# 4.2.4 比特串到字节串
# input:长度为k的字节串M
def bits_to_bytes(s):
	if s[0:2] == '0b':
		s = s[2:]
		m = len(s)
		k = math.ceil(m/8)
		M = []
		for i in range(0, k):
			temp = ''
			j = 0
			while j < 8:
				if(8*i+j >= m):
					temp = temp + '0'
				else:
					temp = temp + s[m-(8*i+j)-1:m-(8*i+j)]
				j = j + 1
			temp = temp[::-1]
			temp = int(temp, 2)
			M.append(temp)
			#M = M + temp
		M.reverse()
	else:
		return -1;
	return M


# 字节串到比特串
def bytes2bits(M):
    k=len(M)
    m=8*k
    tmp=''
    s=0
    M.reverse()
    j=0
    for i in M:
        s+=i*pow(256,j)
        j+=1
    s=bin(s)




# 域元素到字节串
# 字节串到域元素
# 域元素到整数
# 点到字节串
# 字节串到点

# 椭圆曲线上的点运算
# 倍乘


if __name__ == '__main__':
    print(params)