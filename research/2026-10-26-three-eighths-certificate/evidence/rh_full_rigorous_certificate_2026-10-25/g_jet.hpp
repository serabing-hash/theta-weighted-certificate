#pragma once
#include "../mpfr_backend/interval.hpp"
#include <array>
namespace gcert {
using directed::I;
struct Jet { std::array<I,7> c; Jet(){} Jet(const I&a){c[0]=a;} Jet(int a):Jet(I(a)){} static Jet var(const I&a){Jet z(a);z.c[1]=I(1);return z;} };
inline Jet operator+(const Jet&a,const Jet&b){Jet z;for(int n=0;n<7;n++)z.c[n]=a.c[n]+b.c[n];return z;}
inline Jet operator-(const Jet&a){Jet z;for(int n=0;n<7;n++)z.c[n]=-a.c[n];return z;}
inline Jet operator-(const Jet&a,const Jet&b){return a+-b;}
inline Jet operator*(const Jet&a,const Jet&b){Jet z;for(int n=0;n<7;n++)for(int k=0;k<=n;k++)z.c[n]+=a.c[k]*b.c[n-k];return z;}
inline Jet inv(const Jet&a){Jet z;z.c[0]=I(1)/a.c[0];for(int n=1;n<7;n++){for(int k=1;k<=n;k++)z.c[n]-=a.c[k]*z.c[n-k];z.c[n]/=a.c[0];}return z;}
inline Jet operator/(const Jet&a,const Jet&b){return a*inv(b);}
inline Jet exp(const Jet&a){Jet z;z.c[0]=directed::exp(a.c[0]);for(int n=1;n<7;n++){for(int k=1;k<=n;k++)z.c[n]+=I(k)*a.c[k]*z.c[n-k];z.c[n]/=I(n);}return z;}
inline Jet cosh(const Jet&a){return (exp(a)+exp(-a))/Jet(2);}
inline I cosh(const I&a){return (directed::exp(a)+directed::exp(-a))/I(2);}
inline I sinh(const I&a){return (directed::exp(a)-directed::exp(-a))/I(2);}
}
