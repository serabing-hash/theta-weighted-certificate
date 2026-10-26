#include "jet.hpp"
#include "inputs.hpp"
#include <vector>
#include <array>
#include <algorithm>
#include <fstream>
#include <string>
#include <cmath>
#include <limits>
#include <cstring>
#include <cstdint>
#include <iostream>
using std::vector;
constexpr int NF=552,DF=1104,NC=276;
const I DEL=I(1)/I(NF), HALF=DEL/I(2);
I NN[2],CN[2],C0,L2; std::array<I,5> logs,ac;
struct Temp {I a,b,origin,L,ua,ub;int sign,transformed;bool tail;};
vector<Temp> temps; std::string last_error;
I fromdouble(double x){I z;mpfr_set_d(z.lo.v,x,MPFR_RNDN);mpfr_set_d(z.hi.v,x,MPFR_RNDN);return z;}
double up(const I&x){double z=mpfr_get_d(x.hi.v,MPFR_RNDU);if(mpfr_sgn(x.hi.v)>0&&z<std::numeric_limits<double>::min())z=std::numeric_limits<double>::min();return z;}
double center(const I&x){return mpfr_get_d(midpoint(x).lo.v,MPFR_RNDN);}
void convert(const I&x,double&m,double&r){m=center(x);uint64_t bits;std::memcpy(&bits,&m,sizeof(bits));if(((bits&0x7ff0000000000000ULL)==0&&(bits&0xfffffffffffffULL)!=0)||!std::isfinite(m)||std::abs(m)>1e50)throw std::runtime_error("subnormal/nonfinite/overflow-risk point center");r=up(absupper(x-fromdouble(m)));}
I positive_series(const I&d){I term=d,s(0);for(int k=1;k<=8;k++){term=term*square(d)/(I(4)*I(2*k)*I(2*k+1));s+=term;}I next=term*square(d)/(I(4)*I(18)*I(19));return s+hull(I(0),next/(I(1)-square(d)/I(4)));}
template<class X>X gp(const X&s){return s+log(X(1)-exp(X(-2)*s))/X(2);}
template<class X>X gm(const X&s){X e=exp(-s);return log((X(1)-e)/(X(1)+e))/X(2);}
template<class X>X SS(const X&z){return log(exp(z)-X(1));}
template<class X>X DD(const X&z){return log(X(1)+exp(z));}
// Differences at distances a and a+DEL, with the common displacement cancelled analytically.
J Sdiff(const J&a){J e=exp(-a);return J(DEL)+log(J(1)+e*(J(1)-exp(-J(DEL)))/(J(1)-e));}
J Ddiff(const J&a){J e=exp(-a);return J(DEL)+log(J(1)-e*(J(1)-exp(-J(DEL)))/(J(1)+e));}
std::array<J,2> basic(const J&x,int q){J s,d;
if(q==0){s=J(C0)-(SS(J(DEL)-x)+SS(x))/J(2);d=(DD(x)-DD(J(DEL)-x))/J(2);}
else if(q<0){s=-Sdiff(-x)/J(2);d=-Ddiff(-x)/J(2);}
else{s=-Sdiff(x-J(DEL))/J(2);d=Ddiff(x-J(DEL))/J(2);}
J y=(x-J(HALF))/J(2);
return {(cosh(y)*s+sinh(y)*d)/J(NN[0]),(sinh(y)*s+cosh(y)*d)/J(NN[1])};}

