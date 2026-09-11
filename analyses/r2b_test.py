"""Tests locaux R2b : aucun serveur, aucun appel reseau, aucune trace source modifiee."""
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
import threading
import sys
import r2b_evaluer as E
import r2b_extension as X
import pandas as pd


class Validation(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.path = Path(self.temp.name) / 'source.jsonl'
        self.people = pd.DataFrame([{'pid': 'synthetic', 'index': 0, 'pli': 0}])
        self.table = {i: {'options': ['a', 'b']} for i in ['x', 'y']}
        self.rows = [dict(pid='synthetic', item=i, pli=0, condition='C3F', passe=1,
                          distribution={'a': .6, 'b': .4}, argmax='a', **E.REGISTRE)
                     for i in ['x', 'y']]

    def validate(self, rows):
        self.path.write_text(''.join(json.dumps(r) + '\n' for r in rows))
        return E.valider_trace(self.path, self.people, self.table, self.table,
                               registre=E.REGISTRE)

    def test_exact_complete(self):
        self.assertEqual(self.validate(self.rows), 2)

    def test_duplicate_cannot_replace_missing_item(self):
        with self.assertRaises(ValueError): self.validate([self.rows[0]] * 2)

    def test_partial_refused(self):
        with self.assertRaises(ValueError): self.validate(self.rows[:1])

    def test_invalid_values_or_metadata(self):
        changes = [{'condition':'C3'}, {'passe':2}, {'pli':1}, {'variante_fin':'brut'},
                   {'distribution':{'a':float('nan'),'b':0}},
                   {'distribution':{'a':.3,'b':.4}}, {'argmax':'b'}, {'rejet':True},
                   {'distribution':{'a':1}}, {'item':'unknown'}]
        for change in changes:
            with self.subTest(change=change), self.assertRaises(ValueError):
                self.validate([{**self.rows[0], **change}, self.rows[1]])

    def test_malformed_json_refused(self):
        self.path.write_text('{')
        with self.assertRaises(ValueError):
            E.valider_trace(self.path, self.people, self.table, self.table)


class GardeMemoire(unittest.TestCase):
    def test_memory_and_unreadable_stop(self):
        for swap, free, base, expected in [(5000,73,{'swap':None},False),
                (17776,34,12791,True), (5000,14,5000,True),
                (25000,73,25000,True), (float('nan'),73,5000,True),
                (5000,float('nan'),5000,True)]:
            with self.subTest(swap=swap,free=free), tempfile.TemporaryDirectory() as d:
                evt=threading.Event(); evt.wait=lambda _:evt.set()
                state={'declenche':False,'swap_max':0,'detail':''}
                with patch.object(X,'_arret_memoire',state), \
                     patch.object(X,'swap_mio',return_value=swap), \
                     patch.object(X,'pression_libre_pct',return_value=free), \
                     patch.object(X,'poser_stop') as stop:
                    X.sonde_memoire(evt,base,str(Path(d)/'mem.csv'))
                    self.assertEqual(stop.called,expected)

    def test_stop_prevents_transport_and_timeout_bounded(self):
        motor=X.MoteurR2b('unused')
        with patch.object(X,'stop_demande',return_value=True), \
             patch.object(X.MoteurA5,'_poster') as send:
            with self.assertRaises(RuntimeError):motor._poster('/completion',{})
            send.assert_not_called()
        with patch.object(X,'stop_demande',return_value=False), \
             patch.object(X,'_arret_memoire',{'declenche':False}), \
             patch.object(X.MoteurA5,'_poster',return_value={}) as send:
            motor._poster('/completion',{'prompt':'same'},timeout=1800)
            send.assert_called_once_with('/completion',{'prompt':'same'},timeout=120)


class Integration(unittest.TestCase):
    def test_same_cache_isolation_and_collision(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d); traces=root/'traces'; traces.mkdir()
            items=[f'item{i}' for i in range(58)]
            ids=[f'synthetic{i}' for i in range(180)]
            paquet={'ids':ids,'items':items}
            a=pd.DataFrame([dict(pid=ids[i],index=i,pli=i//30) for i in range(150)])
            b=pd.DataFrame([dict(pid=ids[i],index=i,pli=(i-150)//6) for i in range(150,180)])
            a.to_csv(traces/'a5-personnes.csv',index=False)
            b.to_csv(traces/'r2b-personnes-ext.csv',index=False)
            for people,name in [(a,'r2-C3F-gptoss.jsonl'),(b,'r2b-C3F-gptoss-ext.jsonl')]:
                with (traces/name).open('w') as f:
                    for p in people.itertuples(index=False):
                        for item in items:
                            f.write(json.dumps(dict(pid=p.pid,item=item,pli=p.pli,
                                condition='C3F',passe=1,distribution={'a':1},argmax='a',
                                **E.REGISTRE))+'\n')
            for name in ['r2-C3-gptoss.jsonl','a5-C3F-p1.jsonl']:(traces/name).write_text('')
            caches=[]
            for i in range(4):
                p=root/f'cache{i}';p.write_text('synthetic');caches.append(str(p))
            out=root/'results'; work=root/'work'
            argv=['r2b_evaluer.py','--sortie',str(out),'--travail',str(work)]
            for flag,path in zip(['--cache','--cache-foret','--cache-a35','--cache-a41'],caches):argv += [flag,path]
            saved={p:p.read_bytes() for p in traces.iterdir()}
            def fake_main():
                self.assertIs(E.C41.charger_paquet('any'),paquet)
                self.assertEqual(Path(E.R2E.TRACES),work)
                self.assertIn(caches[3],sys.argv)
                E.C41.ecrire(pd.DataFrame({'aggregate':[180]}),'r2-tableau-180.csv')
            with patch.object(E,'TRACES',traces), patch.object(sys,'argv',argv), \
                 patch.object(E.C41,'charger_paquet',return_value=paquet) as loader, \
                 patch.object(E.C41,'colonnes_familles',return_value=(list(range(58)),{})), \
                 patch.object(E.R2E,'nomenclature',return_value={i:{'options':['a']} for i in items}), \
                 patch.object(E.R2E,'main',side_effect=fake_main), \
                 patch.object(E.R2E,'references_population',return_value={}), \
                 patch.object(E,'glissement_des_cellules',return_value=pd.DataFrame({'personnes':[150,180]})):
                E.main()
                loader.assert_called_once_with(*caches[:3])
                self.assertTrue((out/'r2b-tableau-180.csv').exists())
                self.assertTrue((out/'r2b-glissement-cellules-180.csv').exists())
                self.assertEqual(len((work/'r2b-C3F-gptoss-180.jsonl').read_text().splitlines()),10440)
                with self.assertRaises(SystemExit): E.main()
            self.assertTrue(all(p.read_bytes()==v for p,v in saved.items()))


if __name__=='__main__': unittest.main()
