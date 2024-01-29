

# Guiao de representacao do conhecimento
# -- Redes semanticas
# 
# Inteligencia Artificial & Introducao a Inteligencia Artificial
# DETI / UA
#
# (c) Luis Seabra Lopes, 2012-2020
# v1.9 - 2019/10/20
#


# Classe Relation, com as seguintes classes derivadas:
#     - Association - uma associacao generica entre duas entidades
#     - Subtype     - uma relacao de subtipo entre dois tipos
#     - Member      - uma relacao de pertenca de uma instancia a um tipo
#

class Relation:
    def __init__(self,e1,rel,e2):
        self.entity1 = e1
#       self.relation = rel  # obsoleto
        self.name = rel
        self.entity2 = e2
    def __str__(self):
        return self.name + "(" + str(self.entity1) + "," + \
               str(self.entity2) + ")"
    def __repr__(self):
        return str(self)


# Subclasse Association
class Association(Relation):
    def __init__(self,e1,assoc,e2):
        Relation.__init__(self,e1,assoc,e2)
    
class AssocOne(Relation):
    def __init__(self,e1,assoc,e2):
        Relation.__init__(self,e1,assoc,e2)

class AssocNum(Relation):
    def __init__(self,e1,assoc,e2):
        Relation.__init__(self,e1,assoc,e2)

#   Exemplo:
#   a = Association('socrates','professor','filosofia')

# Subclasse Subtype
class Subtype(Relation):
    def __init__(self,sub,super):
        Relation.__init__(self,sub,"subtype",super)


#   Exemplo:
#   s = Subtype('homem','mamifero')

# Subclasse Member
class Member(Relation):
    def __init__(self,obj,type):
        Relation.__init__(self,obj,"member",type)

#   Exemplo:
#   m = Member('socrates','homem')

# classe Declaration
# -- associa um utilizador a uma relacao por si inserida
#    na rede semantica
#
class Declaration:
    def __init__(self,user,rel):
        self.user = user
        self.relation = rel
    def __str__(self):
        return "decl("+str(self.user)+","+str(self.relation)+")"
    def __repr__(self):
        return str(self)

#   Exemplos:
#   da = Declaration('descartes',a)
#   ds = Declaration('darwin',s)
#   dm = Declaration('descartes',m)