J kap8(const J&x){J sum(0),ex=exp(J(2)*x);for(int n=1;n<=8;n++){J t=J(PI)*J(n*n)*ex;sum=sum+(J(4)*t*t-J(6)*t)*exp(-t);}return exp(x/J(2))*sum;}
I ktail(const I&x){I e=exp(I(2)*x);return I(4)*square(PI)*exp(I(9)*x/I(2))*I(6561)*exp(-PI*I(81)*e)/(I(1)-powi(I(10)/I(9),4)*exp(-PI*I(19)*e));}
J mapped(const Temp&t,const J&u){return t.transformed?J(t.origin)+J(t.sign)*J(t.L)*powi(u,8):J(t.a)+J(t.L)*u;}
J jac(const Temp&t,const J&u){return t.transformed?J(8)*J(t.L)*powi(u,7):J(t.L);}
std::array<J,2> modes(const J&x,int cell,bool coarse){I d=coarse?I(1)/I(NC):DEL;J y=(x-J(I(2*cell+1)*d/I(2)))/J(2);return {cosh(y)/J(coarse?CN[0]:NN[0]),sinh(y)/J(coarse?CN[1]:NN[1])};}
// Returns support cell and reflected even local modes. All branches certified at exact panel midpoint.
int support_cell(const I&mid){I z=mid;if(strictly_less(mid,I(0)))z=-mid;else if(!mid.positive())throw std::runtime_error("support sign ambiguous");if(strictly_less(I(1),z))return -1;if(!strictly_less(z,I(1)))throw std::runtime_error("support boundary ambiguous");int k=int(std::floor(mpfr_get_d(z.lo.v,MPFR_RNDD)*NF));for(int j=k-1;j<=k+1;j++)if(j>=0&&j<NF&&strictly_less(I(j)/I(NF),z)&&strictly_less(z,I(j+1)/I(NF)))return j;throw std::runtime_error("support cell ambiguous");}
void finite_rows(const J&x,const I&mid,vector<std::array<J,2>>&r){int k=support_cell(mid);if(k>=0){J z=mid.positive()?x:-x;auto p=modes(z,k,false);for(int m=0;m<2;m++)r[k][m]=r[k][m]-J(CG)*p[m];}
for(int n=0;n<5;n++)for(int sg:{-1,1}){I sm=mid+I(sg)*logs[n];int j=support_cell(sm);if(j<0)continue;J sx=x+J(I(sg)*logs[n]);if(strictly_less(sm,I(0)))sx=-sx;auto p=modes(sx,j,false);for(int m=0;m<2;m++)r[j][m]=r[j][m]-J(ac[n])*p[m];}}
void init(){if(!temps.empty())return;L2=log(I(2));C0=I(2)*L2+PI/I(2);I sf=positive_series(DEL),sc=positive_series(I(1)/I(NC));NN[1]=sqrt(sf);NN[0]=sqrt(I(2)*DEL+sf);CN[1]=sqrt(sc);CN[0]=sqrt(I(2)/I(NC)+sc);
int ns[]={2,3,4,5,7},ps[]={2,3,2,5,7};vector<I> cuts={I(0),DEL};for(int n=0;n<5;n++){logs[n]=log(I(ns[n]));ac[n]=log(I(ps[n]))/sqrt(I(ns[n]));for(int sg:{-1,1}){I v=I(sg)*logs[n];int k=int(std::floor(mpfr_get_d((v/DEL).lo.v,MPFR_RNDD)));I f=v-I(k)*DEL;if(!f.positive()||!strictly_less(f,DEL))throw std::runtime_error("phase floor not certified");cuts.push_back(f);}}
std::sort(cuts.begin(),cuts.end(),[](const I&a,const I&b){return compare_lower(a,b)<0;});for(size_t i=1;i<cuts.size();i++)if(!strictly_less(cuts[i-1],cuts[i]))throw std::runtime_error("phase separation failed");
for(size_t j=1;j<cuts.size();j++){I a=cuts[j-1],b=cuts[j];bool singularleft=j==1,singularright=j+1==cuts.size();if(singularleft||singularright){Temp base{a,b,singularleft?a:b,b-a,I(0),I(0),singularleft?1:-1,1,false};Temp tail=base;tail.ua=I(0);tail.ub=I(1)/I(1024);tail.tail=true;temps.push_back(tail);for(int d=10;d>=1;d--){I lo=I(1)/I(1<<d),hi=I(1)/I(1<<(d-1));for(int sub=0;sub<2;sub++){Temp t=base;t.ua=lo+(hi-lo)*I(sub)/I(2);t.ub=lo+(hi-lo)*I(sub+1)/I(2);temps.push_back(t);}}}else{for(int sub=0;sub<2;sub++){Temp t{a,b,I(0),b-a,I(sub)/I(2),I(sub+1)/I(2),1,0,false};temps.push_back(t);}}}}
extern "C" int h_init(){try{init();return int(temps.size());}catch(const std::exception&e){last_error=e.what();return -1;}}
extern "C" const char* h_error(){return last_error.c_str();}
extern "C" int h_is_tail(int tid){return temps.at(tid).tail?1:0;}
// aux per target stride 128: r domain norms[0..4], p domain norms[5..9], v domain norms[10..14],
// wJac domain abs[15..19], Jac domain abs[20..24], mJac domainabs[25..29],
// point p(mid/rad) flattened 3x2 ->[30..41], v->[42..53], wJac(mid/rad)3->[54..59],Jac->[60..65],mJac->[66..71],
// physicalwidth up[72],theta dw up[73],theta |dm|up[74], h upper[75], t0upper[76].
double pu(double x){if(x<0||!std::isfinite(x))throw std::runtime_error("invalid bound scalar");return std::max(x,std::numeric_limits<double>::min());}
double au(double a,double b){return std::nextafter(pu(a)+pu(b)+std::numeric_limits<double>::min(),INFINITY);}
double mu(double a,double b){return std::nextafter(pu(a)*pu(b)+std::numeric_limits<double>::min(),INFINITY);}
void addcenter(double&m,double&r,double a,double ar){double old=m;m=old+a;double er=mu(0x1p-50,au(std::abs(old),std::abs(a)));r=au(au(r,ar),au(er,1e-280));}
extern "C" int h_eval(int tid,double*rmid,double*rrad,double*aux){try{const Temp&t=temps.at(tid);if(t.tail)throw std::runtime_error("tail uses separate interface");I um=(t.ua+t.ub)/I(2),ur=hull(t.ua,t.ub);J xm=mapped(t,J::var(um)),xr=mapped(t,J::var(ur)),jm=jac(t,J::var(um)),jr=jac(t,J::var(ur));
vector<std::array<double,6>> cmid(1655),crad(1655);vector<std::array<I,5>> prefix(1656);
for(int q=-551;q<=1103;q++){auto a=basic(J(I(q)*DEL)+xm,q),b=basic(J(I(q)*DEL)+xr,q);int idx=q+551;for(int k=0;k<5;k++){I ss(0);for(int mode=0;mode<2;mode++){ss+=square(absupper(b[mode].c[k]));if(k<3)convert(a[mode].c[k],cmid[idx][2*k+mode],crad[idx][2*k+mode]);}prefix[idx+1][k]=prefix[idx][k]+ss;}}
for(int target=0;target<NF;target++){double*o=aux+target*128;for(int k=0;k<128;k++)o[k]=0;J x=J(I(target)*DEL)+xm,xd=J(I(target)*DEL)+xr;I xmid=x.c[0];
// Combining two outward cache centers/radii is binary64, with an explicit error allowance.
for(int source=0;source<NF;source++)for(int mode=0;mode<2;mode++)for(int k=0;k<3;k++){size_t pos=(size_t(target)*3+k)*DF+2*source+mode;int a=target-source+551,b=target+source+1+551,col=2*k+mode;rmid[pos]=cmid[a][col];rrad[pos]=crad[a][col];addcenter(rmid[pos],rrad[pos],(mode?-1:1)*cmid[b][col],crad[b][col]);}
I norms[5];for(int k=0;k<5;k++){I direct=prefix[target+552][k]-prefix[target][k],mirror=prefix[target+1104][k]-prefix[target+552][k];norms[k]=sqrt(upperpoint(direct))+sqrt(upperpoint(mirror));}
// At most11 sparse finite scalar/prime contributions; no dense MPFR row recombination.
auto addfinite=[&](int cell,const std::array<J,2>&a,const std::array<J,2>&b,const I&coef){for(int k=0;k<5;k++){I nn(0);for(int mode=0;mode<2;mode++){I v=coef*b[mode].c[k];nn+=square(absupper(v));if(k<3){I v0=coef*a[mode].c[k];double mm,rr;convert(v0,mm,rr);size_t pos=(size_t(target)*3+k)*DF+2*cell+mode;addcenter(rmid[pos],rrad[pos],mm,rr);}}norms[k]+=sqrt(nn);}};
addfinite(target,modes(x,target,false),modes(xd,target,false),-CG);
for(int n=0;n<5;n++)for(int sg:{-1,1}){I sm=xmid+I(sg)*logs[n];int cell=support_cell(sm);if(cell<0)continue;J xp=x+J(I(sg)*logs[n]),dp=xd+J(I(sg)*logs[n]);if(strictly_less(sm,I(0))){xp=-xp;dp=-dp;}addfinite(cell,modes(xp,cell,false),modes(dp,cell,false),-ac[n]);}
for(int k=0;k<5;k++)o[k]=up(norms[k]);
auto pm=modes(x,target,false),pd=modes(xd,target,false),vm=modes(x,target/2,true),vd=modes(xd,target/2,true);for(int k=0;k<5;k++){o[5+k]=up(sqrt(square(absupper(pd[0].c[k]))+square(absupper(pd[1].c[k]))));o[10+k]=up(sqrt(square(absupper(vd[0].c[k]))+square(absupper(vd[1].c[k]))));if(k<3)for(int m=0;m<2;m++){convert(pm[m].c[k],o[30+4*k+2*m],o[31+4*k+2*m]);convert(vm[m].c[k],o[42+4*k+2*m],o[43+4*k+2*m]);}}
J km=kap8(x),kd=kap8(xd),ccm=cosh(x/J(2)),ccd=cosh(xd/J(2));J wm=km/(J(T0)*ccm)*jm,wd=kd/(J(T0)*ccd)*jr,mm=J(2)*ccm/km*jm,md=J(2)*ccd/kd*jr;for(int k=0;k<5;k++){o[15+k]=up(absupper(wd.c[k]));o[20+k]=up(absupper(jr.c[k]));o[25+k]=up(absupper(md.c[k]));if(k<3){convert(wm.c[k],o[54+2*k],o[55+2*k]);convert(jm.c[k],o[60+2*k],o[61+2*k]);convert(mm.c[k],o[66+2*k],o[67+2*k]);}}
I dt=hull(I(0),ktail(xd.c[0])),k0=kd.c[0],c0=ccd.c[0];o[73]=up(absupper(dt/(T0*c0)));o[74]=up(absupper(-I(2)*c0*dt/(k0*(k0+dt))));o[72]=up(t.transformed?t.L*(powi(t.ub,8)-powi(t.ua,8)):t.L*(t.ub-t.ua));o[75]=up(t.ub-t.ua);o[76]=up(T0);
}return 0;}catch(const std::exception&e){last_error=e.what();return -1;}}
struct LP{I a,b;LP(){}LP(const I&x):a(x){} };LP operator+(const LP&x,const LP&y){LP z;z.a=x.a+y.a;z.b=x.b+y.b;return z;}LP operator-(const LP&x){LP z;z.a=-x.a;z.b=-x.b;return z;}LP operator-(const LP&x,const LP&y){return x+-y;}LP operator*(const I&x,const LP&y){LP z;z.a=x*y.a;z.b=x*y.b;return z;}LP operator/(const LP&x,const I&y){return (I(1)/y)*x;}
LP glog(const I&s,bool plus,const I&h){if(s.positive())return LP(plus?gp(s):gm(s));if(!s.contains_zero())throw std::runtime_error("tail distance invalid");LP z;z.b=I(1)/I(2);z.a=plus?hull(L2/I(2),L2/I(2)+h):hull(-L2/I(2)-h/I(2),-L2/I(2));return z;}
LP slog(const I&s,const I&h){if(s.positive())return LP(SS(s));if(!s.contains_zero())throw std::runtime_error("tail S distance invalid");LP z;z.a=hull(I(0),h);z.b=I(1);return z;}
std::array<LP,2> basic_tail(const I&x,int q,const I&h){LP s,d;if(q==0){s=LP(C0)-(slog(DEL-x,h)+slog(x,h))/I(2);d=LP((DD(x)-DD(DEL-x))/I(2));}else if(q<0){s=-(slog(DEL-x,h)-slog(-x,h))/I(2);d=LP(-(DD(DEL-x)-DD(-x))/I(2));}else{s=-(slog(x,h)-slog(x-DEL,h))/I(2);d=LP((DD(x)-DD(x-DEL))/I(2));}I y=(x-HALF)/I(2);return {(cosh(y)*s+sinh(y)*d)/NN[0],(sinh(y)*s+cosh(y)*d)/NN[1]};}

