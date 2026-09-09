"""
a4 : mesure du bridage thermique sous charge continue, sur un MacBook Air M5.

Statut : banc de mesure, pas du code de production. Il existe pour lever la limite
numero 3 du rapport resultats/a3-inference-locale.md, qui dit que la stabilite thermique
sur plusieurs heures n'est pas mesuree et que la plus longue serie du banc a3 dure
18 secondes.

Pourquoi la question se pose sur cette machine precisement. Le Mac17,3 est un MacBook Air.
Il n'a pas de ventilateur : la chaleur sort par le chassis, en convection passive. Un
MacBook Pro, lui, monte ses ventilateurs et tient un regime eleve beaucoup plus longtemps.
Toute duree de production annoncee a partir d'une mesure de 18 secondes suppose que le
debit des 18 premieres secondes vaut pour les sept heures suivantes. C'est exactement
l'hypothese que ce script teste.

Ce qu'il mesure :
  P0  l'etat de la machine avant de commencer, et le refus de mesurer si elle travaille
  P1  le debit d'une charge continue et representative, echantillonne par fenetres d'une
      minute : appels traites, prefill a froid, prefill du delta de question, decodage,
      latence par appel
  P2  les indicateurs de bridage accessibles sans privilege administrateur, releves a
      chaque fenetre : temperature de la batterie, avertissements pmset, charge systeme
  P3  la pente du debit sur la seconde moitie de la serie, qui dit si la courbe s'est
      stabilisee ou si elle descendait encore a la fin

La charge est celle de la phase 1 du projet : un persona factice d'environ 3 000 tokens
place en tete et fige, puis des questions fermees courtes en queue, en boucle, avec le
cache de prefixe actif. Une fois par fenetre, un prefill a froid du persona entier est
force sur un autre slot : c'est la partie la plus dependante du GPU, donc la plus
sensible au bridage, et c'est aussi ce que la phase 1 paie 900 fois.

Entree  : aucune. Le persona et les questions sont FACTICES, importes de
          a3_banc_inference pour qu'ils soient identiques octet pour octet a ceux du banc
          a3. Aucune donnee d'enquete n'entre ici, et rien ne sort de la machine.
Sortie  : un tableau sur la sortie standard, un JSON de mesures brutes dans
          resultats/mesures-a4/, et la figure resultats/a4-bridage-thermique.{png,svg}.

Configuration du serveur : celle qui donne le meilleur debit absolu du rapport a3,
section 4.7, c'est a dire -np 8 avec cache KV en q8_0 et --cache-reuse 256, interroge par
un seul flux. Les options ne sont pas reinventees ici, elles sont recopiees.

Aucun sudo. Les seuls indicateurs employes sont ceux qu'un utilisateur ordinaire peut
lire : pmset -g therm, pmset -g batt, os.getloadavg, et la temperature de la batterie
exposee par ioreg -rc AppleSmartBattery.

Usage :
  python3 analyses/a4_bridage_thermique.py                 # dix minutes, valeur imposee
  python3 analyses/a4_bridage_thermique.py --minutes 60    # serie longue, si demandee
  python3 analyses/a4_bridage_thermique.py --figure-seule  # retrace depuis le JSON

Duree : la duree demandee, plus une trentaine de secondes de mise en place.
"""

import argparse
import json
import os
import re
import statistics
import subprocess
import sys
import time

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RACINE, "analyses"))

from a3_banc_inference import MoteurLlama, fabriquer_persona, fabriquer_questions  # noqa: E402

SORTIE = os.path.join(RACINE, "resultats")
MESURES = os.path.join(SORTIE, "mesures-a4")

MODELE_DEFAUT = os.path.join(RACINE, "data", "modeles", "gguf",
                             "Qwen3-4B-Instruct-2507-Q4_K_M.gguf")

# Seuils du controle de repos. La regle vient du rapport a3, section 1.3 : une campagne
# entiere a ete jetee parce que trois demons iCloud tournaient pendant la mesure, ce qui
# avait sous-estime le prefill de 40 pour cent. La machine au repos a ete relevee entre
# 2,0 et 3,2 de charge moyenne sur dix coeurs pendant toute la campagne a3.
CHARGE_MAX_AU_REPOS = 4.0
PROCESSUS_A_SURVEILLER = ("bird", "fileproviderd", "CloudDocs", "cloudd",
                          "spotlightknowledged", "mds", "mds_stores", "corespotlightd",
                          "XProtect", "Dolittle", "photoanalysisd", "backupd",
                          "mediaanalysisd", "Time Machine")