# classe SemanticNetwork
# -- composta por um conjunto de declaracoes
#    armazenado na forma de uma lista
#
class SemanticNetwork:
    def __init__(self,ldecl=None):
        self.declarations = [] if ldecl==None else ldecl
    def __str__(self):
        return str(self.declarations)
    def insert(self,decl):
        self.declarations.append(decl)
    def query_local(self,user=None,e1=None,rel=None,rel_type=None, e2=None):
        self.query_result = \
            [ d for d in self.declarations
                if  (user == None or d.user==user)
                and (e1 == None or d.relation.entity1 == e1)
                and (rel == None or d.relation.name == rel)
                and (rel_type == None or isinstance(d.relation,rel_type))
                and (e2 == None or d.relation.entity2 == e2) ]
        return self.query_result


    def show_query_result(self):
        for d in self.query_result:
            print(str(d))

    def list_associations(self):
        decl = self.query_local(rel_type=Association)
        return list(set([d.relation.name for d in decl]))

    def list_objects(self):
        decl = self.query_local(rel_type=Member)
        return list(set([d.relation.entity1 for d in decl]))

    def list_users(self):
        decl = self.query_local()
        return list(set([d.user for d in decl]))

    def list_types(self):
        decl1 = self.query_local(rel_type=Member)
        tipos = [d.relation.entity2 for d in decl1]

        decl2 = self.query_local(rel_type=Subtype)
        tipos += [d.relation.entity1 for d in decl2]
        tipos += [d.relation.entity2 for d in decl2]
        return list(set(tipos))


    def list_local_associations(self,entity):
        decl = self.query_local(rel_type=Association, e1=entity)
        decl += self.query_local(rel_type=Association, e2=entity)
        return list(set([d.relation.name for d in decl]))

    def list_relations_by_user(self,user):
        decl = self.query_local(user=user)
        return list(set([d.relation.name for d in decl])) 

    def associations_by_user(self,user):
        decl = self.query_local(user=user, rel_type=Association)
        return len(list(set([d.relation.name for d in decl])))

    def list_associations_by_entity(self, entity):
        decl = self.query_local(rel_type=Association, e1=entity)
        decl += self.query_local(rel_type=Association, e2=entity)
        return list(set([d.relation.name for d in decl]))

    def predecessor(self, b, a):
        decl = self.query_local(e1=a, rel_type=(Member, Subtype))
        predecessors = [d.relation.entity2 for d in decl]

        if b in predecessors:
            return True
        return any([self.predecessor(b, p) for p in predecessors])


    def predecessor_path(self, b, a):
        decl = self.query_local(e1=a, rel_type=(Member, Subtype))
        predecessors = [d.relation.entity2 for d in decl]

        if b in predecessors:
            return [b, a]

        for p in [self.predecessors(b, p) for p in predecessors]:
            if p_path:
                return p_path + [a]

    def query(self, e1=None, rel=None):
        local = self.query_local(e1=e1, rel=rel)

        decl = self.query_local(e1=e1, rel_type=(Member, Subtype))
        predecessors = [d.relation.entity2 for d in decl]
        
        for r in [self.query(e1=p, rel=rel) for p in predecessors]:
            local += r
        
        return local

    def query2(self, e1=None, rel=None):
        inherited = self.query_local(e1=e1, rel=rel)

        local = self.query_local(e1=e1, rel=rel, rel_type=(Member, Subtype))

        return local + inherited

    def query_cancel(self, e1=None, rel=None):
        local = self.query_local(e1=e1, rel=rel, rel_type=Association)
        local_rels = [r.relation.name for r in local]

        decl = self.query_local(e1=e1, rel_type=(Member, Subtype))
        predecessors = [d.relation.entity2 for d in decl]

        for r in [self.query_cancel(e1=p, rel=rel) for p in predecessors]:
            r_filtered = [d for d in r if d.relation.name not in local_rels]
            local += r_filtered

        return local
    
    def query_down(self, e2=None, rel=None, first = True):
        local = [] if first else self.query_local(e1=e2, rel=rel, rel_type=Association)

        decl = self.query_local(e2=e2, rel_type=(Member, Subtype))
        descendents = [d.relation.entity1 for d in decl]
        
        for r in [self.query_down(e2=p, rel=rel) for p in descendents]:
            local += r
        
        return local

    def query_induce(self, e1=None, rel=None):
        inherited = self.query_down(entity, rel)

        return Counter([d.relation.entity2 for d in inherited]).most_common() #ns se está bem

    def query_local_assoc(self, entity=None, rel=rel):
        local = self.query_local(e1=entity, rel=rel, rel=None)

        for d in local:
            if isinstance(d.relation, Association):
                all_assoc = Counter([l.relation.entity2 for l in local]).most_common()

                all_assoc_freq = [(val, count/len(local)) for val, count in all_assoc]

                '''
                lim = 0
                res = []
                for val, freq in all_assoc_freq:
                    res.append((val, freq))
                    lim += freq
                    if lim >= 0.75:
                        return res
                '''
                
                def aux(transporte, elem):
                    res, lim = transporte
                    val, freq = elem
                    return res + [elem], lim+freq if lim < 0.75 else res
                
                return reduce(aux, all_assoc_freq, ([], 0))
                
            elif isinstance(d.relation, AssocOne):
                val, count = Counter([l.relation.entity2 for l in local]).most_common() #ns se está bem

                return (val, count/len(local))

            elif isinstance(d.relation, AssocNum):
                return mean([float(l.relation.entity2) for l in local])

            
        def query_assoc_value(self, E, A):
            local = self.query_local(e1=E, rel=A)

            val_count = Counter([d.relation.entity2 for d in local]).most_common()
            if(len(val_count) == 1):
                return val_count[0][0]
            
            decl = self.query(e1=E, rel = A)
            val_count = Counter([d.relation.entity2 for d in decl]).most_common()
            return val_count[0][0]