// tail aux target stride16: ||r_A||,||r_B||,||phi||,||v||,wmax,mmax,h,|M1|,M2,T0up.
extern "C" int h_tail(int tid,double*aux){try{const Temp&t=temps.at(tid);if(!t.tail)throw std::runtime_error("not tail");I h=t.L*powi(t.ub,8),xi=hull(t.origin,t.origin+I(t.sign)*h),lh=log(h);if(!strictly_less(h,I(1)))throw std::runtime_error("tail log sign");vector<std::array<LP,2>> ca(1655);for(int q=-551;q<=1103;q++)ca[q+551]=basic_tail(I(q)*DEL+xi,q,h);
for(int target=0;target<NF;target++){I x=I(target)*DEL+xi,mid=I(target)*DEL+t.origin+I(t.sign)*h/I(2);vector<std::array<LP,2>> r(NF);for(int source=0;source<NF;source++)for(int m=0;m<2;m++)r[source][m]=ca[target-source+551][m]+I(m?-1:1)*ca[target+source+1+551][m];
// All nonsingular scalar/prime terms retained in the A coefficient.
vector<std::array<J,2>> finite(NF);finite_rows(J(x),mid,finite);for(int j=0;j<NF;j++)for(int m=0;m<2;m++)r[j][m]=r[j][m]+LP(finite[j][m].c[0]);I an(0),bn(0);for(auto &row:r)for(auto &v:row){an+=square(absupper(v.a));bn+=square(absupper(v.b));}auto pp=modes(J(x),target,false),vv=modes(J(x),target/2,true);I pn=sqrt(square(absupper(pp[0].c[0]))+square(absupper(pp[1].c[0]))),vn=sqrt(square(absupper(vv[0].c[0]))+square(absupper(vv[1].c[0])));I kk=kap8(J(x)).c[0]+hull(I(0),ktail(x)),cc=cosh(x/I(2)),w=kk/(T0*cc),mm=I(2)*cc/kk;double*o=aux+target*16;for(int k=0;k<16;k++)o[k]=0;o[0]=up(sqrt(an));o[1]=up(sqrt(bn));o[2]=up(pn);o[3]=up(vn);o[4]=up(w);o[5]=up(mm);o[6]=up(h);o[7]=up(absupper(h*(lh-I(1))));o[8]=up(h*(square(lh)-I(2)*lh+I(2)));o[9]=up(T0);
}return 0;}catch(const std::exception&e){last_error=e.what();return -1;}}
extern "C" void h_t0(double*out){convert(T0,out[0],out[1]);}