CPU_SUSPECT = 20.0          # pour cent d'un coeur, au dela le demon travaille vraiment


# --------------------------------------------------------------------------------------
# 1. Les indicateurs systeme, tous lisibles sans sudo
# --------------------------------------------------------------------------------------

def _commande(argv, timeout=20):
    """Execute une commande et rend sa sortie, ou une chaine vide si elle echoue."""
    try:
        r = subprocess.run(argv, capture_output=True, text=True, timeout=timeout)
        return r.stdout
    except Exception:
        return ""


def temperature_batterie_c():
    """Temperature de la batterie en degres Celsius, ou None.

    C'est le seul capteur thermique que macOS 26 expose a un utilisateur ordinaire.
    ioreg le publie en centiemes de degre. Ce n'est PAS la temperature du SoC : la
    batterie est une masse thermique lente, collee au chassis. Sur un Air sans
    ventilateur, le chassis est justement le radiateur, donc cette valeur suit la
    chaleur evacuee avec un retard de quelques minutes. Elle sert d'indicateur de
    tendance, jamais de mesure de jonction.
    """
    sortie = _commande(["ioreg", "-rc", "AppleSmartBattery"])
    m = re.search(r'"Temperature"\s*=\s*(-?\d+)', sortie)
    return int(m.group(1)) / 100.0 if m else None


def pmset_therm():
    """Sortie brute de pmset -g therm, et le facteur de bridage s'il est publie.

    Quand le systeme bride reellement, pmset publie CPU_Speed_Limit, un pourcentage de
    la frequence nominale encore autorisee. Tant que rien n'est bride, il ecrit
    "No CPU power status has been recorded". L'absence de ligne n'est donc pas la preuve
    d'une absence de bridage GPU : pmset ne parle que du CPU, et le GPU Metal peut
    descendre sans qu'aucune ligne n'apparaisse. C'est une limite a assumer, pas a
    contourner sans sudo.
    """
    brut = _commande(["pmset", "-g", "therm"]).strip()
    limite = None
    m = re.search(r"CPU_Speed_Limit\s*=\s*(\d+)", brut)
    if m:
        limite = int(m.group(1))
    return {"brut": brut, "cpu_speed_limit": limite}


def pmset_batt():
    return _commande(["pmset", "-g", "batt"]).strip()


def processus_lourds(seuil=5.0, combien=12):
    """Les processus les plus consommateurs, echantillonnes a l'instant present.

    ps donne un pourcentage CPU moyenne depuis le lancement du processus, ce qui est
    inutile ici. top avec deux echantillons donne la valeur instantanee : on jette le
    premier echantillon et on lit le second.
    """
    sortie = _commande(["top", "-l", "2", "-n", str(combien), "-o", "cpu", "-s", "1",
                        "-stats", "pid,cpu,command"], timeout=30)
    blocs = sortie.split("PID")
    if len(blocs) < 3:
        return []
    lignes = blocs[-1].splitlines()[1:]
    trouves = []
    for ligne in lignes:
        champs = ligne.split(None, 2)
        if len(champs) < 3:
            continue
        try:
            cpu = float(champs[1].replace(",", "."))
        except ValueError:
            continue
        if cpu >= seuil:
            trouves.append({"pid": champs[0], "cpu": cpu, "commande": champs[2].strip()})
    return trouves


def releve_etat(avec_processus=True):
    """Un releve complet de l'etat de la machine, horodate."""
    charge = os.getloadavg()
    etat = {
        "horodatage": time.strftime("%Y-%m-%d %H:%M:%S"),
        "charge_1_5_15": [round(c, 2) for c in charge],
        "temperature_batterie_c": temperature_batterie_c(),
        "pmset_therm": pmset_therm(),
    }
    if avec_processus:
        etat["pmset_batt"] = pmset_batt()
        etat["processus_lourds"] = processus_lourds()
    return etat


