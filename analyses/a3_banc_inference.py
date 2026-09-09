"""
a3 : banc de mesure de l'inference locale sur la machine du projet.

Statut : banc de mesure, pas du code de production. Il existe pour remplacer par des
mesures les trois hypotheses de exploration/06-infrastructure-zero-cout.md dont dependent
toutes les durees annoncees : le debit de prefill (suppose 800 t/s, jamais mesure), le
debit de decodage (suppose 27 t/s), et le gain du cache de prefixe (suppose x8,5).

Ce qu'il mesure, dans l'ordre du rapport :
  T1  la lecture des probabilites du token de reponse fonctionne ou non sur le moteur
  T2  le biais de longueur et de tokenisation entre modalites, et quatre traitements
  T3  le debit de traitement du contexte en entree, en tokens par seconde
  T4  le debit de generation en sortie, en tokens par seconde
  T5  le gain reel du cache de prefixe entre deux questions posees au meme persona
  T6  le gain reel du traitement par lots
  T7  la serie longue : 50 questions sur un persona, stabilite, memoire, derive

Entree  : aucune. Le persona et les questions sont FACTICES et fabriques par le script,
          avec une graine fixe. Aucune donnee d'enquete n'entre ici, et rien ne sort de
          la machine : les deux moteurs tournent en local.
Sortie  : un tableau sur la sortie standard, et un fichier JSON de mesures brutes.

Deux moteurs, au choix :
  --moteur llama : llama.cpp, lance et arrete par le script lui-meme (llama-server)
  --moteur mlx   : mlx-lm d'Apple, charge en memoire dans le processus

Usage :
  python analyses/a3_banc_inference.py --moteur llama \\
      --modele data/modeles/gguf/Qwen3-4B-Instruct-2507-Q4_K_M.gguf
  python analyses/a3_banc_inference.py --moteur mlx \\
      --modele data/modeles/mlx/Qwen3-4B-Instruct-2507-4bit

Duree : de trois a vingt minutes selon la taille du modele.

Avertissement mesure en pratique et a ne pas oublier. Le banc envoie un prompt BRUT, sans
gabarit de conversation. Cela convient a Qwen3 et a Llama 3.1, qui placent alors 89 a 97
pour cent de leur masse de probabilite sur les modalites. Cela ne convient PAS a
gpt-oss-20b, qui n'y place que 3 pour cent tant qu'on ne lui applique pas son gabarit
harmony, et 99,9 pour cent des qu'on le fait. Le chiffre a surveiller est donc toujours la
masse totale avant renormalisation, affichee par T1. En dessous de 0,5, la mesure est
a jeter, pas a interpreter.
"""

import argparse
import json
import math
import os
import random
import socket
import statistics
import subprocess
import sys
import time
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor

# Les cinq modalites d'une question fermee. Des lettres, pas des libelles : voir T2.
MODALITES = ["A", "B", "C", "D", "E"]

# Libelles verbalises, volontairement de longueurs tres inegales. C'est exactement ce
# qui cree le biais que T2 doit rendre visible.
LIBELLES = [
    "oui",
    "non",
    "plutot d'accord",
    "je ne sais pas vraiment quoi en penser",
    "absolument pas, c'est contraire a ce que je crois",
]

GRAINE = 20260903


# --------------------------------------------------------------------------------------
# 1. Le materiel factice
# --------------------------------------------------------------------------------------

def fabriquer_persona(cible_mots=1650, graine=GRAINE):
    """Fabrique un persona factice d'environ 2 000 a 4 000 tokens.

    Contrainte du projet : le prefixe doit etre identique octet par octet d'un appel a
    l'autre, sinon le cache de prefixe echoue silencieusement. D'ou la graine fixe, aucune
    date, aucun identifiant de session, aucun parcours de dictionnaire non ordonne.

    Le contenu est entierement invente. Il n'y a pas une ligne de donnee d'enquete ici.
    """
    rng = random.Random(graine)
    metiers = ["technicienne de maintenance", "libraire", "chauffeur de bus",
               "infirmier de nuit", "comptable", "menuisier", "professeure de college"]
    villes = ["Vierzon", "Lanester", "Oyonnax", "Guise", "Tarare", "Decazeville"]
    gouts = ["la peche au coup", "les mots croises", "la randonnee", "le jardinage",
             "la brocante", "les documentaires animaliers", "le tarot"]
    idees = [
        "Elle pense que les choses etaient plus simples avant, sans vouloir en faire une doctrine.",
        "Il se mefie des grands discours et prefere juger sur ce qu'il voit dans sa rue.",
        "Elle vote sans conviction depuis trois scrutins et le dit sans amertume.",
        "Il trouve que l'ecole demande trop aux familles et pas assez aux institutions.",
        "Elle estime que la solidarite doit passer par la commune plutot que par l'Etat.",
        "Il n'a pas d'avis tranche sur l'Europe et s'en excuse presque quand on l'interroge.",
        "Elle repete que le travail devrait suffire a vivre, et que ce n'est plus le cas.",
        "Il considere que la police fait un metier difficile et critique les bavures.",
        "Elle se dit croyante sans pratiquer, et separe nettement les deux choses.",
        "Il a change d'avis sur l'immigration apres avoir travaille avec un collegue syrien.",
    ]

    lignes = [
        "Tu es une personne reelle. Tu reponds a une enquete d'opinion.",
        "Ce qui suit est ta biographie. Tu ne dois jamais en sortir.",
        "",
    ]
    mots = 0
    i = 0
    while mots < cible_mots:
        bloc = (
            f"Souvenir {i:03d}. "
            f"{rng.choice(idees)} "
            f"A l'epoque tu vivais a {rng.choice(villes)} et tu travaillais comme "
            f"{rng.choice(metiers)}. "
            f"Le soir tu t'occupais surtout avec {rng.choice(gouts)}. "
            f"Tu gagnais environ {rng.randrange(1100, 2600, 50)} euros par mois, "
            f"ce qui te paraissait {rng.choice(['juste', 'insuffisant', 'correct'])} "
            f"pour un foyer de {rng.randint(1, 5)} personnes. "
            f"Tu en parlais peu, sauf a {rng.choice(['ta soeur', 'ton voisin', 'un collegue'])}."
        )
        lignes.append(bloc)
        mots += len(bloc.split())
        i += 1

    lignes += [
        "",
        "Consigne. Pour chaque question, tu reponds par une seule lettre parmi A, B, C, D, E.",
        "Tu ne justifies jamais. Tu ne rajoutes aucun mot.",
    ]
    return "\n".join(lignes)


