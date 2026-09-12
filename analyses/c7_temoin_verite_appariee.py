# Recupere le 12 septembre 2026 depuis un fichier de scratchpad de session
# (audit_contre_nul.py, jamais commite) et integre tel quel dans analyses/, sous ce nom,
# a la suite de resultats/reproductibilite-chaine-2026-09-12.md (§5) : ce script est celui
# qui produit le chiffre "qui fait autorite" cite par resultats/article-synthese.md et
# resultats/audit-renversement-2026-09-12.md (§1.3) -- rho du temoin de marge corrige
# a exactitude-verite appariee, remplissage marginal : ~0,974 (0,974-0,985 selon le
# remplissage des cellules fausses) contre rho observe 0,965. Code de calcul non modifie ;
# seul cet en-tete de provenance a ete ajoute. Depend de C7_NUL_CACHE (voir
# analyses/c7_nul_corrige.py, chemin par defaut corrige le meme jour) : si ce cache
# n'existe pas encore, lancer d'abord analyses/c7_nul_corrige.py pour le construire.
# Usage : .venv/bin/python analyses/c7_temoin_verite_appariee.py
"""AUDIT ADVERSE. Le nul que c7_nul_corrige n'a PAS construit : celui qui conserve
l'exactitude CONTRE LA VERITE par personne (et donc par configuration), et ne detruit que
le CHOIX des positions exactes. C'est le nul qui correspond a l'objection testee
(« les deux axes sont deux fonctions monotones de la meme marge d'exactitude »).
Lecture seule. Ecrit uniquement dans le scratchpad."""
import os, sys, pickle, time
for _v in ("OMP_NUM_THREADS","OPENBLAS_NUM_THREADS","MKL_NUM_THREADS","NUMEXPR_NUM_THREADS","VECLIB_MAXIMUM_THREADS"):
    os.environ.setdefault(_v,"4")
import numpy as np
from scipy import stats
sys.path.insert(0,"/Users/amirkellousidhoum/Desktop/Code/Projets/popsim/analyses")
import t1_commun as T1, c7_reidentification as C7, c7_bits as CB
from c7_nul_corrige import chute_par_personne, top1_par_personne, marge_par_personne, STATISTIQUES, CACHE
GRAINE=20260912; N_REP=int(os.environ.get("NREP","20")); N_PERM=40; N_TIR=3
t0=time.time(); paq=T1.charger(); codes=paq["codes"]; seg=paq["seg"]["S_gra"]; n_total=paq["n"]
items=C7.items_communs(codes,[C7.REF_V4,C7.REF_V13]); k_items=paq["k_items"][items]
y_ref=codes[C7.REF_V4][:,items]
noms_12=list(C7.CONFIGURATIONS)+STATISTIQUES
pred={n:codes[n][:,items] for n in C7.CONFIGURATIONS}
cache=pickle.load(open(CACHE,"rb")); assert list(cache["items"])==list(items)
for n in STATISTIQUES: pred[n]=cache["base"][n]
couverts={n:np.flatnonzero((pred[n]>=0).any(axis=1)) for n in noms_12}
print(f"{n_total} personnes, {len(items)} items, charge {time.time()-t0:.0f}s",flush=True)

# marginales de population par item, pour les cellules FAUSSES (jamais la valeur de la personne)
vals_j=[];p_j=[]
for j in range(len(items)):
    col=y_ref[:,j]; col=col[col>=0]; v,c=np.unique(col,return_counts=True)
    vals_j.append(v); p_j.append(c/c.sum())

def faux_marginal(y,rng):
    out=np.empty_like(y)
    for j in range(y.shape[1]):
        t=rng.choice(vals_j[j],size=y.shape[0],p=p_j[j]); col=y[:,j]
        bad=t==col
        while bad.any():
            t[bad]=rng.choice(vals_j[j],size=int(bad.sum()),p=p_j[j]); bad=t==col
        out[:,j]=t
    return out

def faux_uniforme(y,rng):
    n=y.shape[0]
    f=rng.integers(0,np.maximum(k_items-1,1)[None,:].repeat(n,axis=0))
    return np.where(k_items[None,:]>1,f+(f>=y),y).astype(y.dtype)

