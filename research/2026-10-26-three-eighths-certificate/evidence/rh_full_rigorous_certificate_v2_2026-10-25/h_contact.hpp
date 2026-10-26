#pragma once
// Static follow-up helper; never patch a running/frozen certificate with this file.
// Proof: ../rh_endpoint_contact_jet_sharpening_2026-10-25.md.
#include "jet.hpp"

namespace contact_jet_detail {
inline I binomial(unsigned n,unsigned j){
    if(j>n)return I(0);
    I b(1);
    for(unsigned r=1;r<=j;r++)b=b*I(static_cast<long>(n-r+1))/I(static_cast<long>(r));
    return b;
}

// Bound the normalized u-derivative of the omitted regular series, k>=5.
// Both arguments are interval enclosures of positive exact quantities.
inline I tail_bound(const I& L,const I& u,unsigned j){
    if(j>4)throw std::runtime_error("contact tail derivative outside certified range");
    I a=upperpoint(L),b=upperpoint(u);
    I q=square(a/I(6))*powi(b,16);
    I ratio=q*powi(I(96)/I(static_cast<long>(81-j)),j);
    if(!strictly_less(ratio,I(1)))throw std::runtime_error("contact derivative tail ratio not below one");
    I first=I(2)/I(5)*powi(a/I(6),10)*binomial(80,j)*powi(b,80-j);
    return upperpoint(first/(I(1)-ratio));
}
}

// Normalized derivatives with respect to u, NOT with respect to s=L*u^8.
// Requires 0<u<=1 and 0<L<1. The endpoint u=0 is handled elsewhere analytically.
// Encloses S(L*u^8), S(s)=log(expm1(s)), through derivative order four.
inline J contact_S(const I& L,const I& u){
    if(!L.positive()||!strictly_less(L,I(1)))
        throw std::runtime_error("contact length outside positive certified range");
    if(!u.positive()||!certainly_leq(u,I(1)))
        throw std::runtime_error("contact u interval must lie in (0,1]");
    const long den[4]={24,2880,181440,9676800};
    J z;
    z.c[0]=log(L)+I(8)*log(u);
    for(unsigned j=1;j<=4;j++)
        z.c[j]=I(j%2?8:-8)/(I(static_cast<long>(j))*powi(u,j));
    for(unsigned j=0;j<=4;j++){
        z.c[j]+=L/I(2)*contact_jet_detail::binomial(8,j)*powi(u,8-j);
        for(unsigned k=1;k<=4;k++){
            I ak=I(k%2?1:-1)/I(den[k-1]);
            z.c[j]+=ak*powi(L,2*k)*contact_jet_detail::binomial(16*k,j)*powi(u,16*k-j);
        }
        I e=contact_jet_detail::tail_bound(L,u,j);
        z.c[j]+=hull(-e,e);
    }
    return z;
}
