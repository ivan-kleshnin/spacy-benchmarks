from collections import Counter
import os
from pathlib import Path
from typing import Literal
import spacy
from spacy.tokens import Doc
import srsly
from utils import normalize

def simplify_deprel(deprel: str) -> str:
  deprel = deprel.split(":")[0]
  table = {
    "ROOT": "root",
    # Fewer weak rules
    "parataxis": "dep",
    "meta": "dep",
    # No passives
    "nsubjpass": "nsubj",
    "csubjpass": "csubj",
    "auxpass": "aux",
    # No "conj:preconj"
    "preconj": "conj",
    # No "det:predet"
    "predet": "det",
    # No "acl:relcl"
    "relcl": "acl",
    # No "nmod:poss"
    "poss": "nmod",
    # Just a subset of "ccomp"
    "xcomp": "ccomp",
    # Just an object, no need to philosophize
    "oprd": "dobj",
    # https://universaldependencies.org/docs/en/overview/migration-guidelines.html
    "quantmod": "advmod",
    "npadvmod": "nmod",
  }
  return table[deprel] if deprel in table else deprel

similar_tags = {
  "NN": {"NNS", "NNP", "NNPS"},
  "NNS": {"NN", "NNP", "NNPS"},
  "NNP": {"NN", "NNS", "NNPS"},
  "NNPS": {"NN", "NNS", "NNP"},
}

def fuzzy_equal_tags(tup: tuple[str, str]):
  tag1, tag2 = tup
  if tag1 == tag2:
    return True
  elif (
    tag1 in similar_tags and tag2 in similar_tags[tag1] or
    tag2 in similar_tags and tag1 in similar_tags[tag2]
  ):
    return True
  return False

type Status = Literal["OK", "ERR"]
type ErrCode = Literal["Deps", "Heads", "Tags"]

def compare_docs(doc1: Doc, doc2: Doc) -> tuple[Status, set[ErrCode]]:
  errors: set[ErrCode] = set([])
  # Compare deps
  deps1 = [simplify_deprel(tok.dep_) for tok in doc1]
  deps2 = [simplify_deprel(tok.dep_) for tok in doc2]
  if deps1 != deps2:
    errors.add("Deps")
  # Compare heads
  heads1 = [tok.head.i for tok in doc1]
  heads2 = [tok.head.i for tok in doc2]
  if heads1 != heads2:
    errors.add("Heads")
  # Compare tags
  tags1 = [tok.tag_ for tok in doc1]
  tags2 = [tok.tag_ for tok in doc2]
  if not all(fuzzy_equal_tags(pair) for pair in zip(tags1, tags2)):
    errors.add("Tags")
  return "ERR" if len(errors) else "OK", errors

snlp = spacy.load("en_core_web_sm")
mnlp = spacy.load("en_core_web_md")
lnlp = spacy.load("en_core_web_lg")
tnlp = spacy.load("en_core_web_trf")

indir = os.path.realpath("./texts-norm")

infiles = [
  os.path.realpath(os.path.join(dirpath, filename))
  for (dirpath, dirnames, filenames) in os.walk(indir)
  for filename in filenames
  if filename.endswith(".jsonl") and "gentle-" in filename
]

# TODO `pipe` all texts through models and pass two docs to `is_recognizable_text`

# --- Report on any water use amounts ---

for infile in infiles:
  print(f"Handling {infile!r}")
  data = srsly.read_jsonl(infile)
  ptexts = {
    row["text"] for row in data
    if isinstance(row, dict) and "text" in row and len(row["text"]) > 10
  }
  sdocs = list(snlp.pipe(ptexts))
  # print([(token, token.tag_) for token in sdocs[0]])
  mdocs = list(mnlp.pipe(ptexts))
  # print([(token, token.tag_) for token in mdocs[0]])
  ldocs = list(lnlp.pipe(ptexts))
  # print([(token, token.tag_) for token in ldocs[0]])
  tdocs = list(tnlp.pipe(ptexts))
  # print([(token, token.tag_) for token in tdocs[0]])
  # Stats
  all_errors: list[ErrCode] = []
  # sm-md
  sm_md_errors: list[ErrCode] = []
  for sdoc, mdoc in zip(sdocs, mdocs):
    status, errors = compare_docs(sdoc, mdoc)
    if status == "ERR":
      all_errors.extend(errors)
      sm_md_errors.extend(errors)
  # md-lg
  md_lg_errors: list[ErrCode] = []
  for mdoc, ldoc in zip(mdocs, ldocs):
    status, errors = compare_docs(mdoc, ldoc)
    if status == "ERR":
      all_errors.extend(errors)
      md_lg_errors.extend(errors)
  # md-tr
  md_tr_errors: list[ErrCode] = []
  for mdoc, tdoc in zip(mdocs, tdocs):
    status, errors = compare_docs(mdoc, tdoc)
    if status == "ERR":
      all_errors.extend(errors)
      md_tr_errors.extend(errors)
  # lg-tr
  lg_tr_errors: list[ErrCode] = []
  for ldoc, tdoc in zip(ldocs, tdocs):
    status, errors = compare_docs(ldoc, tdoc)
    if status == "ERR":
      all_errors.extend(errors)
      lg_tr_errors.extend(errors)
  print("All errors:", Counter(all_errors))
  print("sm-md errors:", Counter(sm_md_errors))
  print("md-lg errors:", Counter(md_lg_errors))
  print("md-tr errors:", Counter(md_tr_errors))
  print("lg-tr errors:", Counter(lg_tr_errors))
 