def machine_au_repos(etat):
    """Rend (verdict, motifs). Le verdict commande le lancement de la mesure."""
    motifs = []
    if etat["charge_1_5_15"][0] > CHARGE_MAX_AU_REPOS:
        motifs.append(f"charge moyenne a {etat['charge_1_5_15'][0]} sur dix coeurs, "
                      f"au dessus du seuil de {CHARGE_MAX_AU_REPOS}")
    for p in etat.get("processus_lourds", []):
        nom = os.path.basename(p["commande"].split()[0]) if p["commande"] else ""
        if any(s.lower() in p["commande"].lower() for s in PROCESSUS_A_SURVEILLER) \
                and p["cpu"] >= CPU_SUSPECT:
            motifs.append(f"{nom} a {p['cpu']} pour cent d'un coeur")
    if "AC Power" not in etat.get("pmset_batt", ""):
        motifs.append("machine sur batterie : macOS bride alors deliberement, la mesure "
                      "ne porterait plus sur la thermique")
    return (len(motifs) == 0), motifs


# --------------------------------------------------------------------------------------
# 2. La charge continue
# --------------------------------------------------------------------------------------

def un_appel(moteur, prompt, cache=True):
    """Un appel de la phase 1 : un passage avant, lecture des probabilites, rien de plus.

    Rend la latence mesuree cote client, qui est celle qui compte pour un plan de
    travail, et les temps internes rapportes par le serveur, qui disent ou passe le
    temps.
    """
    t0 = time.perf_counter()
    r = moteur._poster("/completion", {
        "prompt": prompt,
        "n_predict": 1,
        "n_probs": 40,
        "temperature": 0.0,
        "cache_prompt": cache,
        "post_sampling_probs": False,
    })
    latence_ms = (time.perf_counter() - t0) * 1000.0
    t = r.get("timings", {})
    return {
        "latence_ms": latence_ms,
        "prompt_n": t.get("prompt_n"),
        "prompt_ms": t.get("prompt_ms"),
        "predicted_n": t.get("predicted_n"),
        "predicted_ms": t.get("predicted_ms"),
    }


def sonde_decodage(moteur, prompt, n_predict=32):
    """Mesure le debit de decodage, hors de la boucle de charge.

    Necessaire parce qu'un appel a n_predict=1 ne donne aucun temps de generation
    exploitable : llama.cpp compte ce token unique dans le temps de prompt et rapporte
    un predicted_ms voisin de zero, ce qui produit des debits de l'ordre du million de
    tokens par seconde. Trente-deux tokens suffisent a obtenir une valeur stable.
    """
    r = moteur._poster("/completion", {"prompt": prompt, "n_predict": n_predict,
                                       "temperature": 0.0, "cache_prompt": True})
    t = r.get("timings", {})
    if t.get("predicted_ms"):
        return t["predicted_n"] / t["predicted_ms"] * 1000.0
    return None


def agreger(appels):
    """Agrege une liste d'appels en debits. Les t/s sont des rapports de sommes.

    Faire la moyenne des t/s appel par appel donnerait un poids identique a un appel qui
    evalue 3 000 tokens et a un appel qui en evalue 64. Le rapport des sommes est le seul
    agregat correct.
    """
    if not appels:
        return None
    lat = [a["latence_ms"] for a in appels]
    p_n = sum(a["prompt_n"] or 0 for a in appels)
    p_ms = sum(a["prompt_ms"] or 0.0 for a in appels)
    d_n = sum(a["predicted_n"] or 0 for a in appels)
    d_ms = sum(a["predicted_ms"] or 0.0 for a in appels)
    return {
        "appels": len(appels),
        "latence_moyenne_ms": statistics.fmean(lat),
        "latence_mediane_ms": statistics.median(lat),
        "latence_ecart_type_ms": statistics.pstdev(lat) if len(lat) > 1 else 0.0,
        "latence_min_ms": min(lat),
        "latence_max_ms": max(lat),
        "prefill_delta_t_s": (p_n / p_ms * 1000.0) if p_ms else None,
        "decodage_t_s": (d_n / d_ms * 1000.0) if d_ms else None,
        "appels_par_heure": 3600.0 / (statistics.fmean(lat) / 1000.0),
    }


def pente_ols(x, y):
    """Pente d'une regression lineaire simple, avec son erreur type et son t.

    Ecrite a la main plutot qu'importee : le script doit tourner sans numpy si besoin,
    et la formule tient en six lignes. Rend None si la variance de x est nulle.
    """
    n = len(x)
    if n < 3:
        return None
    mx, my = statistics.fmean(x), statistics.fmean(y)
    sxx = sum((v - mx) ** 2 for v in x)
    if sxx == 0:
        return None
    sxy = sum((x[i] - mx) * (y[i] - my) for i in range(n))
    b = sxy / sxx
    a = my - b * mx
    residus = [y[i] - (a + b * x[i]) for i in range(n)]
    if n <= 2:
        return None
    s2 = sum(r * r for r in residus) / (n - 2)
    se = (s2 / sxx) ** 0.5 if sxx else None
    return {"pente": b, "ordonnee": a, "erreur_type": se,
            "t": (b / se) if se else None, "n": n,
            "ic95_bas": b - 1.96 * se if se else None,
            "ic95_haut": b + 1.96 * se if se else None}