def nul_exactitude_verite(x,y,rng,mode):
    """Exactement le meme nombre de cellules exactes CONTRE y que le prediteur reel,
    positions tirees au hasard, contenu faux venant de la population."""
    masque,q,n_obs=marge_par_personne(x,y)
    u=np.where(masque,rng.random(x.shape),np.inf)
    rang=np.argsort(np.argsort(u,axis=1,kind="stable"),axis=1)
    correct=rang<np.rint(q*n_obs).astype(np.int64)[:,None]
    faux=faux_marginal(y,rng) if mode=="marginal" else faux_uniforme(y,rng)
    return np.where(masque,np.where(correct,y,faux),-1).astype(x.dtype)

for mode in ("marginal","uniforme"):
    rhos=np.empty(N_REP); tab={n:[] for n in noms_12}; fidt={n:[] for n in noms_12}; exa={n:[] for n in noms_12}
    for r in range(N_REP):
        fid,fui={},{}
        for nom in noms_12:
            cv=couverts[nom]; x,y,s=pred[nom][cv],y_ref[cv],seg[cv]
            rng=np.random.default_rng([GRAINE,999,r,C7.graine_nom(nom),0 if mode=="marginal" else 1])
            out=nul_exactitude_verite(x,y,rng,mode)
            rc=np.random.default_rng([GRAINE,4,r,C7.graine_nom(nom)])
            a,ap=chute_par_personne(out,y,s,N_PERM,rc)
            rf=np.random.default_rng([GRAINE,5,r,C7.graine_nom(nom)])
            t1=top1_par_personne(out,y_ref,cv,rf,n_tirages=N_TIR)
            fid[nom]=float(np.nanmean(a)-np.nanmean(ap)); fui[nom]=float(np.mean(t1))
            tab[nom].append(fui[nom]); fidt[nom].append(fid[nom])
            from a44_mesures import exactitude_codes
            exa[nom].append(float(np.nanmean(exactitude_codes(out,y))))
        rhos[r]=stats.spearmanr([fid[n] for n in noms_12],[fui[n] for n in noms_12]).statistic
        if r%5==0: print(f"  [{mode}] rep {r} rho={rhos[r]:.4f} {time.time()-t0:.0f}s",flush=True)
    print(f"\n=== NUL A EXACTITUDE-VERITE APPARIEE, remplissage {mode} ({N_REP} replicats) ===")
    print(f"rho moyen={rhos.mean():+.4f} mediane={np.median(rhos):+.4f} p5={np.percentile(rhos,5):+.4f} "
          f"p95={np.percentile(rhos,95):+.4f} min={rhos.min():+.4f} max={rhos.max():+.4f}")
    print(f"rho reel observe = 0.9650 -> le depasse-t-il ? {bool(0.965>np.percentile(rhos,95))}")
    print(f"{'configuration':50s} {'exact':>7s} {'chute':>9s} {'top1 %':>8s}")
    for nom in sorted(noms_12,key=lambda n:-np.mean(tab[n])):
        print(f"{nom:50s} {np.mean(exa[nom]):7.4f} {np.mean(fidt[nom]):+9.5f} {100*np.mean(tab[nom]):8.3f}")
    print(flush=True)

# --- angle 6 : SUPPRIME le 12 septembre 2026 (correctifs-artefact-2026-09-12.md, defaut 1).
# Ce bloc plantait ici (IndexError : la table de frequences marginales par item etait
# dimensionnee sur les seules valeurs observees de y_ref, trop petite pour les cellules
# fabriquees par faux_uniforme). Il etait redondant avec analyses/c7_audit_decomposition.py,
# qui calcule exactement la meme decomposition (meme configuration "JSON Persona - GPT4.1",
# memes graines [GRAINE,12345]/[GRAINE,12346], meme fonction nul_exactitude_verite/nul) avec
# une table dimensionnee en securite (K = max(k_items.max(), y_ref.max()+1)+2) qui ne plante
# pas. Preuve de redondance : avant le plantage, la ligne "jumeau REEL" de ce bloc imprimait
# justes c=0.4776 (n=72901) | fausses c=0.3660 (n=50579), des valeurs strictement identiques
# a celles deja imprimees par c7_audit_decomposition.py. Le chiffre central de ce script
# (rho 0.9741 marginal / 0.9815 uniforme / 0.9650 observe, imprime plus haut) n'est pas
# affecte : ce calcul n'y touche pas.
print(f"termine {time.time()-t0:.0f}s")
