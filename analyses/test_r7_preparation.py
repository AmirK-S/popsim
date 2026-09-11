"""Tests R7 stdlib, hors GPU; fixtures GGUF creuses, aucun poids copié."""
import contextlib
import io
import json
from pathlib import Path
import struct
import tempfile
import unittest
from unittest.mock import patch

import r7_convertir_finale as c
import r7_valider_gguf as v


class GGUFTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.base = v.CACHE/'gguf/Olmo-3-7B-base-Q8_0.gguf'
        cls.result = v.inspect(cls.base)
        with cls.base.open('rb') as f:
            cls.header = f.read(cls.result['data_offset'])

    def fixture(self, directory, header=None, size=None):
        p = Path(directory)/'test.gguf'
        with p.open('wb') as f:
            f.write(self.header if header is None else header)
            f.truncate(self.result['bytes'] if size is None else size)
        return p

    def test_four_real_files(self):
        results = [v.validate(v.CACHE/'gguf'/f'Olmo-3-7B-{k}-Q8_0.gguf')['status']
                   for k in ('base','sft','dpo','rlvr')]
        self.assertEqual(results, ['PASS','PASS','PASS','FAIL'])

    def test_sparse_valid_layout(self):
        with tempfile.TemporaryDirectory() as d:
            self.assertEqual(v.validate(self.fixture(d))['status'], 'PASS')

    def test_truncated_data(self):
        with tempfile.TemporaryDirectory() as d:
            r = v.validate(self.fixture(d, size=self.result['bytes']-100))
            self.assertEqual(r['status'], 'FAIL')
            self.assertIn('tronqué', r['error'])

    def test_wrong_quantization(self):
        h = bytearray(self.header)
        pos = h.index(b'token_embd.weight')+len(b'token_embd.weight')
        typ_offset = pos+4+2*8
        struct.pack_into('<I', h, typ_offset, 1)
        with tempfile.TemporaryDirectory() as d:
            self.assertIn('quantification', v.validate(self.fixture(d,h))['error'])

    def test_missing_layer_name(self):
        h = self.header.replace(b'blk.0.attn_k.weight', b'blk.9.attn_x.weight')
        with tempfile.TemporaryDirectory() as d:
            self.assertEqual(v.validate(self.fixture(d,h))['status'], 'FAIL')

    def test_overlap(self):
        h = bytearray(self.header)
        pos = h.index(b'blk.0.ffn_down.weight')+len(b'blk.0.ffn_down.weight')
        struct.pack_into('<Q', h, pos+4+2*8+4, 0)
        with tempfile.TemporaryDirectory() as d:
            self.assertIn('chevauchement', v.validate(self.fixture(d,h))['error'])


class ConversionTests(unittest.TestCase):
    def test_mac_truncated_comm_detects_r2b(self):
        ps = '999 /opt/homebrew/Ce /opt/homebrew/Cellar/python/Python -u /project/analyses/r2b_extension.py --heures 3\n'
        with patch.object(c.subprocess,'check_output',return_value=ps):
            self.assertEqual(c.blockers(), [{'pid':999,'command':'Python'}])

    def test_busy_refuses_before_io_or_process(self):
        with patch.object(c,'preflight',return_value={}), patch.object(c,'blockers',return_value=[{'pid':999}]), \
             patch.object(c,'sha256') as hashes, patch.object(c,'run_converter') as run, \
             patch.object(c.tempfile,'mkdtemp') as tmp, patch('sys.argv',['r7','--execute']), \
             contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(c.main(),1)
            hashes.assert_not_called(); run.assert_not_called(); tmp.assert_not_called()

    def fake_hash(self, path, **kwargs):
        return c.SHARDS[path.name][1] if path.name in c.SHARDS else 'fake-unit-test-hash'

    def convert_case(self, directory, hash_fn=None, validation=None):
        def fake_converter(command, log):
            self.assertIn(str(c.SNAPSHOT),command)
            self.assertNotIn('--vocab-only',command)
            out = Path(command[-1])
            self.assertNotEqual(out, v.CACHE/'gguf/Olmo-3-7B-rlvr-Q8_0.gguf')
            out.write_bytes(struct.pack('<4sIQQ',b'GGUF',3,0,0))
            log.write_text('fake converter, zero tensors, rc=0\n')
            return 0
        with patch.object(c,'preflight',return_value={}), patch.object(c,'require_idle'), \
             patch.object(c,'sha256',side_effect=hash_fn or self.fake_hash), \
             patch.object(c,'run_converter',side_effect=fake_converter) as run:
            if validation is None:
                with self.assertRaises(RuntimeError):
                    c.convert(Path(directory))
            else:
                with patch.object(c,'validate',return_value=validation):
                    c.convert(Path(directory))
            return run.call_count

    def test_hash_mismatch_blocks_conversion(self):
        with tempfile.TemporaryDirectory() as d:
            self.assertEqual(self.convert_case(d, hash_fn=lambda *a,**k:'wrong'),0)
            rec=json.loads((Path(d)/'provenance.json').read_text())
            self.assertEqual(rec['status'],'FAILED')
            self.assertIn('SHA-256',rec['error'])

    def test_rc_zero_empty_export_rejected_and_recorded(self):
        with tempfile.TemporaryDirectory() as d:
            self.assertEqual(self.convert_case(d),1)
            rec=json.loads((Path(d)/'provenance.json').read_text())
            self.assertEqual(rec['status'],'FAILED')
            self.assertEqual(rec['returncode'],0)
            self.assertEqual(rec['validation']['status'],'FAIL')

    def test_success_stays_temporary_with_provenance(self):
        # Validation simulée uniquement pour vérifier l'orchestration de succès.
        with tempfile.TemporaryDirectory() as d:
            self.assertEqual(self.convert_case(d, validation={'status':'PASS'}),1)
            rec=json.loads((Path(d)/'provenance.json').read_text())
            self.assertEqual(rec['status'],'VALIDATED_TEMPORARY')
            self.assertEqual(len(rec['shards']),3)
            self.assertTrue(Path(rec['output']).name.endswith('.partial.gguf'))
            self.assertIn('output_sha256',rec)


if __name__ == '__main__':
    unittest.main()