def campagne(moteur, persona, persona_froid, questions, minutes, fenetre_s):
    """La boucle de charge. Rend la liste des fenetres et la liste brute des appels."""
    fenetres = []
    tous = []
    t_debut = time.perf_counter()
    i_question = 0
    n_fenetres = int(round(minutes * 60 / fenetre_s))

    for k in range(n_fenetres):
        t_fin_fenetre = t_debut + (k + 1) * fenetre_s
        etat_entree = releve_etat(avec_processus=False)

        # Le prefill a froid de la fenetre. Persona different de celui de la boucle, donc
        # le serveur le range dans un autre slot et le cache du persona chaud survit.
        # cache_prompt=false force la reevaluation complete des 3 000 tokens.
        froid = un_appel(moteur, persona_froid + questions[0], cache=False)
        # Le slot du persona froid vient d'etre rempli : la sonde de decodage y reprend
        # le cache et ne paie que la generation.
        decodage_t_s = sonde_decodage(moteur, persona_froid + questions[0])

        appels = []
        while time.perf_counter() < t_fin_fenetre:
            a = un_appel(moteur, persona + questions[i_question % len(questions)])
            a["t_s"] = time.perf_counter() - t_debut
            appels.append(a)
            tous.append(a)
            i_question += 1

        etat_sortie = releve_etat(avec_processus=False)
        agr = agreger(appels) or {}
        agr.update({
            "fenetre": k + 1,
            "minute": (k + 1) * fenetre_s / 60.0,
            "prefill_froid_t_s": ((froid["prompt_n"] / froid["prompt_ms"] * 1000.0)
                                  if froid["prompt_ms"] else None),
            "prefill_froid_tokens": froid["prompt_n"],
            "prefill_froid_ms": froid["prompt_ms"],
            "decodage_sonde_t_s": decodage_t_s,
            "charge_entree": etat_entree["charge_1_5_15"][0],
            "charge_sortie": etat_sortie["charge_1_5_15"][0],
            "temperature_batterie_c": etat_sortie["temperature_batterie_c"],
            "pmset_therm": etat_sortie["pmset_therm"]["brut"],
            "cpu_speed_limit": etat_sortie["pmset_therm"]["cpu_speed_limit"],
            "memoire_serveur_mo": moteur.memoire_rss_mo(),
        })
        fenetres.append(agr)
        print(f"  minute {agr['minute']:5.1f}  "
              f"{agr['appels']:5d} appels  "
              f"{agr['appels_par_heure']:8.0f} appels/h  "
              f"prefill froid {agr['prefill_froid_t_s'] or float('nan'):6.1f} t/s  "
              f"delta {agr['prefill_delta_t_s'] or float('nan'):6.1f} t/s  "
              f"decodage {agr['decodage_sonde_t_s'] or float('nan'):5.1f} t/s  "
              f"latence {agr['latence_moyenne_ms']:6.1f} ms  "
              f"charge {agr['charge_sortie']:4.2f}  "
              f"batterie {agr['temperature_batterie_c']} C",
              flush=True)
    return fenetres, tous


# --------------------------------------------------------------------------------------
# 3. L'analyse
# --------------------------------------------------------------------------------------

