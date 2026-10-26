// Certified complete fine-source G matrix. No numerical work is run at build time.
// Source basis: 552 positive cells, two normalized modes, even reflection.
#include "g_jet.hpp"
using directed::I;
#include "../rh_two_direction_certificate_2026-10-25/inputs.hpp"
#include <array>
#include <vector>
#include <fstream>
#include <iostream>
#include <chrono>
#include <cmath>
#include <cstdint>
#include <limits>
#include <sys/resource.h>
using namespace directed;
using gcert::Jet;
using gcert::cosh;
using gcert::sinh;
constexpr int N=552,D=1104,MAXSEP=1103;
static_assert(sizeof(double)==8 && std::numeric_limits<double>::is_iec559,"IEEE754 binary64 required");
const I DEL=I(1)/I(N),HALF=DEL/I(2);
I norms[2],L2,C0;
using Block=std::array<I,4>; // 00,01,10,11
using Prims=std::array<I,6>; // sigma + then -, k=-1,0,+1
std::vector<Prims> primitives;
std::vector<Block> gamma_cache,prime_cache,metric_blocks;
I max_metric_remainder,max_metric_tail;
std::chrono::steady_clock::time_point started;
double elapsed(){return std::chrono::duration<double>(std::chrono::steady_clock::now()-started).count();}
I sym(const I&a){I u=absupper(a);return hull(-u,u);}
I exact_double(double x){I z;mpfr_set_d(z.lo.v,x,MPFR_RNDN);z.hi=z.lo;return z;}
I li2(const I&x){if(mpfr_cmp_si(x.hi.v,1)>0)throw std::runtime_error("Li2 domain exceeds one");I z;mpfr_li2(z.lo.v,x.lo.v,MPFR_RNDD);mpfr_li2(z.hi.v,x.hi.v,MPFR_RNDU);z.check();return z;}
I gp(const I&s){return s+log(I(1)-exp(-I(2)*s))/I(2);}
I gm(const I&s){I q=exp(-s);return log((I(1)-q)/(I(1)+q))/I(2);}
I atanh_exp(const I&s){I q=exp(-s);return log((I(1)+q)/(I(1)-q))/I(2);}
int pindex(int sigma,int k){return (sigma==1?0:3)+k+1;}
const I& prim(int sigma,int k,int index){return primitives.at(index).at(pindex(sigma,k));}
void initialize(){
 L2=log(I(2));C0=I(2)*L2+PI/I(2);
 I term=DEL,sum(0);
 for(int k=1;k<=8;k++){term*=square(DEL)/(I(4)*I(2*k)*I(2*k+1));sum+=term;}
 I next=term*square(DEL)/(I(4)*I(18)*I(19));sum+=hull(I(0),next/(I(1)-square(DEL)/I(4)));
 norms[1]=sqrt(sum);norms[0]=sqrt(I(2)*DEL+sum);
 primitives.resize(MAXSEP+2);
 for(int n=0;n<=MAXSEP+1;n++){
  auto&v=primitives[n];
  if(n==0){v={-L2,square(PI)/I(24),L2-I(1),L2,square(PI)/I(8),-L2};continue;}
  I s=I(n)*DEL,q=exp(-s),ep=exp(s),p=gp(s),m=gm(s),a=atanh_exp(s);
  v[0]=-q*p-a;v[1]=square(s)/I(2)+li2(exp(-I(2)*s))/I(4);v[2]=ep*p-ep+a;
  v[3]=-q*m+log(I(1)-exp(-I(2)*s))/I(2);v[4]=(li2(q)-li2(-q))/I(2);v[5]=ep*m-p;
 }
}
I e_integral(const I&lo,const I&hi,int k){return k==0?hi-lo:(exp(I(k)*hi)-exp(I(k)*lo))/I(k);}
I gamma_exponential(int sep,int tau,int sigma){
 int k=(tau+sigma)/2;
 if(sep==0){
  return C0*e_integral(-HALF,HALF,k)
   -exp(I(k)*HALF)*(prim(sigma,-k,1)-prim(sigma,-k,0))
   -exp(-I(k)*HALF)*(prim(-sigma,k,1)-prim(-sigma,k,0));
 }
 I center=I(sep)*DEL,a=center-HALF,b=center+HALF;
 return -exp(-I(sigma)*center/I(2))*(
   exp(I(k)*b)*(prim(sigma,-k,sep+1)-prim(sigma,-k,sep))
   -exp(I(k)*a)*(prim(sigma,-k,sep)-prim(sigma,-k,sep-1)));
}
I mode_coeff(int mode,int sigma){return I(mode==0?1:sigma)/(I(2)*norms[mode]);}
void build_gamma(){
 gamma_cache.resize(MAXSEP+1);
 for(int d=0;d<=MAXSEP;d++)for(int a=0;a<2;a++)for(int b=0;b<2;b++){
  I value(0);for(int tau:{-1,1})for(int sigma:{-1,1})value+=mode_coeff(a,tau)*mode_coeff(b,sigma)*gamma_exponential(d,tau,sigma);
  gamma_cache[d][2*a+b]=value;
 }
 // Reflection makes the co-located mixed-mode form exactly zero.
 if(!gamma_cache[0][1].contains_zero()||!gamma_cache[0][2].contains_zero())throw std::runtime_error("Gamma parity inconsistency");
 gamma_cache[0][1]=I(0);gamma_cache[0][2]=I(0);
 for(int d=1;d<=MAXSEP;d++){I off=intersect(gamma_cache[d][1],-gamma_cache[d][2]);gamma_cache[d][1]=off;gamma_cache[d][2]=-off;}
}
Block overlap(const I&shift){
 Block ans;I lo,hi;
 if(certainly_leq(DEL,shift)||certainly_leq(shift,-DEL))return ans;
 if(strictly_less(I(0),shift)){lo=shift-HALF;hi=HALF;}
 else if(strictly_less(shift,I(0))){lo=-HALF;hi=shift+HALF;}
 else if(mpfr_zero_p(shift.lo.v)&&mpfr_zero_p(shift.hi.v)){lo=-HALF;hi=HALF;}
 else throw std::runtime_error("uncertain prime overlap orientation");
 if(!strictly_less(lo,hi))throw std::runtime_error("uncertain prime overlap support");
 for(int a=0;a<2;a++)for(int b=0;b<2;b++)for(int tau:{-1,1})for(int sigma:{-1,1}){
  int k=(tau+sigma)/2;
  ans[2*a+b]+=mode_coeff(a,tau)*mode_coeff(b,sigma)*exp(-I(sigma)*shift/I(2))*e_integral(lo,hi,k);
 }
 return ans;
}
void build_prime(){
 prime_cache.resize(MAXSEP+1);int ns[5]={2,3,4,5,7},ps[5]={2,3,2,5,7};
 for(int d=0;d<=MAXSEP;d++)for(int j=0;j<5;j++)for(int sign:{-1,1}){
  I shift=I(d)*DEL+I(sign)*log(I(ns[j]));
  if(certainly_leq(DEL,shift)||certainly_leq(shift,-DEL))continue;
  if(!(strictly_less(-DEL,shift)&&strictly_less(shift,DEL)))throw std::runtime_error("prime overlap threshold uncertain");
  Block v=overlap(shift);I weight=log(I(ps[j]))/sqrt(I(ns[j]));
  for(int k=0;k<4;k++)prime_cache[d][k]+=weight*v[k];
 }
 for(int d=0;d<=MAXSEP;d++){I off=intersect(prime_cache[d][1],-prime_cache[d][2]);prime_cache[d][1]=off;prime_cache[d][2]=-off;}
}
Jet kappa8(const Jet&x){Jet total(0),ex=gcert::exp(Jet(2)*x);for(int n=1;n<=8;n++){Jet t=Jet(PI)*Jet(n*n)*ex;total=total+(Jet(4)*t*t-Jet(6)*t)*gcert::exp(-t);}return gcert::exp(x/Jet(2))*total;}
I kappa8(const I&x){I total(0),ex=exp(I(2)*x);for(int n=1;n<=8;n++){I t=PI*I(n*n)*ex;total+=(I(4)*square(t)-I(6)*t)*exp(-t);}return exp(x/I(2))*total;}
I kappa_tail(const I&x){return I(4)*square(PI)*exp(I(9)*x/I(2))*I(6561)*exp(-PI*I(81)*exp(I(2)*x))/(I(1)-powi(I(10)/I(9),4)*exp(-PI*I(19)*exp(I(2)*x)));}
I monomial_integral(unsigned p){return p%2?I(0):I(2)*powi(HALF,p+1)/I(static_cast<long>(p+1));}
// Positive series integral of t^k cosh(t), cosh(t)-1, or sinh(t).
I series_moment(int k,int kind){
 if((kind==2&&k%2==0)||(kind!=2&&k%2!=0))return I(0);
 int start=(kind==1?2:(kind==2?1:0));I fact(1);for(int j=1;j<=start;j++)fact*=I(j);
 I sum(0);int p=start;
 for(int n=0;n<10;n++,p+=2){if(n)fact*=I(p-1)*I(p);sum+=monomial_integral(k+p)/fact;}
 fact*=I(p-1)*I(p);I next=monomial_integral(k+p)/fact;
 sum+=hull(I(0),next/(I(1)-square(HALF)));
 return sum;
}
void build_metric(){
 std::array<Block,6> moments;
 for(int k=0;k<6;k++){
  moments[k][0]=(series_moment(k,0)+monomial_integral(k))/square(norms[0]);
  moments[k][3]=series_moment(k,1)/square(norms[1]);
  moments[k][1]=moments[k][2]=series_moment(k,2)/(norms[0]*norms[1]);
 }
 metric_blocks.resize(N);
 for(int cell=0;cell<N;cell++){
  I center=(I(cell)+I(1)/I(2))*DEL,domain=hull(I(cell)*DEL,I(cell+1)*DEL);
  Jet xc=Jet::var(center),xr=Jet::var(domain);
  Jet mc=Jet(2)*gcert::cosh(xc/Jet(2))/kappa8(xc);
  Jet mr=Jet(2)*gcert::cosh(xr/Jet(2))/kappa8(xr);
  I tail=kappa_tail(domain),kap=kappa8(domain);
  I m_tail=I(2)*cosh(domain/I(2))*tail/(kap*(kap+tail));
  I remainder=absupper(T0)*(absupper(mr.c[6])*powi(HALF,6)+absupper(m_tail));
  if(compare_upper(remainder,max_metric_remainder)>0)max_metric_remainder=upperpoint(remainder);
  if(compare_upper(m_tail,max_metric_tail)>0)max_metric_tail=upperpoint(m_tail);
  for(int entry=0;entry<4;entry++){
   I z(0);for(int k=0;k<6;k++)z+=T0*mc.c[k]*moments[k][entry];
   metric_blocks[cell][entry]=z+sym(remainder);
  }
 }
}
I reflected(const std::vector<Block>&cache,int i,int a,int j,int b){
 int diff=j-i,sum=i+j+1;I first=cache[std::abs(diff)][2*a+b];
 if(diff<0&&(a+b)%2)first=-first;
 I second=cache[sum][2*a+b];if(a)second=-second;
 return I(2)*(first+second);
}
void write_result(){
 std::ofstream mid("Gmid.bin",std::ios::binary),rad("Grad.bin",std::ios::binary);
 if(!mid||!rad)throw std::runtime_error("cannot open binary matrix outputs");
 I maxrowsum(0),maxentry(0),maxmagnitude(0);
 for(int row=0;row<D;row++){
  I rowsum(0);int i=row/2,a=row%2;
  for(int col=0;col<D;col++){
   int j=col/2,b=col%2;
   I z=reflected(gamma_cache,i,a,j,b)-reflected(prime_cache,i,a,j,b);
   if(i==j)z+=metric_blocks[i][2*a+b];if(row==col)z-=CG;
   double center=mpfr_get_d(midpoint(z).lo.v,MPFR_RNDN);
   I r=absupper(z-exact_double(center));double radius_up=mpfr_get_d(r.hi.v,MPFR_RNDU);
   if(!std::isfinite(center)||!std::isfinite(radius_up)||radius_up<0)throw std::runtime_error("invalid binary conversion");
   mid.write(reinterpret_cast<const char*>(&center),sizeof(double));rad.write(reinterpret_cast<const char*>(&radius_up),sizeof(double));
   rowsum+=exact_double(radius_up);if(compare_upper(r,maxentry)>0)maxentry=upperpoint(r);if(compare_upper(absupper(z),maxmagnitude)>0)maxmagnitude=absupper(z);
  }
  if(compare_upper(rowsum,maxrowsum)>0)maxrowsum=upperpoint(rowsum);
 }
 mid.close();rad.close();if(!mid||!rad)throw std::runtime_error("matrix write failure");
 // Read back exactly the emitted data; fail closed on an asymmetric center/radius.
 std::vector<double> cm(D*D),cr(D*D);
 std::ifstream mi("Gmid.bin",std::ios::binary),ra("Grad.bin",std::ios::binary);
 mi.read(reinterpret_cast<char*>(cm.data()),cm.size()*sizeof(double));ra.read(reinterpret_cast<char*>(cr.data()),cr.size()*sizeof(double));
 if(!mi||!ra||mi.peek()!=EOF||ra.peek()!=EOF)throw std::runtime_error("binary matrix readback size failure");
 for(int i=0;i<D;i++)for(int j=0;j<D;j++)if(cm[i*D+j]!=cm[j*D+i]||cr[i*D+j]!=cr[j*D+i])throw std::runtime_error("binary matrix symmetry failure");
 struct rusage ru;getrusage(RUSAGE_SELF,&ru);
 std::ofstream out("g_output.json");out<<"{\n\"classification\":\"CERTIFIED_ENTRY_ENCLOSURES_NOT_FINAL_INERTIA\",\n\"dimension\":"<<D<<",\n\"positive_cells\":"<<N<<",\n\"binary_format\":\"IEEE754 binary64 row-major little-endian; Gmid.bin centers, Grad.bin outward radii\",\n\"binary_symmetry_verified\":true,\n\"global_entry_radius_row_sum_upper\":\""<<maxrowsum.upper()<<"\",\n\"maximum_entry_interval_radius_upper\":\""<<maxentry.upper()<<"\",\n\"maximum_entry_magnitude_upper\":\""<<maxmagnitude.upper()<<"\",\n\"maximum_metric_pointwise_remainder_times_t_upper\":\""<<max_metric_remainder.upper()<<"\",\n\"maximum_metric_theta_tail_effect_upper\":\""<<max_metric_tail.upper()<<"\",\n\"working_bits\":266,\n\"metric_polynomial_degree\":5,\n\"all_prime_powers\":[2,3,4,5,7],\n\"gamma_full_tail\":true,\n\"wall_seconds\":"<<elapsed()<<",\n\"peak_resident_KiB\":"<<ru.ru_maxrss<<"\n}\n";
}
int main(){started=std::chrono::steady_clock::now();try{std::uint32_t endian=1;if(*reinterpret_cast<unsigned char*>(&endian)!=1)throw std::runtime_error("little-endian host required");initialize();build_gamma();build_prime();build_metric();write_result();std::cout<<"G fine enclosures complete\n";return 0;}catch(const std::exception&e){std::ofstream out("g_failure.json");out<<"{\"status\":\"failed\",\"reason\":\""<<e.what()<<"\",\"wall_seconds\":"<<elapsed()<<"}\n";std::cerr<<e.what()<<"\n";return 2;}}
