"""Recupere le 12 septembre 2026 depuis un fichier de scratchpad de session (audit3.py,
jamais commite) et integre tel quel dans analyses/, sous ce nom. Calcule la decomposition
« angle 6 » de resultats/audit-renversement-2026-09-12.md (defaut 4) : la coincidence c
avec un candidat au hasard, ventilee entre cellules justes et fausses, pour le jumeau reel
et pour le nul a exactitude-verite appariee (analyses/c7_temoin_verite_appariee.py) ; puis
relit resultats/c7-nul-corrige.csv pour la table complementaire par construction. Code de
calcul non modifie ; seul cet en-tete de provenance a ete ajoute. Depend de C7_NUL_CACHE
(voir analyses/c7_nul_corrige.py) comme c7_temoin_verite_appariee.py.
Usage : .venv/bin/python analyses/c7_audit_decomposition.py
"""
import os,sys,pickle,time
for _v in ("OMP_NUM_THREADS","OPENBLAS_NUM_THREADS","MKL_NUM_THREADS"): os.environ.setdefault(_v,"4")
import numpy as np, pandas as pd
sys.path.insert(0,"/Users/amirkellousidhoum/Desktop/Code/Projets/popsim/analyses")
import t1_commun as T1, c7_reidentification as C7
from c7_nul_corrige import marge_par_personne
GRAINE=20260912
paq=T1.charger(); codes=paq["codes"]; items=C7.items_communs(codes,[C7.REF_V4,C7.REF_V13])
k_items=paq["k_items"][items]; y_ref=codes[C7.REF_V4][:,items]
nom="JSON Persona - GPT4.1"; x=codes[nom][:,items]; y=y_ref
K=int(max(k_items.max(),y_ref.max()+1))+2
PM=np.zeros((len(items),K))
for j in range(len(items)):
    col=y_ref[:,j]; col=col[col>=0]; v,c=np.unique(col,return_counts=True); PM[j,v]=c/c.sum()
def c_moyen(out,sel):
    tot=0.;cnt=0
    for j in range(out.shape[1]):
        s=sel[:,j]&(out[:,j]>=0)
        if s.sum()==0: continue
        tot+=PM[j,out[s,j]].sum(); cnt+=int(s.sum())
    return tot/cnt,cnt
def faux_uniforme(y,rng):
    n=y.shape[0]; f=rng.integers(0,np.maximum(k_items-1,1)[None,:].repeat(n,axis=0))
    return np.where(k_items[None,:]>1,f+(f>=y),y).astype(y.dtype)
def faux_marginal(y,rng):
    out=np.empty_like(y)
    for j in range(y.shape[1]):
        v=np.flatnonzero(PM[j]>0); p=PM[j,v]
        t=rng.choice(v,size=y.shape[0],p=p); col=y[:,j]; bad=t==col
        while bad.any(): t[bad]=rng.choice(v,size=int(bad.sum()),p=p); bad=t==col
        out[:,j]=t
    return out
def nul(x,y,rng,mode):
    m,q,n_obs=marge_par_personne(x,y)
    u=np.where(m,rng.random(x.shape),np.inf)
    rang=np.argsort(np.argsort(u,axis=1,kind="stable"),axis=1)
    ok=rang<np.rint(q*n_obs).astype(np.int64)[:,None]
    f=faux_marginal(y,rng) if mode=="marginal" else faux_uniforme(y,rng)
    return np.where(m,np.where(ok,y,f),-1).astype(x.dtype)
print("=== ANGLE 6 : c (coincidence avec un candidat au hasard) par type de cellule ===")
for lab,out in [("jumeau REEL",x),
                ("nul exact-verite, remplissage UNIFORME",nul(x,y,np.random.default_rng([GRAINE,12345]),"uniforme")),
                ("nul exact-verite, remplissage MARGINAL",nul(x,y,np.random.default_rng([GRAINE,12346]),"marginal"))]:
    j=(out>=0)&(out==y); f=(out>=0)&(out!=y)
    cj,nj=c_moyen(out,j); cf,nf=c_moyen(out,f); ct,nt=c_moyen(out,out>=0)
    print(f"{lab:42s} c_global={ct:.4f} | c_cellules_JUSTES={cj:.4f} | c_cellules_FAUSSES={cf:.4f} | part fausses={nf/nt:.3f}")
print("\n=== Table A complete (CSV) : axes par construction, 12 configs ===")
df=pd.read_csv("/Users/amirkellousidhoum/Desktop/Code/Projets/popsim/resultats/c7-nul-corrige.csv")
cfg=df[df.type=="configuration"]; HUM="humains vagues 1-3 (retest)"
for c in cfg.construction.unique():
    s=cfg[(cfg.construction==c)&(cfg.configuration!=HUM)]
    print(f"{c:34s} exact_vs_VERITE={s.exactitude_contre_verite.mean():.4f} [{s.exactitude_contre_verite.min():.3f};{s.exactitude_contre_verite.max():.3f}] "
          f"| fid={s.fidelite_chute.mean():+.5f} sd={s.fidelite_chute.std():.5f} | top1={100*s.top1.mean():.4f}% "
          f"[{100*s.top1.min():.4f};{100*s.top1.max():.4f}] sd={100*s.top1.std():.4f}pp")
print(f"\nhasard pur = {100/2058:.4f}%")