def analyser(fenetres, tous):
    """Compare la premiere et la derniere fenetre, et cherche une pente residuelle.

    Le point decisif du rapport n'est pas la perte totale, c'est de savoir si la courbe
    etait plate a la fin. Deux tests, volontairement redondants :
      1. la pente sur les points de fenetre de la seconde moitie, cinq points seulement,
         donc peu puissante ;
      2. la pente sur tous les appels individuels de la seconde moitie, plusieurs
         milliers de points, qui tranche vraiment.
    """
    if not fenetres:
        return {}
    prem, dern = fenetres[0], fenetres[-1]
    perte = (1 - dern["appels_par_heure"] / prem["appels_par_heure"]) * 100.0

    moitie = len(fenetres) // 2
    secondes = fenetres[moitie:]
    pente_fenetres = pente_ols([f["minute"] for f in secondes],
                               [f["appels_par_heure"] for f in secondes])

    t_moitie = tous[-1]["t_s"] / 2.0 if tous else 0.0
    fin = [a for a in tous if a["t_s"] >= t_moitie]
    pente_appels = pente_ols([a["t_s"] / 60.0 for a in fin],
                             [3600.0 / (a["latence_ms"] / 1000.0) for a in fin])

    # Verdict de stabilisation. On declare stabilise si la pente de la seconde moitie
    # n'est pas distinguable de zero, ou si elle est si faible qu'elle ne represente pas
    # 1 pour cent du debit par minute.
    verdict = "indetermine"
    if pente_appels:
        seuil = 0.01 * dern["appels_par_heure"]      # 1 pour cent du debit, par minute
        significatif = abs(pente_appels["t"] or 0) > 2.0
        materiel = abs(pente_appels["pente"]) > seuil
        if significatif and materiel and pente_appels["pente"] < 0:
            verdict = "encore en descente"
        elif significatif and materiel and pente_appels["pente"] > 0:
            verdict = "encore en remontee"
        else:
            verdict = "stabilisee"

    temps = [f["temperature_batterie_c"] for f in fenetres if f["temperature_batterie_c"]]
    pente_temp = None
    if len(temps) >= 3:
        pente_temp = pente_ols([f["minute"] for f in fenetres[moitie:]
                                if f["temperature_batterie_c"]],
                               [f["temperature_batterie_c"] for f in fenetres[moitie:]
                                if f["temperature_batterie_c"]])

    return {
        "premiere_fenetre_appels_h": prem["appels_par_heure"],
        "derniere_fenetre_appels_h": dern["appels_par_heure"],
        "perte_pour_cent": perte,
        "premiere_fenetre_latence_ms": prem["latence_moyenne_ms"],
        "derniere_fenetre_latence_ms": dern["latence_moyenne_ms"],
        "prefill_froid_premier_t_s": prem["prefill_froid_t_s"],
        "prefill_froid_dernier_t_s": dern["prefill_froid_t_s"],
        "decodage_premier_t_s": prem.get("decodage_sonde_t_s"),
        "decodage_dernier_t_s": dern.get("decodage_sonde_t_s"),
        "meilleure_fenetre_appels_h": max(f["appels_par_heure"] for f in fenetres),
        "pire_fenetre_appels_h": min(f["appels_par_heure"] for f in fenetres),
        "pente_seconde_moitie_fenetres": pente_fenetres,
        "pente_seconde_moitie_appels": pente_appels,
        "verdict_stabilisation": verdict,
        "temperature_debut_c": temps[0] if temps else None,
        "temperature_fin_c": temps[-1] if temps else None,
        "pente_temperature_seconde_moitie": pente_temp,
    }


def traduire_phase1(analyse, duree_reference_h, etiquette):
    """Applique le facteur mesure aux durees de la phase 1 du rapport a3.

    Deux bornes, et il faut dire ce que chacune vaut :
      borne basse  : la degradation s'arrete la ou elle en etait a la fin de la mesure,
                     donc on applique le facteur de la derniere fenetre. C'est un
                     PLANCHER, valable seulement si la courbe s'est stabilisee ;
      borne haute  : la pente residuelle mesuree se prolonge lineairement. C'est une
                     EXTRAPOLATION, et elle ne vaut que si rien ne l'arrete.
    Aucune des deux n'est une mesure sur sept heures. Le rapport doit le dire.
    """
    facteur_fin = analyse["derniere_fenetre_appels_h"] / analyse["premiere_fenetre_appels_h"]
    basse = duree_reference_h / facteur_fin
    return {"modele": etiquette, "duree_a3_h": duree_reference_h,
            "facteur_fin": facteur_fin, "duree_plancher_h": basse}


def hm(heures):
    """Formate un nombre d'heures en h et min, sans jamais arrondir a la demi-heure."""
    h = int(heures)
    m = int(round((heures - h) * 60))
    if m == 60:
        h, m = h + 1, 0
    return f"{h} h {m:02d}"


# --------------------------------------------------------------------------------------
# 4. La figure
# --------------------------------------------------------------------------------------

