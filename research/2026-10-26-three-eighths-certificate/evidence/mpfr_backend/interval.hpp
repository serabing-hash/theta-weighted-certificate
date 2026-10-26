#pragma once
#include "mpfr.h"
#include <string>
#include <stdexcept>
#include <utility>
namespace directed {
constexpr mpfr_prec_t PREC=266; // ceil(80 log2(10)); fixed for entire run.
struct R {
 mpfr_t v;
 R(){mpfr_init2(v,PREC);mpfr_set_zero(v,1);}
 R(const R& x):R(){mpfr_set(v,x.v,MPFR_RNDN);}
 R(R&& x) noexcept:R(){mpfr_swap(v,x.v);}
 R& operator=(const R& x){mpfr_set(v,x.v,MPFR_RNDN);return *this;}
 R& operator=(R&& x) noexcept{mpfr_swap(v,x.v);return *this;}
 ~R(){mpfr_clear(v);}
};
struct I {
 R lo,hi;
 I()=default;
 I(long x){mpfr_set_si(lo.v,x,MPFR_RNDD);mpfr_set_si(hi.v,x,MPFR_RNDU);}
 I(int x):I(static_cast<long>(x)){}
 explicit I(const std::string& x):I(x,x){}
 I(const std::string& l,const std::string& h){
  if(mpfr_set_str(lo.v,l.c_str(),10,MPFR_RNDD)||mpfr_set_str(hi.v,h.c_str(),10,MPFR_RNDU))throw std::runtime_error("invalid decimal");
  check();
 }
 void check()const{if(!mpfr_number_p(lo.v)||!mpfr_number_p(hi.v)||mpfr_cmp(lo.v,hi.v)>0)throw std::runtime_error("invalid/nonfinite interval");}
 bool positive()const{return mpfr_cmp_si(lo.v,0)>0;}
 bool nonnegative()const{return mpfr_cmp_si(lo.v,0)>=0;}
 bool contains_zero()const{return mpfr_cmp_si(lo.v,0)<=0&&mpfr_cmp_si(hi.v,0)>=0;}
 std::string lower()const;
 std::string upper()const;
};
inline std::string decimal(mpfr_srcptr v,mpfr_rnd_t mode){
 mpfr_exp_t e; char* p=mpfr_get_str(nullptr,&e,10,90,v,mode);if(!p)throw std::bad_alloc();
 std::string s(p);mpfr_free_str(p);if(mpfr_zero_p(v))return "0";
 bool neg=s[0]=='-';if(neg)s.erase(0,1);
 return std::string(neg?"-":"")+s[0]+"."+s.substr(1)+"e"+std::to_string(e-1);
}
inline std::string I::lower()const{return decimal(lo.v,MPFR_RNDD);}
inline std::string I::upper()const{return decimal(hi.v,MPFR_RNDU);}
inline I operator+(const I&a,const I&b){I r;mpfr_add(r.lo.v,a.lo.v,b.lo.v,MPFR_RNDD);mpfr_add(r.hi.v,a.hi.v,b.hi.v,MPFR_RNDU);r.check();return r;}
inline I operator-(const I&a,const I&b){I r;mpfr_sub(r.lo.v,a.lo.v,b.hi.v,MPFR_RNDD);mpfr_sub(r.hi.v,a.hi.v,b.lo.v,MPFR_RNDU);r.check();return r;}
inline I operator-(const I&a){I r;mpfr_neg(r.lo.v,a.hi.v,MPFR_RNDD);mpfr_neg(r.hi.v,a.lo.v,MPFR_RNDU);r.check();return r;}
inline I operator*(const I&a,const I&b){
 I r;R d,u;bool first=true;mpfr_srcptr aa[]={a.lo.v,a.hi.v},bb[]={b.lo.v,b.hi.v};
 for(auto x:aa)for(auto y:bb){mpfr_mul(d.v,x,y,MPFR_RNDD);mpfr_mul(u.v,x,y,MPFR_RNDU);
 if(first||mpfr_cmp(d.v,r.lo.v)<0)mpfr_set(r.lo.v,d.v,MPFR_RNDN);
 if(first||mpfr_cmp(u.v,r.hi.v)>0)mpfr_set(r.hi.v,u.v,MPFR_RNDN);
 first=false;}
 r.check();return r;
}
inline I reciprocal(const I&a){if(a.contains_zero())throw std::runtime_error("division includes zero");I r;mpfr_ui_div(r.lo.v,1,a.hi.v,MPFR_RNDD);mpfr_ui_div(r.hi.v,1,a.lo.v,MPFR_RNDU);r.check();return r;}
inline I operator/(const I&a,const I&b){return a*reciprocal(b);}
inline I& operator+=(I&a,const I&b){a=a+b;return a;}
inline I& operator-=(I&a,const I&b){a=a-b;return a;}
inline I& operator*=(I&a,const I&b){a=a*b;return a;}
inline I& operator/=(I&a,const I&b){a=a/b;return a;}
inline I square(const I&a){I r;R x,y;mpfr_sqr(x.v,a.lo.v,MPFR_RNDU);mpfr_sqr(y.v,a.hi.v,MPFR_RNDU);mpfr_set(r.hi.v,mpfr_cmp(x.v,y.v)>0?x.v:y.v,MPFR_RNDN);
 if(a.contains_zero())mpfr_set_zero(r.lo.v,1);else {mpfr_sqr(x.v,a.lo.v,MPFR_RNDD);mpfr_sqr(y.v,a.hi.v,MPFR_RNDD);mpfr_set(r.lo.v,mpfr_cmp(x.v,y.v)<0?x.v:y.v,MPFR_RNDN);}r.check();return r;}
inline I powi(I a,unsigned n){I r(1);while(n){if(n&1)r*=a;n>>=1;if(n)a=square(a);}return r;}
inline I exp(const I&a){I r;mpfr_exp(r.lo.v,a.lo.v,MPFR_RNDD);mpfr_exp(r.hi.v,a.hi.v,MPFR_RNDU);r.check();return r;}
inline I log(const I&a){if(!a.positive())throw std::runtime_error("log domain");I r;mpfr_log(r.lo.v,a.lo.v,MPFR_RNDD);mpfr_log(r.hi.v,a.hi.v,MPFR_RNDU);r.check();return r;}
inline I sqrt(const I&a){if(!a.nonnegative())throw std::runtime_error("sqrt domain");I r;mpfr_sqrt(r.lo.v,a.lo.v,MPFR_RNDD);mpfr_sqrt(r.hi.v,a.hi.v,MPFR_RNDU);r.check();return r;}
inline I tanh(const I&a){I r;mpfr_tanh(r.lo.v,a.lo.v,MPFR_RNDD);mpfr_tanh(r.hi.v,a.hi.v,MPFR_RNDU);r.check();return r;}
inline I pow_positive(const I&a,const I&b){return exp(b*log(a));}
inline I hull(const I&a,const I&b){I r;mpfr_set(r.lo.v,mpfr_cmp(a.lo.v,b.lo.v)<0?a.lo.v:b.lo.v,MPFR_RNDN);mpfr_set(r.hi.v,mpfr_cmp(a.hi.v,b.hi.v)>0?a.hi.v:b.hi.v,MPFR_RNDN);r.check();return r;}
inline I intersect(const I&a,const I&b){I r;mpfr_set(r.lo.v,mpfr_cmp(a.lo.v,b.lo.v)>0?a.lo.v:b.lo.v,MPFR_RNDN);mpfr_set(r.hi.v,mpfr_cmp(a.hi.v,b.hi.v)<0?a.hi.v:b.hi.v,MPFR_RNDN);r.check();return r;}
inline I lower_point(const I&a){I r;r.lo=a.lo;r.hi=a.lo;return r;}
inline I upper_point(const I&a){I r;r.lo=a.hi;r.hi=a.hi;return r;}
inline I absupper(const I&a){I r;R x,y;mpfr_abs(x.v,a.lo.v,MPFR_RNDU);mpfr_abs(y.v,a.hi.v,MPFR_RNDU);mpfr_set(r.hi.v,mpfr_cmp(x.v,y.v)>0?x.v:y.v,MPFR_RNDN);r.lo=r.hi;return r;}
inline I width(const I&a){I r;mpfr_sub(r.hi.v,a.hi.v,a.lo.v,MPFR_RNDU);r.lo=r.hi;r.check();return r;}
inline I radius(const I&a){I r=width(a);mpfr_div_2ui(r.hi.v,r.hi.v,1,MPFR_RNDU);r.lo=r.hi;r.check();return r;}
inline bool strictly_less(const I&a,const I&b){return mpfr_cmp(a.hi.v,b.lo.v)<0;}
inline bool certainly_leq(const I&a,const I&b){return mpfr_cmp(a.hi.v,b.lo.v)<=0;}
inline int compare_lower(const I&a,const I&b){return mpfr_cmp(a.lo.v,b.lo.v);}
inline int compare_upper(const I&a,const I&b){return mpfr_cmp(a.hi.v,b.hi.v);}
inline I pi(){I r;mpfr_const_pi(r.lo.v,MPFR_RNDD);mpfr_const_pi(r.hi.v,MPFR_RNDU);return r;}
inline I lowerpoint(const I&a){return lower_point(a);}
inline I upperpoint(const I&a){return upper_point(a);}
inline bool upper_lt_lower(const I&a,const I&b){return strictly_less(a,b);}
// Chosen representable center, NOT an enclosure of the exact mathematical midpoint.
// For a Taylor bound about it use absupper(a-midpoint(a)), NOT radius(a).
inline I midpoint(const I&a){I r;mpfr_add(r.lo.v,a.lo.v,a.hi.v,MPFR_RNDN);mpfr_div_2ui(r.lo.v,r.lo.v,1,MPFR_RNDN);r.hi=r.lo;r.check();
 if(mpfr_cmp(r.lo.v,a.lo.v)<0||mpfr_cmp(r.hi.v,a.hi.v)>0)throw std::runtime_error("midpoint out of interval");
 return r;}
} // namespace directed
