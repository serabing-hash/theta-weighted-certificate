#pragma once
#include "../mpfr_backend/interval.hpp"
#include <array>
using namespace directed;
struct J {std::array<I,5> c; J(){} J(const I&a){c[0]=a;} J(int a):J(I(a)){} static J var(const I&a){J z(a);z.c[1]=I(1);return z;} };
inline J operator+(const J&a,const J&b){J z;for(int k=0;k<5;k++)z.c[k]=a.c[k]+b.c[k];return z;}
inline J operator-(const J&a){J z;for(int k=0;k<5;k++)z.c[k]=-a.c[k];return z;}
inline J operator-(const J&a,const J&b){return a+-b;}
inline J operator*(const J&a,const J&b){J z;for(int n=0;n<5;n++)for(int k=0;k<=n;k++)z.c[n]+=a.c[k]*b.c[n-k];return z;}
inline J inv(const J&a){J z;z.c[0]=I(1)/a.c[0];for(int n=1;n<5;n++){for(int k=1;k<=n;k++)z.c[n]-=a.c[k]*z.c[n-k];z.c[n]/=a.c[0];}return z;}
inline J operator/(const J&a,const J&b){return a*inv(b);}
inline J exp(const J&a){J z;z.c[0]=exp(a.c[0]);for(int n=1;n<5;n++){for(int k=1;k<=n;k++)z.c[n]+=I(k)*a.c[k]*z.c[n-k];z.c[n]/=I(n);}return z;}
inline J log(const J&a){J z;z.c[0]=log(a.c[0]);J d;for(int k=0;k<4;k++)d.c[k]=I(k+1)*a.c[k+1];J q=d*inv(a);for(int n=1;n<5;n++)z.c[n]=q.c[n-1]/I(n);return z;}
inline J powi(J a,unsigned n){J z(1);while(n){if(n&1)z=z*a;n>>=1;if(n)a=a*a;}return z;}
inline J cosh(const J&a){return (exp(a)+exp(-a))/J(2);}
inline J sinh(const J&a){return (exp(a)-exp(-a))/J(2);}
inline I cosh(const I&a){return (exp(a)+exp(-a))/I(2);}
inline I sinh(const I&a){return (exp(a)-exp(-a))/I(2);}
