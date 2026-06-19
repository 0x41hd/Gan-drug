# -*- coding: utf-8 -*-
"""
tokens.py

Provides the tokens_table class required by predictor.py.

The original GAN-Drug-Generator project referenced a `tokens` module that was
not always shipped with the code. This class exposes the SMILES token alphabet
and, crucially, `table_len` — the size of the embedding input dimension used by
the LSTM predictor.

The token list below matches the SMILES character set produced by
Vocabulary2.Vocabulary (Br -> R, Cl -> L, Se -> E, Si -> X substitutions, plus
the 'G' start token and 'A' padding token).

IMPORTANT: table_len must be >= the largest integer index produced by the
Vocabulary encoder, otherwise the Embedding layer will raise an
InvalidArgumentError at runtime. To stay safe, this table is built to be a
superset of the standard ChEMBL/ZINC SMILES alphabet.
"""


class tokens_table(object):
    """SMILES token table.

    Attributes
    ----------
    table : list[str]
        The list of SMILES tokens.
    table_len : int
        Number of tokens (used as the Embedding input dimension).
    """

    def __init__(self):
        # Standard SMILES alphabet used by the LatentGAN / FeedbackGAN project.
        # This is a superset that safely covers ChEMBL/ZINC drug-like molecules
        # after the Br->R, Cl->L, Se->E, Si->X substitutions.
        tokens = [
            'H', 'B', 'C', 'N', 'O', 'F', 'P', 'S', 'I',
            'R',  # Br
            'L',  # Cl
            'E',  # Se
            'X',  # Si
            'c', 'n', 'o', 's', 'p', 'b',
            '(', ')', '[', ']', '=', '#', '-', '+', '/', '\\',
            '@', '.', '%',
            '0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
            'G',  # START token
            'A',  # PADDING token
            '*',  # wildcard / extra
        ]

        self.table = tokens
        self.table_len = len(self.table)
