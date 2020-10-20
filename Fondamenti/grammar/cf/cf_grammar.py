#!/usr/bin/env python3
"""Classes and methods for working with context free grammars."""

import copy

import tools.tools as tools
import grammar.base.grammar_exceptions as ge

import grammar.base.grammar as grammar


class CFG(grammar.Grammar):
    """
    A context free grammar.

    Created by:
        CFG(): definition provided as call parameters
        CFG.load(file): definition provided in yaml file
        cfg.remove_nulls(): derived from given cfg removing null (epsilon) productions
        cfg.remove_unit_prods(): derived from given cfg removing null and unitary
            productions
        cfg.reduce(): grammar in reduced form equivalent to given cfg
        cfg.cnf(): grammar in CNF equivalent to given cfg
        *cfg.gnf(): grammar in GNF equivalent to given cfg
        *CFG.from_NPDA(): derived from given NPDA

    A CFG is coded as follows:
        - terminals are defined as strings
        - the set of terminals is a Python set of strings
        - nonterminals are defined as strings
        - the set of nonterminals is a Python set of strings
        - axiom is a string
        - productions is a Python dictionary where
            - keys are Python tuples of strings of length one
            - values are Python dicts where
                - keys are input symbols, including the empty string ''
                - values are sets of possibly empty Python tuples of strings
                A->a | AaA | '' is encoded as
                    productions[('A',)]={('a',), ('A', 'a', 'A'), ()}
    """

    def __init__(self, *, terminals, non_terminals, axiom, productions,
                 no_null_production=False, null_string_produced=None,
                 no_unit_production=False, reduced=False, cnf=False, gnf=False):
        """
        Initialize grammar.

        no_null_production = True iff there is no null production, except possibly
        from the axiom
        null_string_produced = True iff the null string belongs to the language
        no_unit_production = True iff there is no unit production: by construction,
        no_unit_production implies no_null_production
        reduced = True iff there is no useless symbol (the grammar is in reduced form):
        by construction, reduced implies no_unit_production
        cnf = True iff the grammar is in CNF
        gnf = True iff the grammar is in GNF
        """
        super().__init__(terminals, non_terminals, axiom)
        self.productions = grammar.Grammar.build_productions(productions, non_terminals)
        self.no_null_production = no_null_production
        if null_string_produced is None:
            self.null_string_produced = self._null_string_produced()
        else:
            self.null_string_produced = null_string_produced
        self.no_unit_production = no_unit_production
        self.reduced = reduced
        self.cnf = cnf
        self.gnf = gnf
        self.validate()

    @classmethod
    def from_NPDA(cls, npda):
        """Initialize this CFG as one equivalent to the given NPDA."""
        return npda.cfg

