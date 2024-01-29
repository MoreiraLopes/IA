#encoding: utf8

# YOUR NAME: Gonçalo Rafael Correia Moreira Lopes
# YOUR NUMBER: 107572
 
# COLLEAGUES WITH WHOM YOU DISCUSSED THIS ASSIGNMENT (names, numbers):
# - Cristiano Nicolau, 108536
# - ...

from semantic_network import *
from constraintsearch import *
from math import sqrt

class MySN(SemanticNetwork):

    def __init__(self):
        SemanticNetwork.__init__(self)
        self.assoc_stats = {}
        # ADD CODE HERE IF NEEDED
        pass

    def query_local(self, user=None, e1=None, rel=None, e2=None, rel_type=None):
        self.query_result = [
            Declaration(decl_user, Relation(d[0], d[1], entity)) 
            for decl_user, user_data in self.declarations.items()
            for d in user_data.keys()
            if (user is None or decl_user == user)
            and (e1 is None or e1 == d[0])
            and (rel is None or rel == d[1])
            and (e2 is None or (isinstance(user_data[d], set) and e2 in user_data[d]) or (not isinstance(user_data[d], set) and e2 == user_data[d]))
            for entity in (user_data[d] if isinstance(user_data[d], set) else [user_data[d]])
        ]
        return self.query_result



    def query(self, entity, rel=None):
        visited = set()
        decl_local = self.query_local(e1=entity, rel=rel, rel_type=Association)
        visited.update(decl_local)
        pred_direct = self.query_local(e1=entity, rel_type=(Member, Subtype))
        decl = decl_local

        seen_relations = set()

        for dp in pred_direct:
            sub_query = self.query(dp.relation.entity2, rel)
            for decl_item in sub_query:
                
                if decl_item not in visited and (dp.relation, decl_item.relation.entity2) not in seen_relations:
                    decl.append(decl_item)
                    visited.add(decl_item)
                    # Add the relation to the seen set
                    seen_relations.add((dp.relation, decl_item.relation.entity2))
        
        for i in decl:
            if i.relation.name == 'subtype' or i.relation.name == 'member':
                decl.remove(i)

        self.query_result = decl
        return self.query_result



    def update_assoc_stats(self, assoc, user=None):
        if user is None:
            users = self.declarations.keys()
            total_freq_count = {}
            total_total_count = 0

            for user_key in users:
                entities = set()
                freq_count = {}
                total_count = 0

                for decl, data in self.declarations[user_key].items():
                    if decl[1] == assoc:
                        entities.add(decl[0])
                        if isinstance(data, set):
                            for e in data:
                                freq_count.setdefault(e, 0)
                                freq_count[e] += 1
                                total_count += 1
                        else:
                            freq_count.setdefault(data, 0)
                            freq_count[data] += 1
                            total_count += 1

                for entity, freq in freq_count.items():
                    self.assoc_stats.setdefault((assoc, user_key), [{}, {}])
                    self.assoc_stats[assoc, user_key][0][entity] = freq / total_count if total_count > 0 else 0

               
                for entity, freq in freq_count.items():
                    total_freq_count.setdefault(entity, 0)
                    total_freq_count[entity] += freq
                    total_total_count += total_count

           
            for entity, freq in total_freq_count.items():
                self.assoc_stats.setdefault((assoc, None), [{}, {}])
                self.assoc_stats[assoc, None][0][entity] = freq / total_total_count if total_total_count > 0 else 0

        else:
            users = [user]

            for user_key in users:
                entities = set()
                freq_count = {}
                total_count = 0

                for decl, data in self.declarations[user_key].items():
                    if decl[1] == assoc:
                        entities.add(decl[0])
                        if isinstance(data, set):
                            for e in data:
                                freq_count.setdefault(e, 0)
                                freq_count[e] += 1
                                total_count += 1
                        else:
                            freq_count.setdefault(data, 0)
                            freq_count[data] += 1
                            total_count += 1

                self.assoc_stats.setdefault((assoc, user_key), [{}, {}])

                for entity, freq in freq_count.items():
                    self.assoc_stats[assoc, user_key][0][entity] = freq / total_count if total_count > 0 else 0

        return self.assoc_stats







        




class MyCS(ConstraintSearch):

    def __init__(self, domains, constraints):
        super().__init__(domains, constraints)

    def search_all(self, domains=None, assignment=None):
        if assignment is None:
            assignment = []

        if domains is None:
            domains = self.domains
        
        if len(assignment) == len(domains):
            return [dict(assignment)]
        
        var = self.select_unassigned_variable(domains, assignment)
        solutions = []
        for value in domains[var]:
            new_assignment = assignment + [(var, value)]
            new_domains = self.forward_check(domains, var, value, new_assignment)
            if new_domains is not None:
                sub_solutions = self.search_all(new_domains, new_assignment)
                solutions.extend(sub_solutions)

        return solutions

    def select_unassigned_variable(self, domains, assignment):
        assigned_vars = {v for v, _ in assignment}
        unassigned_vars = domains.keys() - assigned_vars
        return next(iter(unassigned_vars), None)

    def forward_check(self, domains, var, value, assignment):
        new_domains = {v: domains[v][:] if v != var else [value] for v in domains}

        for other_var in new_domains:
            if other_var != var:
                to_remove = []
                for v2 in new_domains[other_var]:
                    if not self.is_consistent(var, value, other_var, v2):
                        to_remove.append(v2)
                for v_to_remove in to_remove:
                    new_domains[other_var].remove(v_to_remove)
                if not new_domains[other_var]:
                    return None 

        return new_domains

    def is_consistent(self, var1, value1, var2, value2):
        if (var1, var2) in self.constraints:
            return self.constraints[var1, var2](var1, value1, var2, value2)
        return True
    