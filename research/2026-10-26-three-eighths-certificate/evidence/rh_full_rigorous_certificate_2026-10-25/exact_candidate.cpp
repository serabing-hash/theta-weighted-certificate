// Candidate exactification only. Execute solely inside the approved full-certificate runner.
#include "../mpfr_backend/interval.hpp"
#include <vector>
#include <array>
#include <fstream>
#include <iostream>
#include <iomanip>
#include <cmath>
#include <cstdint>
#include <limits>
#include <stdexcept>
using namespace directed;
constexpr int NC=276, DC=552, DF=1104;
I dyadic(double x){if(!std::isfinite(x))throw std::runtime_error("nonfinite binary64 input"); I a;mpfr_set_d(a.lo.v,x,MPFR_RNDD);mpfr_set_d(a.hi.v,x,MPFR_RNDU);a.check();return a;}
std::vector<double> load(const char* path,size_t count){std::ifstream f(path,std::ios::binary);if(!f)throw std::runtime_error(std::string("missing ")+path);std::vector<double>v(count);f.read(reinterpret_cast<char*>(v.data()),count*sizeof(double));if(f.gcount()!=static_cast<std::streamsize>(count*sizeof(double)))throw std::runtime_error("short input");char c;if(f.read(&c,1))throw std::runtime_error("long input");for(double x:v)if(!std::isfinite(x))throw std::runtime_error("nonfinite input");return v;}
I maxupper(const I&a,const I&b){return upperpoint(compare_upper(a,b)>=0?a:b);}
I minupper(const I&a,const I&b){return upperpoint(compare_upper(a,b)<=0?a:b);}
I ch(const I&x){return (exp(x)+exp(-x))/I(2);}
I sh(const I&x){return (exp(x)-exp(-x))/I(2);}
std::array<I,2> norms(int n){I d=I(1)/I(n),term=d,sum(0);for(int k=1;k<=8;k++){term=term*square(d)/(I(4)*I(2*k)*I(2*k+1));sum+=term;}I next=term*square(d)/(I(4)*I(18)*I(19));sum+=hull(I(0),next/(I(1)-square(d)/I(4)));return {sqrt(I(2)*d+sum),sqrt(sum)};}
std::string interval_json(const I&a){return "{\"lo\":\""+a.lower()+"\",\"hi\":\""+a.upper()+"\"}";}
double updouble(const I&a){double x=mpfr_get_d(a.hi.v,MPFR_RNDU);if(!std::isfinite(x))throw std::runtime_error("nonfinite exported bound");return x;}
void bound(std::ostream&o,const char*name,const I&a,bool comma=true){o<<"\""<<name<<"\":"<<interval_json(a)<<",\n\""<<name<<"_upper_float\":"<<std::setprecision(17)<<updouble(a);if(comma)o<<",\n";}
int main(){try{
 if(sizeof(double)!=8||!std::numeric_limits<double>::is_iec559)throw std::runtime_error("binary64 host required");
 uint32_t endian=1;
 if(*reinterpret_cast<unsigned char*>(&endian)!=1)throw std::runtime_error("little-endian host required");
 auto Z=load("Z_dyadic.bin",size_t(DC)*DC),U=load("Ufloat.bin",size_t(DF)*DC),C=load("Ctrial.bin",size_t(NC)*2*DC);
 auto nf=norms(552),nc=norms(276);I d=I(1)/I(2208),AA=nf[0]*ch(d)/nc[0],BB=nf[1]*sh(d)/nc[0],CC=nf[0]*sh(d)/nc[1],DD=nf[1]*ch(d)/nc[1];
 I P[4][2]={{AA,-CC},{-BB,DD},{AA,CC},{BB,DD}};
 I X[4][2]={{BB,DD},{AA,CC},{BB,-DD},{-AA,CC}};
 for(int i=0;i<4;i++)for(int j=0;j<4;j++){I s;for(int k=0;k<4;k++){const I&a=i<2?P[k][i]:X[k][i-2];const I&b=j<2?P[k][j]:X[k][j-2];s+=a*b;}if(!(s-I(i==j?1:0)).contains_zero())throw std::runtime_error("local orthogonality identity not enclosed");}
 I zsq,zrowmax,zcolmax;std::vector<I>zc(DC);
 for(int i=0;i<DC;i++){I row;for(int j=0;j<DC;j++){I z=dyadic(Z[size_t(i)*DC+j]);I az=absupper(z);row+=az;zc[j]+=az;zsq+=square(z);}zrowmax=maxupper(zrowmax,row);}
 for(auto&x:zc)zcolmax=maxupper(zcolmax,x);
 I znorm2=minupper(upperpoint(zsq),upperpoint(zrowmax*zcolmax));I unorm=upperpoint(sqrt(I(1)+znorm2));
 I esq,erowmax,ecolmax;std::vector<I>ec(DC);
 for(int c=0;c<NC;c++)for(int r=0;r<4;r++){I row;int i=4*c+r;for(int j=0;j<DC;j++){I p;if(j==2*c)p=P[r][0];if(j==2*c+1)p=P[r][1];I ue=p-X[r][0]*dyadic(Z[size_t(2*c)*DC+j])-X[r][1]*dyadic(Z[size_t(2*c+1)*DC+j]);I err=absupper(ue-dyadic(U[size_t(i)*DC+j]));row+=err;ec[j]+=err;esq+=square(err);}erowmax=maxupper(erowmax,row);}
 for(auto&x:ec)ecolmax=maxupper(ecolmax,x);
 I efrob=upperpoint(sqrt(upperpoint(esq))),erc=upperpoint(sqrt(erowmax*ecolmax)),eta=minupper(efrob,erc);
 std::vector<I>cn(NC);I csq,cm;
 for(int c=0;c<NC;c++){I s;for(int k=0;k<2;k++)for(int j=0;j<DC;j++)s+=square(dyadic(C[(size_t(c)*2+k)*DC+j]));cn[c]=upperpoint(sqrt(upperpoint(s)));csq+=s;cm=maxupper(cm,cn[c]);}
 std::ofstream out("exact_candidate.json");out<<"{\n\"status\":\"validated_candidate_exactification\",\n\"working_bits\":266,\n\"coarse_dimension\":552,\n\"fine_dimension\":1104,\n";
 out<<"\"U_norm_upper\":"<<std::setprecision(17)<<updouble(unorm)<<",\n\"U_error_norm_upper\":"<<updouble(eta)<<",\n\"C_cell_norm_upper\":[";for(int c=0;c<NC;c++){if(c)out<<",";out<<updouble(cn[c]);}out<<"],\n";
 bound(out,"U_norm",unorm);bound(out,"U_error_norm",eta);bound(out,"U_frobenius",upperpoint(sqrt(I(DC)+upperpoint(zsq))));bound(out,"Z_operator_norm_squared",znorm2);bound(out,"U_exact_operator_norm",unorm);bound(out,"U_exact_minus_stored_operator_error",eta);bound(out,"U_exact_minus_stored_frobenius_error",efrob);bound(out,"U_exact_minus_stored_rowcol_error",erc);bound(out,"U_stored_operator_norm",upperpoint(unorm+eta));bound(out,"C_global_frobenius",upperpoint(sqrt(upperpoint(csq))));bound(out,"C_max_cell_frobenius",cm);
 out<<"\"C_cell_frobenius_upper_float\":[";for(int c=0;c<NC;c++){if(c)out<<",";out<<std::setprecision(17)<<updouble(cn[c]);}out<<"],\n\"C_cell_frobenius_intervals\":[";for(int c=0;c<NC;c++){if(c)out<<",";out<<interval_json(cn[c]);}out<<"],\n\"P_local_intervals\":[";for(int r=0;r<4;r++){if(r)out<<",";out<<"["<<interval_json(P[r][0])<<","<<interval_json(P[r][1])<<"]";}out<<"],\n\"X_local_intervals\":[";for(int r=0;r<4;r++){if(r)out<<",";out<<"["<<interval_json(X[r][0])<<","<<interval_json(X[r][1])<<"]";}out<<"],\n\"scope\":\"Exact original-moment-preserving U=P-XZ with stored binary64 Z treated as dyadic; arbitrary dyadic C trial. Bounds only, no form/inertia certification.\"\n}\n";if(!out)throw std::runtime_error("output write failed");std::cout<<"validated_candidate_exactification\n";return 0;
 }catch(const std::exception&e){std::cerr<<e.what()<<"\n";return 2;}}