def fabriquer_questions(n=50, graine=GRAINE + 1):
    """Fabrique n questions fermees factices a cinq modalites."""
    rng = random.Random(graine)
    themes = ["les impots locaux", "le service public de sante", "le tri des dechets",
              "la vitesse sur les routes", "l'aide au logement", "les eoliennes",
              "le temps de travail", "les commerces du centre-ville", "l'ecole publique",
              "les transports en commun", "la securite du quartier", "le prix de l'essence"]
    tournures = ["Que penses-tu de {} ?", "Es-tu satisfait de {} ?",
                 "Faut-il en faire davantage pour {} ?", "As-tu confiance dans {} ?"]
    questions = []
    for k in range(n):
        theme = themes[k % len(themes)]
        tournure = tournures[rng.randrange(len(tournures))]
        corps = tournure.format(theme)
        options = "\n".join(f"{MODALITES[j]}. {LIBELLES[j]}" for j in range(len(MODALITES)))
        questions.append(f"\nQuestion {k + 1:02d}. {corps}\n{options}\nReponse :")
    return questions


# --------------------------------------------------------------------------------------
# 2. Moteur llama.cpp, pilote par le script
# --------------------------------------------------------------------------------------

class MoteurLlama:
    """Lance llama-server, l'interroge en HTTP, l'arrete. Rien ne sort de la machine."""

    nom = "llama.cpp"

    def __init__(self, modele, contexte=16384, parallele=1, port=8099, cache_kv_8bits=True):
        self.modele = modele
        self.contexte = contexte
        self.parallele = parallele
        self.port = port
        self.base = f"http://127.0.0.1:{port}"
        self.cache_kv_8bits = cache_kv_8bits
        self.proc = None

    def demarrer(self):
        # llama-server refuse de demarrer si ce dossier n'existe pas deja.
        os.makedirs("/tmp/a3-slots", exist_ok=True)
        cmd = [
            "llama-server", "-m", self.modele,
            "--host", "127.0.0.1", "--port", str(self.port),
            # Le contexte est partage entre les slots : il faut le multiplier par le
            # nombre de slots paralleles, sinon chaque slot n'a que c/np tokens.
            "-c", str(self.contexte * self.parallele),
            "-np", str(self.parallele),
            "-ngl", "999",              # tout sur le GPU Metal
            "--cache-reuse", "256",     # decale le cache au lieu de recalculer
            "--no-webui",
            "-fa", "on",                # attention fusionnee, requise pour le cache KV quantifie
            # Sans --slot-save-path le serveur repond 501 a l'action erase, et le banc
            # croit mesurer un prefill a froid alors que le cache est encore chaud.
            "--slot-save-path", "/tmp/a3-slots",
        ]
        if self.cache_kv_8bits:
            cmd += ["--cache-type-k", "q8_0", "--cache-type-v", "q8_0"]
        self.journal = open(f"/tmp/a3-llama-server-{self.port}.log", "w")
        self.proc = subprocess.Popen(cmd, stdout=self.journal, stderr=subprocess.STDOUT)
        # Attente active de la disponibilite, plafonnee.
        debut = time.time()
        while time.time() - debut < 300:
            try:
                with urllib.request.urlopen(self.base + "/health", timeout=2) as r:
                    if r.status == 200:
                        self.chargement_s = time.time() - debut
                        return
            except Exception:
                if self.proc.poll() is not None:
                    raise RuntimeError(
                        f"llama-server s'est arrete. Journal : /tmp/a3-llama-server-{self.port}.log")
                time.sleep(0.5)
        raise RuntimeError("llama-server n'a pas repondu en 300 s")

    def arreter(self):
        if self.proc:
            self.proc.terminate()
            try:
                self.proc.wait(timeout=20)
            except subprocess.TimeoutExpired:
                self.proc.kill()
            self.journal.close()

    def _poster(self, route, charge, timeout=1800):
        req = urllib.request.Request(
            self.base + route, data=json.dumps(charge).encode("utf-8"),
            headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return json.loads(r.read())

    def compter_tokens(self, texte):
        return len(self._poster("/tokenize", {"content": texte})["tokens"])

    def memoire_rss_mo(self):
        if not self.proc:
            return None
        sortie = subprocess.run(["ps", "-o", "rss=", "-p", str(self.proc.pid)],
                                capture_output=True, text=True).stdout.strip()
        return int(sortie) / 1024 if sortie else None

    def vider_cache(self):
        """Force le prochain appel a recalculer tout le prefixe.

        Il faut vider TOUS les slots : avec -np 8 le serveur choisit le slot dont le
        prefixe commun est le plus long, donc n'en vider qu'un ne sert a rien. Erreur
        commise a la premiere version de ce script, elle donnait un prefill a froid de
        36 ms au lieu de 8 s.
        """
        for slot in range(self.parallele):
            try:
                self._poster(f"/slots/{slot}?action=erase", {})
            except Exception:
                pass

    def passe_avant(self, prompt, n_probs=40, cache=True):
        """Un seul passage avant. Renvoie les probabilites du token suivant et les temps.

        C'est la primitive centrale du protocole popsim : on ne genere pas, on lit.
        """
        r = self._poster("/completion", {
            "prompt": prompt,
            "n_predict": 1,
            "n_probs": n_probs,
            "temperature": 0.0,
            "cache_prompt": cache,
            "post_sampling_probs": False,
        })
        t = r.get("timings", {})
        proba = {}
        cps = r.get("completion_probabilities") or []
        if cps:
            for e in cps[0].get("top_logprobs", []):
                proba[e["token"]] = math.exp(e["logprob"])
        return {
            "probabilites": proba,
            "tokens_prompt_evalues": t.get("prompt_n"),
            "prompt_ms": t.get("prompt_ms"),
            "prompt_par_seconde": t.get("prompt_per_second"),
            "tokens_prompt_total": r.get("tokens_evaluated"),
        }

    def generer(self, prompt, n_predict=128, cache=True):
        r = self._poster("/completion", {
            "prompt": prompt, "n_predict": n_predict, "temperature": 0.0,
            "cache_prompt": cache})
        t = r.get("timings", {})
        return {
            "texte": r.get("content", ""),
            "tokens_generes": t.get("predicted_n"),
            "generation_ms": t.get("predicted_ms"),
            "generation_par_seconde": t.get("predicted_per_second"),
            "prompt_par_seconde": t.get("prompt_per_second"),
            "tokens_prompt_evalues": t.get("prompt_n"),
        }


# --------------------------------------------------------------------------------------
# 3. Moteur mlx-lm
# --------------------------------------------------------------------------------------

class MoteurMlx:
    """Charge le modele dans le processus. Acces direct aux logits, donc exact."""

    nom = "mlx-lm"

    def __init__(self, modele, contexte=16384, parallele=1, **_):
        self.modele = modele
        self.contexte = contexte
        self.parallele = parallele

    def demarrer(self):
        import mlx.core as mx
        from mlx_lm import load
        self.mx = mx
        debut = time.time()
        self.m, self.tok = load(self.modele)
        self.chargement_s = time.time() - debut

    def arreter(self):
        pass

    def compter_tokens(self, texte):
        return len(self.tok.encode(texte))

    def memoire_rss_mo(self):
        for nom in ("get_peak_memory", "get_active_memory"):
            f = getattr(self.mx, nom, None)
            if f:
                return f() / 1e6
        return None

    def _cache_neuf(self):
        from mlx_lm.models.cache import make_prompt_cache
        return make_prompt_cache(self.m)

    def _prefill(self, ids, cache, pas=512):
        """Traite le prompt par tranches, comme le fait mlx_lm en interne."""
        mx = self.mx
        logits = None
        for i in range(0, len(ids), pas):
            bloc = mx.array(ids[i:i + pas])[None]
            logits = self.m(bloc, cache=cache)
            mx.eval(logits)
        return logits

    def revenir_au_persona(self, cache, n_tokens):
        """Retranche du cache les n derniers tokens, pour reprendre au meme prefixe.

        Piege documente : les modeles a fenetre glissante ou a couches SSM ne supportent
        pas cette operation. `can_trim_prompt_cache` le dit, et le banc s'arrete plutot
        que de mesurer un cache silencieusement inoperant.
        """
        from mlx_lm.models.cache import trim_prompt_cache, can_trim_prompt_cache
        if not can_trim_prompt_cache(cache):
            raise RuntimeError(
                "ce modele ne permet pas de rembobiner le cache de prefixe sous mlx-lm "
                "(fenetre glissante ou couches SSM) : le cache de prefixe y est inoperant")
        retire = trim_prompt_cache(cache, n_tokens)
        if retire != n_tokens:
            raise RuntimeError(f"rembobinage incomplet : {retire} sur {n_tokens}")

    def passe_avant(self, prompt, cache=None, n_probs=40):
        """Un passage avant. Renvoie la distribution complete du token suivant."""
        mx = self.mx
        ids = self.tok.encode(prompt)
        cache = cache if cache is not None else self._cache_neuf()
        t0 = time.perf_counter()
        logits = self._prefill(ids, cache)
        dt = time.perf_counter() - t0
        derniers = logits[0, -1].astype(mx.float32)
        lp = derniers - mx.logsumexp(derniers)
        mx.eval(lp)
        return {
            "logprobs": lp,
            "cache": cache,
            "tokens_prompt_evalues": len(ids),
            "prompt_ms": dt * 1000,
            "prompt_par_seconde": len(ids) / dt if dt > 0 else None,
        }

    def logprob_du_token(self, lp, token_id):
        return float(lp[token_id].item())

    def id_de_suite(self, prompt, suite):
        """Identifiant du premier token de `suite` quand elle suit `prompt`.

        Passe obligee : la tokenisation depend du contexte gauche. Encoder la suite
        isolement donne souvent un autre token que celui reellement attendu.
        """
        a = self.tok.encode(prompt)
        b = self.tok.encode(prompt + suite)
        if len(b) <= len(a) or b[:len(a)] != a:
            return None, None
        return b[len(a)], b[len(a):]

    def score_sequence(self, prompt, suite):
        """Somme des log-probabilites des tokens de `suite`, et leur nombre.

        Sert a T2. Un seul passage avant sur prompt+suite suffit : les logits de la
        position t predisent le token t+1.
        """
        mx = self.mx
        ids_p = self.tok.encode(prompt)
        ids_c = self.tok.encode(prompt + suite)
        cible = ids_c[len(ids_p):]
        if not cible:
            return None, 0
        logits = self._prefill(ids_c[:-1], self._cache_neuf())
        # Les positions utiles sont les len(cible) dernieres.
        util = logits[0, -len(cible):].astype(mx.float32)
        lp = util - mx.logsumexp(util, axis=-1, keepdims=True)
        total = sum(float(lp[i, t].item()) for i, t in enumerate(cible))
        return total, len(cible)

    def generer(self, prompt, n_predict=128, cache=None):
        """Decodage glouton, chronometre en separant prefill et generation."""
        mx = self.mx
        ids = self.tok.encode(prompt)
        cache = cache if cache is not None else self._cache_neuf()
        t0 = time.perf_counter()
        logits = self._prefill(ids, cache)
        t1 = time.perf_counter()
        jeton = mx.argmax(logits[0, -1]).item()
        produits = [jeton]
        for _ in range(n_predict - 1):
            logits = self.m(mx.array([[jeton]]), cache=cache)
            mx.eval(logits)
            jeton = mx.argmax(logits[0, -1]).item()
            produits.append(jeton)
        t2 = time.perf_counter()
        return {
            "texte": self.tok.decode(produits),
            "tokens_generes": len(produits),
            "generation_ms": (t2 - t1) * 1000,
            "generation_par_seconde": len(produits) / (t2 - t1),
            "prompt_par_seconde": len(ids) / (t1 - t0),
            "tokens_prompt_evalues": len(ids),
        }


# --------------------------------------------------------------------------------------
# 4. Les mesures
# --------------------------------------------------------------------------------------

def normaliser(brut):
    s = sum(brut.values())
    return {k: v / s for k, v in brut.items()} if s > 0 else brut


def t1_probabilites(moteur, prompt):
    """T1. Peut-on lire la probabilite de chaque modalite ? Sinon, moteur elimine."""
    print("\n--- T1. Lecture des probabilites du token de reponse ---")
    if isinstance(moteur, MoteurLlama):
        r = moteur.passe_avant(prompt, n_probs=40)
        brut = {}
        for lettre in MODALITES:
            trouve = [v for k, v in r["probabilites"].items() if k.strip() == lettre]
            brut[lettre] = max(trouve) if trouve else 0.0
        manquantes = [k for k, v in brut.items() if v == 0.0]
        methode = "top-k renvoye par llama-server (n_probs=40)"
    else:
        r = moteur.passe_avant(prompt)
        brut = {}
        manquantes = []
        for lettre in MODALITES:
            tid, _ = moteur.id_de_suite(prompt, " " + lettre)
            if tid is None:
                manquantes.append(lettre)
                brut[lettre] = 0.0
            else:
                brut[lettre] = math.exp(moteur.logprob_du_token(r["logprobs"], tid))
        methode = "distribution complete sur le vocabulaire (exacte)"

    norm = normaliser(brut)
    print(f"  methode : {methode}")
    print(f"  masse totale sur les cinq modalites avant renormalisation : {sum(brut.values()):.4f}")
    for lettre in MODALITES:
        print(f"    p({lettre}) = {brut[lettre]:.6f}   renormalisee {norm[lettre]:.4f}"
              f"   [{LIBELLES[MODALITES.index(lettre)]}]")
    if manquantes:
        print(f"  ATTENTION : modalites absentes du resultat : {manquantes}")
    # Entropie de la distribution renormalisee : c'est la mesure que le projet etudie.
    h = -sum(p * math.log2(p) for p in norm.values() if p > 0)
    print(f"  entropie de la reponse : {h:.4f} bits sur un maximum de "
          f"{math.log2(len(MODALITES)):.4f}")
    return {"brut": brut, "normalisee": norm, "manquantes": manquantes,
            "masse_totale": sum(brut.values()), "entropie_bits": h, "methode": methode}


def t2_biais_de_longueur(moteur, prompt):
    """T2. Le piege : les modalites n'ont ni la meme longueur ni la meme tokenisation.

    Comparer directement p("oui") et p("absolument pas, c'est contraire a ce que je
    crois") n'a aucun sens : la seconde est un produit de vingt probabilites, donc
    mecaniquement plus petite, quel que soit l'avis du persona. Le classement obtenu
    mesure la longueur, pas l'opinion.

    Quatre traitements sont mesures ici et compares :
      (a) etiquette courte  : on ne score qu'une lettre, un token, meme position pour
                              toutes les modalites. Le biais disparait par construction.
                              C'est le traitement retenu pour popsim.
      (b) somme brute       : somme des log-probabilites du libelle. Sert de temoin
                              negatif : c'est la facon naive et fausse.
      (c) normalisation par la longueur : moyenne des log-probabilites par token.
                              Corrige l'essentiel du biais, mais surpondere les libelles
                              longs dont chaque token est previsible.
      (d) PMI conditionnel  : log p(libelle | persona + question) moins
                              log p(libelle | question seule). Retire la frequence propre
                              du libelle dans la langue. C'est la correction de Holtzman
                              et al. 2021 sur la competition de forme de surface.
    """
    print("\n--- T2. Biais de longueur et de tokenisation entre modalites ---")
    if isinstance(moteur, MoteurLlama):
        print("  Le scoring multi-token n'est pas fait ici pour llama.cpp : l'API du serveur")
        print("  n'expose les probabilites qu'aux positions generees, pas aux positions du")
        print("  prompt. Le traitement (a), le seul retenu pour popsim, fonctionne lui")
        print("  parfaitement, cf. T1. Voir le rapport pour la discussion.")
        return {"applicable": False}

    # Contexte neutre pour le PMI : la question sans le persona.
    debut_question = prompt.rfind("\nQuestion ")
    prompt_neutre = prompt[debut_question:] if debut_question > 0 else prompt

    r = moteur.passe_avant(prompt)
    lignes = []
    for i, libelle in enumerate(LIBELLES):
        lettre = MODALITES[i]
        tid, _ = moteur.id_de_suite(prompt, " " + lettre)
        lp_lettre = moteur.logprob_du_token(r["logprobs"], tid) if tid is not None else None
        brut, n = moteur.score_sequence(prompt, " " + libelle)
        neutre, _ = moteur.score_sequence(prompt_neutre, " " + libelle)
        lignes.append({
            "modalite": lettre, "libelle": libelle, "n_tokens": n,
            "a_etiquette": lp_lettre,
            "b_somme_brute": brut,
            "c_par_token": brut / n if n else None,
            "d_pmi": (brut - neutre) if neutre is not None else None,
        })

    print(f"  {'mod':<4}{'ntok':>5}{'(a) etiquette':>15}{'(b) somme':>12}"
          f"{'(c) /token':>12}{'(d) PMI':>10}  libelle")
    for l in lignes:
        print(f"  {l['modalite']:<4}{l['n_tokens']:>5}{l['a_etiquette']:>15.4f}"
              f"{l['b_somme_brute']:>12.3f}{l['c_par_token']:>12.4f}"
              f"{l['d_pmi']:>10.3f}  {l['libelle'][:38]}")

    classements = {}
    for cle in ("a_etiquette", "b_somme_brute", "c_par_token", "d_pmi"):
        ordre = sorted(lignes, key=lambda l: -(l[cle] if l[cle] is not None else -1e9))
        classements[cle] = [l["modalite"] for l in ordre]
        print(f"  classement {cle:<14} : {' > '.join(classements[cle])}")

    accord = classements["a_etiquette"][0] == classements["b_somme_brute"][0]
    print(f"  la modalite gagnante est-elle la meme en (a) et en (b) ? "
          f"{'oui' if accord else 'NON, le biais de longueur change la reponse'}")
    correl = _tau(classements["a_etiquette"], classements["b_somme_brute"])
    print(f"  correlation de rang entre (a) et (b) : tau = {correl:+.2f}")
    return {"applicable": True, "lignes": lignes, "classements": classements,
            "meme_gagnante_a_b": accord, "tau_a_b": correl}


def _tau(r1, r2):
    """Tau de Kendall entre deux classements donnes comme des listes ordonnees."""
    pos1 = {v: i for i, v in enumerate(r1)}
    pos2 = {v: i for i, v in enumerate(r2)}
    cles = list(pos1)
    c = d = 0
    for i in range(len(cles)):
        for j in range(i + 1, len(cles)):
            a, b = cles[i], cles[j]
            s = (pos1[a] - pos1[b]) * (pos2[a] - pos2[b])
            c += s > 0
            d += s < 0
    return (c - d) / (c + d) if (c + d) else 0.0


def t3_t4_debits(moteur, persona, question):
    """T3 et T4. Debit de prefill et debit de decodage, cache vide."""
    print("\n--- T3 et T4. Debit de traitement du contexte et debit de generation ---")
    moteur.vider_cache() if hasattr(moteur, "vider_cache") else None
    prompt = persona + question
    n = moteur.compter_tokens(prompt)
    if isinstance(moteur, MoteurLlama):
        r = moteur.generer(prompt, n_predict=128, cache=False)
    else:
        r = moteur.generer(prompt, n_predict=128)
    print(f"  longueur du prompt : {n} tokens")
    print(f"  prefill  : {r['tokens_prompt_evalues']} tokens, "
          f"{r['prompt_par_seconde']:.1f} tokens/s")
    print(f"  decodage : {r['tokens_generes']} tokens, "
          f"{r['generation_par_seconde']:.1f} tokens/s")
    return {"tokens_prompt": n,
            "prefill_t_par_s": r["prompt_par_seconde"],
            "decodage_t_par_s": r["generation_par_seconde"]}


def t5_cache_de_prefixe(moteur, persona, questions, n=6):
    """T5. Le levier annonce comme decisif : le prefixe du persona n'est calcule qu'une fois.

    Protocole : on mesure d'abord un appel cache vide (le persona est traite en entier),
    puis n appels sur le meme persona avec des questions differentes. Le gain est le
    rapport des durees. Le meme essai est refait cache desactive, pour verifier que la
    difference vient bien du cache et non d'un echauffement.
    """
    print("\n--- T5. Gain reel du cache de prefixe entre deux questions ---")
    n_persona = moteur.compter_tokens(persona)

    if isinstance(moteur, MoteurLlama):
        moteur.vider_cache()
        froid = moteur.passe_avant(persona + questions[0], cache=True)
        t_froid = froid["prompt_ms"]
        chauds = []
        for q in questions[1:1 + n]:
            r = moteur.passe_avant(persona + q, cache=True)
            chauds.append((r["prompt_ms"], r["tokens_prompt_evalues"]))
        moteur.vider_cache()
        sans = []
        for q in questions[1:1 + n]:
            r = moteur.passe_avant(persona + q, cache=False)
            sans.append(r["prompt_ms"])
            moteur.vider_cache()
        med_chaud = statistics.median(m for m, _ in chauds)
        tokens_reevalues = statistics.median(t for _, t in chauds)
        med_sans = statistics.median(sans)
    else:
        # Cache froid : on traite le persona en entier une fois.
        cache = moteur._cache_neuf()
        ids_persona = moteur.tok.encode(persona)
        t0 = time.perf_counter()
        moteur._prefill(ids_persona, cache)
        t_froid = (time.perf_counter() - t0) * 1000
        # Appels chauds. La bonne primitive est trim_prompt_cache, qui retranche du cache
        # les tokens de la question precedente sans rien recalculer et sans passer par le
        # disque. La sauvegarde et le rechargement d'un cache de 3 000 tokens coutent
        # plusieurs centaines de mega-octets d'entrees-sorties par question, ce qui
        # mesurerait le disque et non le modele.
        chauds = []
        for q in questions[1:1 + n]:
            ids_q = moteur.tok.encode(persona + q)[len(ids_persona):]
            t0 = time.perf_counter()
            moteur._prefill(ids_q, cache)
            chauds.append(((time.perf_counter() - t0) * 1000, len(ids_q)))
            moteur.revenir_au_persona(cache, len(ids_q))
        sans = []
        for q in questions[1:1 + n]:
            r = moteur.passe_avant(persona + q)
            sans.append(r["prompt_ms"])
        med_chaud = statistics.median(m for m, _ in chauds)
        tokens_reevalues = statistics.median(t for _, t in chauds)
        med_sans = statistics.median(sans)

    gain = med_sans / med_chaud if med_chaud else None
    print(f"  persona : {n_persona} tokens")
    print(f"  premier appel, cache vide            : {t_froid:.0f} ms")
    print(f"  appels suivants, cache actif         : {med_chaud:.0f} ms "
          f"(mediane, {tokens_reevalues:.0f} tokens reevalues)")
    print(f"  memes appels, cache desactive        : {med_sans:.0f} ms (mediane)")
    print(f"  GAIN MESURE DU CACHE DE PREFIXE      : x{gain:.1f}" if gain else "")
    return {"tokens_persona": n_persona, "froid_ms": t_froid,
            "chaud_ms": med_chaud, "sans_cache_ms": med_sans,
            "tokens_reevalues": tokens_reevalues, "gain": gain}


def t6_lots(moteur, persona, questions, tailles=(1, 2, 4)):
    """T6. Traitement par lots, sous la seule forme qui ait un sens en production.

    Premiere version de ce test, fausse, et l'erreur merite d'etre gardee en memoire :
    envoyer P requetes simultanees portant le MEME persona. Le serveur les repartit sur
    P slots, chacun doit alors traiter le persona entier, et les slots s'evincent
    mutuellement au tour suivant. Mesure obtenue : un gain de 0,06, c'est a dire seize
    fois plus lent. Ce n'etait pas une mesure du lot, c'etait une mesure de la contention.

    La forme productive est l'inverse exact : P personas differents, un par slot, chacun
    deroulant ses questions en serie. Chaque slot conserve alors son propre prefixe, et
    l'ordonnanceur de llama.cpp peut reellement fusionner les P deltas de question dans
    un meme lot physique. C'est aussi la forme de l'experience de phase 1 : 150 personas
    par 50 questions.
    """
    print("\n--- T6. Gain reel du traitement par lots ---")
    if not isinstance(moteur, MoteurLlama):
        print("  non applicable : mlx-lm n'a pas d'ordonnanceur de requetes concurrentes.")
        print("  Le banc ne simule pas ce que le moteur n'a pas.")
        return {"applicable": False}

    personas = [fabriquer_persona(graine=GRAINE + i) for i in range(max(tailles))]
    n_q = 8

    def travail(i, combien):
        for q in questions[1:1 + combien]:
            moteur.passe_avant(personas[i] + q, n_probs=40, cache=True)

    resultats = {}
    reference = None
    for taille in tailles:
        if taille > moteur.parallele:
            print(f"  lot de {taille} ignore : le serveur n'a que {moteur.parallele} slots")
            continue
        # Prechauffage : une question par persona, pour installer chaque prefixe dans son
        # slot. Sans cela on mesure P prefills complets et non le regime etabli.
        with ThreadPoolExecutor(max_workers=taille) as ex:
            list(ex.map(lambda i: travail(i, 1), range(taille)))
        t0 = time.perf_counter()
        with ThreadPoolExecutor(max_workers=taille) as ex:
            list(ex.map(lambda i: travail(i, n_q), range(taille)))
        dt = time.perf_counter() - t0
        n = taille * n_q
        debit = n / dt
        if reference is None:
            reference = debit
        resultats[taille] = {"duree_s": dt, "appels": n, "appels_par_s": debit,
                             "appels_par_heure": debit * 3600, "gain": debit / reference}
        print(f"  {taille:>2} persona(s) en parallele : {dt:6.2f} s pour {n:>3} appels, "
              f"{debit:5.2f} appels/s, {debit * 3600:8.0f} appels/h, gain x{debit / reference:.2f}")
    meilleur = max(v["gain"] for v in resultats.values()) if resultats else 1.0
    print(f"  GAIN MESURE DU LOT : x{meilleur:.2f}")
    return {"applicable": True, "resultats": resultats, "gain_max": meilleur}


def t7_serie_longue(moteur, persona, questions):
    """T7. Le cas d'usage reel : un persona, cinquante questions fermees, a la suite.

    C'est cette mesure, et elle seule, qui donne le nombre d'appels par heure.
    """
    print(f"\n--- T7. Serie longue : 1 persona, {len(questions)} questions fermees ---")
    if hasattr(moteur, "vider_cache"):
        moteur.vider_cache()

    durees = []
    memoire = []
    entropies = []
    t_debut = time.perf_counter()

    if isinstance(moteur, MoteurLlama):
        for i, q in enumerate(questions):
            t0 = time.perf_counter()
            r = moteur.passe_avant(persona + q, n_probs=40, cache=True)
            durees.append(time.perf_counter() - t0)
            brut = {}
            for lettre in MODALITES:
                trouve = [v for k, v in r["probabilites"].items() if k.strip() == lettre]
                brut[lettre] = max(trouve) if trouve else 0.0
            norm = normaliser(brut)
            entropies.append(-sum(p * math.log2(p) for p in norm.values() if p > 0))
            if i % 10 == 0:
                memoire.append(moteur.memoire_rss_mo())
    else:
        cache = moteur._cache_neuf()
        ids_persona = moteur.tok.encode(persona)
        moteur._prefill(ids_persona, cache)
        ids_lettres = [moteur.id_de_suite(persona + questions[0], " " + l)[0]
                       for l in MODALITES]
        for i, q in enumerate(questions):
            t0 = time.perf_counter()
            ids_q = moteur.tok.encode(persona + q)[len(ids_persona):]
            logits = moteur._prefill(ids_q, cache)
            derniers = logits[0, -1].astype(moteur.mx.float32)
            lp = derniers - moteur.mx.logsumexp(derniers)
            moteur.mx.eval(lp)
            brut = {MODALITES[j]: math.exp(float(lp[t].item())) if t is not None else 0.0
                    for j, t in enumerate(ids_lettres)}
            durees.append(time.perf_counter() - t0)
            # On rembobine le cache jusqu'au persona pour la question suivante.
            moteur.revenir_au_persona(cache, len(ids_q))
            norm = normaliser(brut)
            entropies.append(-sum(p * math.log2(p) for p in norm.values() if p > 0))
            if i % 10 == 0:
                memoire.append(moteur.memoire_rss_mo())

    total = time.perf_counter() - t_debut
    premiere = durees[0]
    reste = durees[1:]
    print(f"  duree totale                    : {total:.2f} s")
    print(f"  premier appel (prefixe a froid) : {premiere * 1000:.0f} ms")
    print(f"  appels suivants                 : mediane {statistics.median(reste) * 1000:.0f} ms, "
          f"min {min(reste) * 1000:.0f}, max {max(reste) * 1000:.0f}")
    if len(reste) >= 20:
        d1 = statistics.median(reste[:len(reste) // 2])
        d2 = statistics.median(reste[len(reste) // 2:])
        print(f"  derive sur la serie             : premiere moitie {d1 * 1000:.0f} ms, "
              f"seconde moitie {d2 * 1000:.0f} ms, soit {(d2 / d1 - 1) * 100:+.1f} %")
    mem = [m for m in memoire if m]
    if mem:
        print(f"  memoire                         : {mem[0]:.0f} Mo au depart, "
              f"{mem[-1]:.0f} Mo a la fin")
    print(f"  entropie moyenne des reponses   : {statistics.mean(entropies):.4f} bits")
    debit_horaire = 3600 / statistics.median(reste)
    print(f"  APPELS PAR HEURE, REGIME ETABLI : {debit_horaire:,.0f}".replace(",", " "))
    return {"duree_totale_s": total, "premier_appel_ms": premiere * 1000,
            "mediane_ms": statistics.median(reste) * 1000,
            "min_ms": min(reste) * 1000, "max_ms": max(reste) * 1000,
            "memoire_debut_mo": mem[0] if mem else None,
            "memoire_fin_mo": mem[-1] if mem else None,
            "entropie_moyenne_bits": statistics.mean(entropies),
            "appels_par_heure": debit_horaire}


# --------------------------------------------------------------------------------------
# 5. Assemblage
# --------------------------------------------------------------------------------------

def main():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--moteur", choices=["llama", "mlx"], required=True)
    p.add_argument("--modele", required=True, help="chemin du .gguf ou du dossier MLX")
    p.add_argument("--questions", type=int, default=50)
    p.add_argument("--mots-persona", type=int, default=1650,
                   help="1650 mots donnent environ 3 000 tokens, cible du projet")
    p.add_argument("--contexte", type=int, default=16384)
    p.add_argument("--parallele", type=int, default=8, help="slots de llama-server")
    p.add_argument("--port", type=int, default=8099)
    p.add_argument("--sortie", default=None, help="fichier JSON des mesures brutes")
    p.add_argument("--sauter", default="", help="tests a sauter, ex : t2,t6")
    p.add_argument("--cache-kv-f16", action="store_true",
                   help="desactive la quantification 8 bits du cache KV, pour mesurer "
                        "ce qu'elle coute en debit et ce qu'elle economise en memoire")
    args = p.parse_args()

    sauter = {s.strip() for s in args.sauter.split(",") if s.strip()}

    persona = fabriquer_persona(args.mots_persona)
    questions = fabriquer_questions(args.questions)

    Classe = MoteurLlama if args.moteur == "llama" else MoteurMlx
    moteur = Classe(args.modele, contexte=args.contexte, parallele=args.parallele,
                    port=args.port, cache_kv_8bits=not args.cache_kv_f16)

    print("=" * 78)
    print(f"a3 banc d'inference   moteur {moteur.nom}   modele {os.path.basename(args.modele)}")
    print("=" * 78)
    t0 = time.time()
    moteur.demarrer()
    print(f"  modele charge en {moteur.chargement_s:.1f} s")

    mesures = {"moteur": moteur.nom, "modele": args.modele,
               "chargement_s": moteur.chargement_s,
               "cache_kv": "f16" if args.cache_kv_f16 else "q8_0",
               "slots_paralleles": args.parallele,
               "contexte_par_slot": args.contexte}
    try:
        n_persona = moteur.compter_tokens(persona)
        print(f"  persona factice : {n_persona} tokens, {args.questions} questions")
        mesures["tokens_persona"] = n_persona

        prompt1 = persona + questions[0]
        if "t1" not in sauter:
            mesures["t1"] = t1_probabilites(moteur, prompt1)
        if "t2" not in sauter:
            mesures["t2"] = t2_biais_de_longueur(moteur, prompt1)
        if "t3" not in sauter:
            mesures["t3_t4"] = t3_t4_debits(moteur, persona, questions[0])
        if "t5" not in sauter:
            mesures["t5"] = t5_cache_de_prefixe(moteur, persona, questions)
        if "t6" not in sauter:
            mesures["t6"] = t6_lots(moteur, persona, questions)
        if "t7" not in sauter:
            mesures["t7"] = t7_serie_longue(moteur, persona, questions)
    finally:
        moteur.arreter()

    mesures["duree_du_banc_s"] = time.time() - t0

    # Le chiffre que le projet attend. Attention au piege : le regime etabli de T7 ne
    # compte pas le calcul des prefixes de persona, qui n'est pas gratuit. La phase 1
    # compte 150 personas par 6 conditions, soit 900 prefixes distincts a calculer une
    # fois chacun, plus 45 000 appels en regime etabli.
    N_APPELS, N_PREFIXES = 45000, 150 * 6
    if "t7" in mesures and "t3_t4" in mesures:
        par_heure = mesures["t7"]["appels_par_heure"]
        ms = mesures["t7"]["mediane_ms"] / 1000
        prefill = mesures["t3_t4"]["prefill_t_par_s"]
        cout_prefixe = mesures["tokens_persona"] / prefill
        gain_lot = mesures.get("t6", {}).get("gain_max") or 1.0
        total = N_PREFIXES * cout_prefixe + N_APPELS * ms
        total_lot = N_PREFIXES * cout_prefixe + N_APPELS * ms / gain_lot
        print("\n" + "=" * 78)
        print(f"  appels/h en regime etabli, prefixe deja en cache : {par_heure:,.0f}"
              .replace(",", " "))
        print(f"  cout d'un prefixe de persona a froid             : {cout_prefixe:.2f} s")
        print(f"  phase 1, {N_PREFIXES} prefixes plus {N_APPELS} appels          : "
              f"{total / 3600:.2f} h, soit {N_APPELS / (total / 3600):,.0f} appels/h reels"
              .replace(",", " "))
        if gain_lot > 1.01:
            print(f"  la meme, avec le gain de lot mesure x{gain_lot:.2f}        : "
                  f"{total_lot / 3600:.2f} h")
        print("=" * 78)
        mesures["appels_par_heure_regime_etabli"] = par_heure
        mesures["cout_prefixe_s"] = cout_prefixe
        mesures["heures_pour_45000_appels"] = total / 3600
        mesures["heures_pour_45000_appels_avec_lots"] = total_lot / 3600
        mesures["appels_par_heure_reels"] = N_APPELS / (total / 3600)

    if args.sortie:
        with open(args.sortie, "w", encoding="utf-8") as fh:
            json.dump(mesures, fh, indent=2, ensure_ascii=False, default=str)
        print(f"\nmesures brutes ecrites dans {args.sortie}")


if __name__ == "__main__":
    main()
