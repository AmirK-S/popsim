"""Recupere le 12 septembre 2026 depuis un fichier de scratchpad de session (audit2.py,
jamais commite) et integre tel quel dans analyses/, sous ce nom. Ne calcule rien de neuf :
relit resultats/c7-nul-corrige.csv (deja produit par analyses/c7_nul_corrige.py et deja
versionne) et imprime les tables de diagnostic (axes par construction, bruit intra vs
dispersion inter, controles d'exactitude visee, jackknife du rho reel, comparaison a la
loi de Spearman sous H0) qui etayent resultats/audit-renversement-2026-09-12.md. Code de
calcul non modifie ; seul cet en-tete de provenance a ete ajoute.
Usage : .venv/bin/python analyses/c7_audit_lecture_resultats.py
"""
import numpy as np, pandas as pd
from scipy import stats
pd.set_option("display.width",200); pd.set_option("display.max_columns",50)
R="/Users/amirkellousidhoum/Desktop/Code/Projets/popsim/resultats/c7-nul-corrige.csv"
df=pd.read_csv(R)
cfg=df[df.type=="configuration"].copy()
res=df[df.type=="rho_resume"].copy()
rep=df[df.type=="rho_replicat"].copy()
HUM="humains vagues 1-3 (retest)"
n12=[c for c in cfg[cfg.construction=="N1 mode de segment"].configuration]
print("=== A. Axes par construction : moyenne et dispersion INTER-configuration (12 pts) ===")
for c in cfg.construction.unique():
    s=cfg[(cfg.construction==c)&(cfg.configuration!=HUM)]
    print(f"{c:34s} fid moy={s.fidelite_chute.mean():+.5f} sd_inter={s.fidelite_chute.std():.5f} "
          f"| top1 moy={s.top1.mean()*100:.4f}% sd_inter={s.top1.std()*100:.4f}pp "
          f"| exact_vs_verite moy={s.exactitude_contre_verite.mean():.4f} [{s.exactitude_contre_verite.min():.3f};{s.exactitude_contre_verite.max():.3f}]")
print("\n=== B. Bruit intra (demi-largeur IC bootstrap moyenne) vs dispersion inter ===")
for c in cfg.construction.unique():
    s=cfg[(cfg.construction==c)&(cfg.configuration!=HUM)]
    hf=((s.fidelite_boot_haut-s.fidelite_boot_bas)/2).mean()
    ht=((s.top1_boot_haut-s.top1_boot_bas)/2).mean()
    print(f"{c:34s} fid: sd_inter/demiIC={s.fidelite_chute.std()/hf:6.2f}  top1: sd_inter/demiIC={s.top1.std()/ht:6.2f}")
print("\n=== C. Controles d'exactitude visee ===")
for c in cfg.construction.unique():
    s=cfg[(cfg.construction==c)&(cfg.configuration!=HUM)]
    print(f"{c:34s} ecart_moy={s.ecart_exactitude_moyen.mean():.6f} ecart_max={s.ecart_exactitude_max.max():.4f} z_max={s.z_exactitude_max.max():.3f} masque_ident={s.masque_identique.all()}")
print("\n=== D. rho : resume ===")
print(res[["construction","rho_moyen","rho_median","rho_p5","rho_p95","rho_min","rho_max","rho_boot_personnes_bas","rho_boot_personnes_haut","replicats_axe_degenere","replicats_rho_non_defini"]].to_string(index=False))
print("\n=== E. Distribution nulle empirique vs loi de Spearman sous H0 (n=12) ===")
rng=np.random.default_rng(7)
sim=np.array([stats.spearmanr(rng.random(12),rng.random(12)).statistic for _ in range(200000)])
print(f"Spearman H0 n=12 : moyenne={sim.mean():+.4f} p5={np.percentile(sim,5):+.4f} p95={np.percentile(sim,95):+.4f} sd={sim.std():.4f}")
for c in ["N1 mode de segment","N1b mode de segment (Bernoulli)","N2 vecteur d'autrui","N2b vecteur d'autrui (Bernoulli)","N3 identites permutees","N4 mode global"]:
    v=rep[rep.construction==c].rho.values
    if len(v)==0: continue
    ks=stats.ks_2samp(v,sim[:100000])
    print(f"{c:34s} n={len(v):3d} moy={v.mean():+.4f} p95={np.percentile(v,95):+.4f} sd={v.std():.4f} KS vs H0: D={ks.statistic:.3f} p={ks.pvalue:.4f}")
print("\n=== F. rho du reel : valeur, p de Spearman, jackknife retrait 1 point ===")
s=cfg[cfg.construction=="reel"]
s12=s[s.configuration!=HUM]
f=s12.fidelite_chute.values; u=s12.top1.values; noms=list(s12.configuration)
r_all=stats.spearmanr(f,u)
print(f"rho 12 points = {r_all.statistic:.4f}, p={r_all.pvalue:.2e}  (CSV rho_moyen reel={res[res.construction=='reel'].rho_moyen.values[0]:.4f})")
jk=[]
for i in range(12):
    m=np.ones(12,bool); m[i]=False
    jk.append((noms[i],stats.spearmanr(f[m],u[m]).statistic))
for nom,v in sorted(jk,key=lambda z:z[1]): print(f"   sans {nom:48s} rho11={v:.4f}")
vals=np.array([v for _,v in jk]); print(f"   etendue jackknife 12pts : [{vals.min():.4f} ; {vals.max():.4f}]")
f13=s.fidelite_chute.values; u13=s.top1.values; n13=list(s.configuration)
print(f"\nrho 13 points (humain inclus) = {stats.spearmanr(f13,u13).statistic:.4f}")
jk13=[]
for i in range(13):
    m=np.ones(13,bool); m[i]=False
    jk13.append((n13[i],stats.spearmanr(f13[m],u13[m]).statistic))
for nom,v in sorted(jk13,key=lambda z:z[1]): print(f"   sans {nom:48s} rho12={v:.4f}")
v13=np.array([v for _,v in jk13]); print(f"   etendue jackknife 13pts : [{v13.min():.4f} ; {v13.max():.4f}]")
print("\n=== G. verdict avec seuil z=5 prereg : quelles constructions seraient rejetees ===")
for c in cfg.construction.unique():
    if c=="reel": continue
    s=cfg[(cfg.construction==c)&(cfg.configuration!=HUM)]
    print(f"{c:34s} z_max={s.z_exactitude_max.max():.3f} -> {'REJETEE a seuil 5' if s.z_exactitude_max.max()>=5 else 'passe'}")
print("\n=== H. delta identification et a/c par construction ===")
for c in cfg.construction.unique():
    s=cfg[(cfg.construction==c)&(cfg.configuration!=HUM)]
    print(f"{c:34s} a={s.a_vraie_personne.mean():.4f} c={s.c_candidat_hasard.mean():.4f} delta={s.delta_identification.mean():+.5f} bits={s.bits.mean():+.4f}")
print("\n=== I. reel : table par config ===")
print(s12[["configuration","exactitude_contre_verite","fidelite_chute","top1","bits","a_vraie_personne","c_candidat_hasard","delta_identification"]].sort_values("top1",ascending=False).to_string(index=False))
print("\n=== J. N0 vs reel sur JSON Persona - GPT4.1 ===")
print(cfg[(cfg.configuration=="JSON Persona - GPT4.1")][["construction","exactitude_contre_verite","fidelite_chute","top1","bits","a_vraie_personne","c_candidat_hasard","delta_identification"]].to_string(index=False))
