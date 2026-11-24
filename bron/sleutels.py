import json, sys
def sleutels(tid, lv):
    T=json.load(open('technieken.json')); arr=T if isinstance(T,list) else list(T.values())
    L=[t for t in arr if t['id']==tid][0]['levels'][int(lv)-1]; out=[]; t=0
    for i,f in enumerate(L['fases']):
        if not f.get('houding'): continue
        if i>0:
            for x in f.get('tussen') or []:
                if 0<x['ms']<f['duurMs']: out.append((t+x['ms'],x['houding'],i,'tussen'))
        t_i = t + (f['duurMs'] if i>0 else 0)
        if i>0 and f.get('aankomstMs') and f['aankomstMs']<f['duurMs']: out.append((t+f['aankomstMs'],f['houding'],i,'aankomst'))
        out.append((t_i,f['houding'],i,'fase')); t=t_i
    for x in L.get('eind') or []:
        t+=x.get('ms',600); out.append((t,x['houding'],None,'eind'))
    return sorted(out)
if __name__=='__main__':
    for s in sleutels(sys.argv[1],sys.argv[2]): print(s)