def tracer(fenetres, analyse, chemin_sans_extension):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    FOND, ENCRE, ENCRE2, GRILLE = "#fcfcfb", "#0b0b0b", "#52514e", "#e2e1dd"
    BLEU, ORANGE = "#2a78d6", "#eb6834"

    x = [f["minute"] for f in fenetres]
    y = [f["appels_par_heure"] for f in fenetres]
    froid = [f["prefill_froid_t_s"] for f in fenetres]
    temp = [f["temperature_batterie_c"] for f in fenetres]

    fig, (h, b) = plt.subplots(2, 1, figsize=(9, 7.2), sharex=True,
                               gridspec_kw={"height_ratios": [2.1, 1]})
    fig.patch.set_facecolor(FOND)
    for ax in (h, b):
        ax.set_facecolor(FOND)
        ax.grid(True, color=GRILLE, linewidth=0.8)
        ax.set_axisbelow(True)
        for cote in ("top", "right"):
            ax.spines[cote].set_visible(False)
        for cote in ("left", "bottom"):
            ax.spines[cote].set_color(GRILLE)
        ax.tick_params(colors=ENCRE2)

    h.plot(x, y, marker="o", color=BLEU, linewidth=2.0, markersize=5,
           label="debit en regime etabli, appels par heure")
    h.axhline(y[0], color=ENCRE2, linewidth=0.9, linestyle="--")
    h.annotate(f"{y[0]:.0f}", (x[0], y[0]), textcoords="offset points",
               xytext=(4, 8), color=ENCRE, fontsize=9)
    h.annotate(f"{y[-1]:.0f}", (x[-1], y[-1]), textcoords="offset points",
               xytext=(-40, -14), color=ENCRE, fontsize=9)
    # De la place au dessus pour la legende, et en dessous pour l'etiquette du dernier
    # point : sans cette marge les deux se posent sur les courbes.
    h.set_ylim(min(y) * 0.90, max(y) * 1.16)

    # La pente residuelle de la seconde moitie, tracee en pointille. C'est le point
    # decisif du rapport : si ce trait est plat, dix minutes suffisent ; s'il descend,
    # elles ne suffisent pas.
    pa = analyse.get("pente_seconde_moitie_appels")
    if pa:
        moitie = len(x) // 2
        xs = x[moitie:]
        ys = [pa["ordonnee"] + pa["pente"] * v for v in xs]
        h.plot(xs, ys, linestyle=":", color=ENCRE2, linewidth=1.6,
               label=f"pente de la seconde moitie, {pa['pente']:+.0f} appels/h par minute")
    h.set_ylabel("appels par heure", color=ENCRE)
    h.set_title("Debit d'inference sous charge continue, MacBook Air M5 sans ventilateur\n"
                f"Qwen3-4B en 4 bits, llama.cpp, perte de {analyse['perte_pour_cent']:.1f} "
                f"pour cent entre la premiere et la derniere minute",
                color=ENCRE, fontsize=11, loc="left")

    d = h.twinx()
    d.plot(x, froid, marker="s", color=ORANGE, linewidth=1.6, markersize=4,
           label="prefill a froid du persona, tokens par seconde")
    d.set_ylabel("prefill a froid, tokens par seconde", color=ORANGE)
    d.tick_params(colors=ORANGE)
    d.spines["top"].set_visible(False)
    d.spines["right"].set_color(GRILLE)

    lignes = [l for l in h.get_lines() if not l.get_label().startswith("_")] + d.get_lines()
    h.legend(lignes, [l.get_label() for l in lignes], loc="upper right", ncol=1, frameon=False, fontsize=9, labelcolor=ENCRE2)

    b.plot(x, temp, marker="^", color="#a03030", linewidth=1.8, markersize=4)
    b.set_ylabel("temperature de la\nbatterie, degres", color=ENCRE)
    b.set_xlabel("temps sous charge, minutes", color=ENCRE)
    b.set_xticks(x)

    fig.tight_layout()
    for ext in ("png", "svg"):
        fig.savefig(f"{chemin_sans_extension}.{ext}", dpi=160, facecolor=FOND)
    plt.close(fig)


# --------------------------------------------------------------------------------------
# 5. Le programme
# --------------------------------------------------------------------------------------

