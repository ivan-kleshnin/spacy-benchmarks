# spaCy Benchmarks

Comparison of Spacy performance with different architectures, corpuses, hyperparams...

## tok2vec.model depth

### Constants

- Corpus: EWT + GUM + GENTLE converted to CLEARNLP format.
- Ad hoc tokenizer.
- Static Vectors: MD.

### Experiment

```
components.tok2vec.model.encode.width: 128
components.tok2vec.model.encode.depth: 8 -> 6
```

```
Training time: 1:08:16.50 -> 56:44.51
TAGG_ACC: 96.33 -> 96.44
DEP_UAS: 89.61 -> 89.53
DEP_LAS: 87.38 -> 87.22
SENTS_F: 80.92 -> 81.32
```