# -----------------------------------------------------------------------------
# Validation

    def _validate_left_part(self, left_part, right_parts):
        """
        Raise an error if the left part of a production is invalid.

        Checks that the left part is a single non terminal.
        """
        super()._validate_left_part(left_part, right_parts)
        if len(left_part) != 1 and left_part != ("S'",):
            raise ge.InvalidLeftPartError(
                 'left part {} of productions has more than one symbol'.format(left_part))

    def _validate_right_part(self, left_part, right_part):
        """
        Raise an error if the right part of a production is invalid.

        Checks that the right part is a (possibly empty) sequence of terminals
        and non terminals
        """
        super()._validate_right_part(left_part, right_part)
        if right_part != ('',) and not set(right_part).issubset(self.terminals.union(
                    self.non_terminals)):
            raise ge.InvalidRightPartError(
                'production {} -> {} is not valid'
                .format(left_part, right_part))

    @property
    def _nullable_symbols(self):
        """Return the set of nullable non terminals of the grammar."""
        nullable_lp = set()
        non_nullable_lp = set(self.productions.keys())
        for left_part, right_parts in self.productions.items():
            if () in right_parts:
                nullable_lp.add(left_part)
                non_nullable_lp.remove(left_part)
        modified = True
        # repeat if the set of nullable left parts was modified
        while modified:
            modified = False
            Updated_nullable_lp = nullable_lp.copy()
            non_nullable_lp = non_nullable_lp.difference(nullable_lp)
            for left_part in non_nullable_lp:
                # for each current non nullable, consider all productions
                for right_part in self.productions[left_part]:
                    checks = [(x,) in nullable_lp for x in right_part]
                    if sum(checks) == len(checks):
                        # the right part of the production is composed of nullables
                        Updated_nullable_lp.add(left_part)
                        break
            if Updated_nullable_lp != nullable_lp:
                nullable_lp = Updated_nullable_lp
                modified = True
        nullables = {lp[0] for lp in nullable_lp}
        return nullables

    @property
    def productive_symbols(self):
        """Return nonterminals of this grammar from which some string can be produced."""
        grammar = self.remove_unit_prods() if self.no_unit_production else self
        return CFG._productive_symbols(grammar.terminals, grammar.non_terminals,
                                       grammar.productions)

    @property
    def reachable_symbols(self):
        """Return nonterminals of this grammar appearing in phrases produced by axiom."""
        grammar = self.remove_unit_prods() if self.no_unit_production else self
        return CFG._reachable_symbols(grammar.terminals, grammar.non_terminals,
                                      grammar.productions, grammar.axiom)

    @property
    def axiom_in_rp(self):
        """Return True if axiom appears in some right part."""
        for right_parts in self.productions.values():
            for right_part in right_parts:
                if self.axiom in set(right_part):
                    return True
        return False

    def _null_string_produced(self):
        """Return True if the grammar produces the null string."""
        return self.axiom in self._nullable_symbols

    def remove_nulls(self):
        """
        Remove null productions from this grammar.

        A new equivalent grammar with no null productions is returned. If the null
        string belongs to the language and the axiom appear in some right
        part of a production, a new axiom S' is introduced which produced the old axiom
        and the null string
        """
        grammar = self
        nullables = grammar._nullable_symbols
        # the new set of productions
        prods = {}
        for left_part, right_parts in grammar.productions.items():
            # list of all resulting productions from left_part
            new_right_parts = []
            # new productions
            for right_part in right_parts:
                # each production from left_part
                if len(right_part) > 1:
                    # right_part has at least two symbols
                    # list of indices of nullable symbols in right part
                    nullable_inds = [i for i, symbol in enumerate(right_part)
                                     if symbol in nullables]
                    # list of all resulting productions from left_part->right_part
                    # start with the case when all nullables are not null
                    new_rps = [right_part]
                    for i in nullable_inds[::-1]:
                        # list of new right_parts
                        updated_rps = []
                        # for each already derived right_part, introduce a new one
                        # with null current nullable
                        for rp in new_rps:
                            lrp = list(rp)
                            _ = lrp.pop(i)
                            if lrp:
                                # insert new right_part if it has length > 0
                                updated_rps.append(tuple(lrp))
                        new_rps.extend(updated_rps)
                    new_right_parts.extend(new_rps)
                elif len(right_part) == 1:
                    new_right_parts.append(right_part)
                prods[left_part] = set(new_right_parts)
        # the set of productions in prods produces the same language as this grammar,
        # except, in case, the null string
        if not grammar.null_string_produced:
            # the null string is not produced in this grammar: a new grammar with
            # same symbols and productions from prods is returned
            axiom = grammar.axiom
            non_terminals = grammar.non_terminals.copy()
        elif not grammar.axiom_in_rp:
            # the null string is produced in this grammar and the axiom does not appear
            # in any right part: a new production axiom -> () is introduced
            axiom = grammar.axiom
            non_terminals = grammar.non_terminals.copy()
            prods[(grammar.axiom,)].add(())
        else:
            # the null string is produced in this grammar and the axiom does appear
            # in some right part: a new axiom S' is introduced, with the same
            # productions from axiom, plus S' -> ()
            axiom = "S'"
            non_terminals = grammar.non_terminals.copy()
            non_terminals = non_terminals.union({"S'"})
            prods[("S'",)] = {(grammar.axiom,), ()}
        return grammar.__class__(terminals=grammar.terminals,
                                 non_terminals=non_terminals,
                                 axiom=axiom,
                                 productions=prods,
                                 no_null_production=True,
                                 null_string_produced=grammar.null_string_produced)

    def remove_unit_prods(self):
        """Return grammar with no null or unitary production."""
        def unitaries(productions, nonterminals):
            """
            Return sets of nonterminals produce through unitary productions.

            unitary dict associates to left part the set of right parts produced through
            sequences of unitary productions
            """
            unitary = {lp: set() for lp in productions.keys()}
            for left_part, right_parts in productions.items():
                for right_part in right_parts:
                    if len(right_part) == 1 and right_part[0] in nonterminals:
                        unitary[left_part].add(right_part)
            unitary_updated = unitary.copy()
            flag = True
            while flag:
                flag = False
                for key, values in unitary.items():
                    for value in values:
                        unitary_updated[key] = unitary_updated[key].union(unitary[value])
                if unitary != unitary_updated:
                    unitary = unitary_updated
                    flag = True
            unitary.pop(("S'",), None)
            for lp in unitary.keys():
                if lp in unitary[lp]:
                    unitary[lp].remove(lp)
            return unitary

        if self.no_null_production:
            grammar = self
        else:
            grammar = self.remove_nulls()
        productions = copy.deepcopy(grammar.productions)
        # unitary associates to left part the set of right parts produced through
        # sequences of unitary productions
        unitary = unitaries(productions, grammar.non_terminals)
        prods = {}
        # remove unitary productions
        for left_part in productions.keys():
            if left_part == ("S'",):
                prods[left_part] = productions[left_part]
            else:
                rps = {rp for rp in productions[left_part] if len(rp) != 1 or
                       rp[0] in grammar.terminals}
                prods[left_part] = rps
        # add productions corresponding to chains of unitary productions
        for left_part in productions.keys():
            if left_part != ("S'",):
                rps = set()
                for lp in unitary[left_part]:
                    if lp != left_part:
                        rps = rps.union(prods[lp])
                prods[left_part] = prods[left_part].union(rps)
        return grammar.__class__(terminals=grammar.terminals,
                                 non_terminals=grammar.non_terminals,
                                 axiom=grammar.axiom,
                                 productions=prods,
                                 no_null_production=True,
                                 null_string_produced=self.null_string_produced,
                                 no_unit_production=True)

    @classmethod
    def _productive_symbols(cls, terminals, nonterminals, productions):
        """Return nonterminals from which some string can be produced."""
        productives = set()
        flag = True
        while flag:
            flag = False
            nt_to_check = nonterminals.difference(productives)
            for nt in nt_to_check:
                for right_part in productions[(nt,)]:
                    if set(right_part).issubset(productives.union(terminals)):
                        productives.add(nt)
                        flag = True
        return productives

    @classmethod
    def _reachable_symbols(cls, terminals, nonterminals, productions, axiom):
        """Return symbols in phrases produced starting from axiom."""
        # set of reachable symbols
        reachables = {axiom}
        nt_to_check = set()
        while reachables != nt_to_check:
            nt_to_check = reachables.copy()
            for nt in nt_to_check.intersection(nonterminals):
                for right_part in productions[(nt,)]:
                    for symbol in right_part:
                        if symbol not in reachables:
                            reachables.add(symbol)
        return reachables

    def reduce(self):
        """Return grammar in reduced form."""
        if self.no_unit_production:
            grammar = self
        else:
            grammar = self.remove_unit_prods()
        productions = copy.deepcopy(grammar.productions)
        nonterminals = grammar.non_terminals.copy()
        terminals = grammar.terminals
        axiom = grammar.axiom
        if grammar.null_string_produced:
            axiom = list(filter(lambda x: (len(x) > 0), productions[(axiom,)]))[0][0]
            _ = productions.pop(("S'",), None)
            nonterminals.remove("S'")
        # derive the set of nonterminals producing some string
        productives = CFG._productive_symbols(terminals, nonterminals, productions)
        if axiom not in productives:
            # axiom is not productive, no symbol in language, possibly except null
            if grammar.null_string_produced:
                # language includes only the null string
                axiom = "S'"
                non_terminals = {"S'"}
                terminals = set()
                productions = {}
                productions[("S'",)] = {()}
            else:
                # languge is empty
                non_terminals = {axiom}
                terminals = set()
                productions = {}
        else:
            # axiom is productive, language includes some string, plus possibly null
            keys = list(productions.keys())
            for lp in keys:
                if lp[0] not in productives:
                    # remove productions from non productive nonterminals
                    _ = productions.pop(lp, None)
                else:
                    rps = productions[lp].copy()
                    for rp in rps:
                        if not set(rp).issubset(productives.union(terminals)):
                            # remove productions with nonproductive terminals in rightpart
                            productions[lp].remove(rp)
            # derive the set of terminals and nonterminals produced from the axiom
            useful = CFG._reachable_symbols(terminals, productives, productions, axiom)
            keys = list(productions.keys())
            for lp in keys:
                if lp[0] not in useful:
                    # remove productions from useless nonterminals
                    _ = productions.pop(lp, None)
                else:
                    rps = productions[lp].copy()
                    for rp in rps:
                        if not set(rp).issubset(useful):
                            # remove productions with useless symbols in rightpart
                            productions[lp].remove(rp)
            non_terminals = productives.intersection(useful)
            terminals = terminals.intersection(useful)
            if grammar.null_string_produced:
                # languge includes the null string
                non_terminals = non_terminals.union({"S'"})
                productions[("S'",)] = {(grammar.axiom,), ()}
        return grammar.__class__(terminals=terminals,
                                 non_terminals=non_terminals,
                                 axiom=grammar.axiom,
                                 productions=productions,
                                 no_null_production=True,
                                 null_string_produced=grammar.null_string_produced,
                                 no_unit_production=True,
                                 reduced=True)

    def to_cnf(self):
        """Return equivalent grammar in Chomsky Normal Form."""
        if self.reduced:
            grammar = self
        else:
            grammar = self.reduce()
        productions = copy.deepcopy(grammar.productions)
        nonterminals = copy.deepcopy(grammar.non_terminals)
        terms_dict = {}
        for t in grammar.terminals:
            nt = tools.Tools.new_nt_symbol(nonterminals)
            nonterminals.add(nt)
            terms_dict[t] = nt
            productions[(nt,)] = {(t,)}
        for left_part, right_parts in grammar.productions.items():
            if left_part != ("S'",):
                rps = set()
                for right_part in right_parts:
                    if len(right_part) == 1:
                        rps.add(right_part)
                    else:
                        rps.add(tuple([terms_dict[symbol] if symbol in grammar.terminals
                                       else symbol for symbol in right_part]))
                productions[left_part] = rps
        prods = {}
        for left_part, right_parts in productions.items():
            if left_part == ("S'",):
                prods[("S'",)] = productions[("S'",)].copy()
            else:
                prods[left_part] = set()
                for right_part in right_parts:
                    rp = copy.deepcopy(right_part)
                    while len(rp) > 2:
                        prefix = rp[:2]
                        nt = tools.Tools.new_nt_symbol(nonterminals)
                        nonterminals.add(nt)
                        prods[(nt,)] = {prefix}
                        rp = rp[2:]
                        lst = list(rp)
                        lst.insert(0, nt)
                        rp = tuple(lst)
                    prods[left_part].add(rp)
        return CFG(terminals=grammar.terminals,
                   non_terminals=nonterminals,
                   axiom=grammar.axiom,
                   productions=prods,
                   no_null_production=True,
                   null_string_produced=grammar.null_string_produced,
                   no_unit_production=True,
                   reduced=True,
                   cnf=True)

    def to_gnf(self):
        """Return equivalent grammar in Greibach Normal Form."""
        if self.cnf:
            grammar = self
        else:
            grammar = self.to_cnf()
            # stub: to be done
        new_grammar = None
        return new_grammar

    @property
    def npda(self):
        """Return NPDA equivalent to this CFG."""
        npda = None
        # stub: to be done
        return npda

# -----------------------------------------------------------------------------
# Other

    def __str__(self):
        """Return a string representation of the grammar."""
        s = 'terminals: {}\n'.format(','.join(sorted(self.terminals)))
        s += 'non terminals: {}\n'.format(','.join(sorted(self.non_terminals)))
        s += 'axiom: {}\n'.format(self.axiom)
        s += 'productions\n'
        if self.all_chars:
            for left, rights in self.productions.items():
                if rights:
                    s += '\t'+tools.Tools.print(left)+' -> '
                    for right in rights:
                        s += ''+tools.Tools.print(right) + ' | '
                    s = s[:-2]
                    s += '\n'
            return s[:-2]
        else:
            for left, rights in self.productions.items():
                if rights:
                    s += '\t'+tools.Tools.print_tuple(left)+' -> '
                    for right in rights:
                        s += ''+tools.Tools.print_tuple(right) + ' | '
                    s = s[:-2]
                    s += '\n'
            return s[:-2]