def main():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--modele", default=MODELE_DEFAUT)
    p.add_argument("--minutes", type=float, default=10.0,
                   help="duree de la charge continue. Dix minutes est la valeur imposee "
                        "par la consigne de la mission a4")
    p.add_argument("--fenetre", type=float, default=60.0, help="taille d'une fenetre, en s")
    p.add_argument("--parallele", type=int, default=8,
                   help="slots du serveur. 8 est la configuration de reference du "
                        "rapport a3 section 4.7, celle du meilleur debit absolu")
    p.add_argument("--port", type=int, default=8097)
    p.add_argument("--mots-persona", type=int, default=1650)
    p.add_argument("--questions", type=int, default=50)
    p.add_argument("--attente-repos", type=int, default=6,
                   help="nombre de tentatives de 30 s avant d'abandonner si la machine "
                        "n'est pas au repos")
    p.add_argument("--forcer", action="store_true",
                   help="mesure meme si la machine travaille. La mesure ne vaudra rien, "
                        "et le JSON le consignera")
    p.add_argument("--figure-seule", default=None,
                   help="chemin d'un JSON deja produit, pour retracer la figure sans "
                        "relancer la mesure")
    args = p.parse_args()

    os.makedirs(MESURES, exist_ok=True)
    base_figure = os.path.join(SORTIE, "a4-bridage-thermique")

    if args.figure_seule:
        with open(args.figure_seule, encoding="utf-8") as fh:
            d = json.load(fh)
        tracer(d["fenetres"], d["analyse"], base_figure)
        print(f"figure retracee dans {base_figure}.png et .svg")
        return

    print("=" * 88)
    print("a4  bridage thermique sous charge continue")
    print(f"    machine : {_commande(['sysctl', '-n', 'hw.model']).strip()}, "
          f"{os.cpu_count()} coeurs, sans ventilateur")
    print(f"    modele  : {os.path.basename(args.modele)}")
    print(f"    duree   : {args.minutes:g} minutes, fenetres de {args.fenetre:.0f} s")
    print("=" * 88)

    # --- P0. L'etat initial. Sans lui la mesure ne vaut rien, voir a3 section 1.3. ---
    print("\nP0. Etat de la machine avant la mesure")
    etat_initial = releve_etat()
    ok, motifs = machine_au_repos(etat_initial)
    tentative = 0
    while not ok and tentative < args.attente_repos and not args.forcer:
        print(f"  machine non au repos : {' ; '.join(motifs)}")
        print(f"  attente de 30 s, tentative {tentative + 1} sur {args.attente_repos}")
        time.sleep(30)
        etat_initial = releve_etat()
        ok, motifs = machine_au_repos(etat_initial)
        tentative += 1
    print(f"  charge moyenne         : {etat_initial['charge_1_5_15']}")
    print(f"  alimentation           : {etat_initial['pmset_batt'].splitlines()[0]}")
    print(f"  temperature batterie   : {etat_initial['temperature_batterie_c']} degres")
    print(f"  pmset -g therm         : "
          f"{etat_initial['pmset_therm']['brut'].replace(chr(10), ' | ')}")
    print("  processus au dessus de 5 pour cent d'un coeur :")
    for pr in etat_initial["processus_lourds"]:
        print(f"      {pr['cpu']:5.1f}  {pr['commande'][:70]}")
    if not ok and not args.forcer:
        print("\n  ARRET. La machine n'est pas au repos apres attente. La regle est celle "
              "du rapport a3 section 1.3 : une mesure prise pendant qu'un demon travaille "
              "sous estime le debit de 40 pour cent et doit etre jetee.")
        sys.exit(2)
    if not ok:
        print("\n  AVERTISSEMENT. Mesure forcee sur une machine non au repos.")
    print("  verdict : machine au repos, la mesure peut commencer" if ok
          else "  verdict : NON AU REPOS, mesure forcee")

    # --- P1. La charge continue. ---
    persona = fabriquer_persona(args.mots_persona)
    # Un second persona, graine differente, pour le prefill a froid de chaque fenetre.
    # Il doit differer des les premieres lignes pour que le serveur lui donne un autre
    # slot et n'evince pas le cache du persona chaud.
    persona_froid = ("Autre personne, autre biographie.\n"
                     + fabriquer_persona(args.mots_persona, graine=987654321))
    questions = fabriquer_questions(args.questions)

    moteur = MoteurLlama(args.modele, contexte=16384, parallele=args.parallele,
                         port=args.port, cache_kv_8bits=True)
    fenetres, tous, analyse = [], [], {}
    try:
        print("\nP1. Demarrage du serveur, configuration de reference du rapport a3")
        moteur.demarrer()
        n_persona = moteur.compter_tokens(persona)
        n_question = moteur.compter_tokens(questions[0])
        print(f"  serveur pret en {moteur.chargement_s:.1f} s, "
              f"persona {n_persona} tokens, question {n_question} tokens")

        # Chauffe du cache de prefixe. Ces deux appels ne sont pas comptes : le premier
        # paie le prefill du persona, et c'est justement ce que le regime etabli ne paie
        # pas. Les compter melangerait deux regimes dans la premiere fenetre.
        print("  chauffe du cache de prefixe, deux appels non comptes")
        un_appel(moteur, persona + questions[0])
        un_appel(moteur, persona + questions[1])

        print(f"\n  charge continue pendant {args.minutes:g} minutes")
        fenetres, tous = campagne(moteur, persona, persona_froid, questions,
                                  args.minutes, args.fenetre)
        analyse = analyser(fenetres, tous)
    finally:
        moteur.arreter()
        print("\n  serveur arrete")

    etat_final = releve_etat()

    # --- P3. Le verdict. ---
    print("\nP3. Analyse")
    print(f"  premiere minute        : {analyse['premiere_fenetre_appels_h']:.0f} appels/h "
          f"({analyse['premiere_fenetre_latence_ms']:.1f} ms par appel)")
    print(f"  derniere minute        : {analyse['derniere_fenetre_appels_h']:.0f} appels/h "
          f"({analyse['derniere_fenetre_latence_ms']:.1f} ms par appel)")
    print(f"  perte                  : {analyse['perte_pour_cent']:.1f} pour cent")
    pa = analyse["pente_seconde_moitie_appels"]
    if pa:
        print(f"  pente seconde moitie   : {pa['pente']:+.0f} appels/h par minute, "
              f"IC 95 [{pa['ic95_bas']:+.0f} ; {pa['ic95_haut']:+.0f}], "
              f"t = {pa['t']:+.1f}, n = {pa['n']} appels")
    print(f"  verdict                : courbe {analyse['verdict_stabilisation']}")
    print(f"  temperature batterie   : {analyse['temperature_debut_c']} puis "
          f"{analyse['temperature_fin_c']} degres")

    traductions = [traduire_phase1(analyse, 7.05, "Llama-3.1-8B, llama.cpp"),
                   traduire_phase1(analyse, 3.45, "Qwen3-4B, llama.cpp")]
    print("\n  traduction sur les 45 000 appels de la phase 1")
    for t in traductions:
        print(f"      {t['modele']:26s} {hm(t['duree_a3_h'])} mesure a3  "
              f"-> plancher {hm(t['duree_plancher_h'])} "
              f"(facteur {1 / t['facteur_fin']:.3f})")

    # --- Ecriture. ---
    horo = time.strftime("%Y%m%d-%H%M%S")
    chemin = os.path.join(MESURES, f"a4-{horo}.json")
    with open(chemin, "w", encoding="utf-8") as fh:
        json.dump({
            "machine": {
                "modele_materiel": _commande(["sysctl", "-n", "hw.model"]).strip(),
                "puce": _commande(["sysctl", "-n", "machdep.cpu.brand_string"]).strip(),
                "coeurs": os.cpu_count(),
                "macos": _commande(["sw_vers", "-productVersion"]).strip(),
                "refroidissement": "passif, sans ventilateur",
            },
            "configuration": {
                "modele": args.modele, "parallele": args.parallele,
                "contexte_par_slot": 16384, "cache_kv": "q8_0",
                "cache_reuse": 256, "flux_simultanes": 1,
                "minutes": args.minutes, "fenetre_s": args.fenetre,
                "tokens_persona": n_persona, "tokens_question": n_question,
            },
            "etat_initial": etat_initial,
            "etat_final": etat_final,
            "machine_au_repos": ok,
            "fenetres": fenetres,
            "analyse": analyse,
            "traduction_phase1": traductions,
            "appels": [{"t_s": round(a["t_s"], 3), "latence_ms": round(a["latence_ms"], 2)}
                       for a in tous],
        }, fh, ensure_ascii=False, indent=1)
    print(f"\nmesures brutes ecrites dans {chemin}")

    tracer(fenetres, analyse, base_figure)
    print(f"figure ecrite dans {base_figure}.png et {base_figure}.svg")


if __name__ == "__main__":
    main()
