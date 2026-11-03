"""Exact signed convolution by balanced binary-radix integer multiplication."""
def signed_convolution(a,b):
    a=[int(x) for x in a];b=[int(x) for x in b]
    if not a or not b:return []
    count=len(a)+len(b)-1
    bound=min(len(a),len(b))*max(map(abs,a))*max(map(abs,b))
    if not bound:return [0]*count
    width=max(1,(int(2*bound).bit_length()+7)//8)
    radix=1<<(8*width);assert 2*bound<radix
    def pack(v):
        pos=b''.join(max(x,0).to_bytes(width,'little') for x in v)
        neg=b''.join(max(-x,0).to_bytes(width,'little') for x in v)
        return int.from_bytes(pos,'little')-int.from_bytes(neg,'little')
    product=pack(a)*pack(b);sign=1 if product>=0 else -1
    digits=abs(product).to_bytes(count*width,'little')
    carry=0;result=[]
    for i in range(count):
        value=int.from_bytes(digits[i*width:(i+1)*width],'little')+carry
        if value>=radix//2:value-=radix;carry=1
        else:carry=0
        assert abs(value)<=bound
        result.append(sign*value)
    assert carry==0
    return result
