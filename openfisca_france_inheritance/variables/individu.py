from openfisca_core.model_api import *

from openfisca_france_inheritance.entities import Donation, Individu, Succession


AGE_INT_MINIMUM = -9999

class age(Variable):
    value_type = int
    default_value = AGE_INT_MINIMUM
    entity = Individu
    label = 'Âge au premier jour du mois'
    definition_period = MONTH
    is_period_size_independent = True
    set_input = set_input_dispatch_by_period

class date_deces(Variable):
    value_type = date
    entity = Individu
    label = 'Date du décès'
    definition_period = ETERNITY


class date_donation(Variable):
    value_type = date
    entity = Individu  # TODO Migrer vers l'entité Donation ?
    label = 'Date de la donation'
    definition_period = ETERNITY


class LienParente(Enum):
    __order__ = 'inconnu aucun quatrieme_degre neveu adelphite arriere_petit_enfant petit_enfant enfant ascendant pacs epoux'  # Needed to preserve the enum order in Python 2
    inconnu = 'Inconnu'  # valeur neutre en terme de droits de mutation
    aucun = 'Aucun lien de parenté'
    quatrieme_degre = 'Parent de 4ème degré'
    neveu = 'Neveu ou Nièce'
    adelphite = 'Frère ou soeur'
    arriere_petit_enfant = 'Arrière petit enfant'
    petit_enfant = 'Petit enfant'
    enfant = 'Enfant'
    ascendant = 'Mère, père, grand-mère, grand-père'
    pacs = "Partenaire Pacs"
    epoux = 'Epoux-se'


class role_representant(Variable):
    value_type = Enum
    possible_values = LienParente
    default_value = LienParente.inconnu
    entity = Individu
    label = "Lien de parenté de l'individu par rapport au représenté"
    definition_period = ETERNITY


# class degre_parente_civil(Variable):
#     value_type = int
#     entity = Individu
#     label = 'Degré de parenté, en droit civil, avec le décédé'
#     definition_period = ETERNITY

#     def formula(succession, period, parameters):
#         index_represente = succession('index_represente', period)
#         role_representant = succession('role_representant', period)

#         holder = self.holder
#         value_type = holder.column
#         degre_parente = empty(holder.entity.count, dtype = column.dtype)
#         degre_parente.fill(-9999)

#         # Initialise les décédes à 0.
#         degre_parente[role_representant == DECEDE] = 0

#         # Mets les époux des décédés à -1
#         degre_parente_represente = degre_parente[index_represente]
#         degre_parente[(role_representant == EPOUX) & (degre_parente_represente >= 0)] = -1

#         for i in itertools.count(0):
#             degre_parente_represente = degre_parente[index_represente]
#             degre_parente_precedent = degre_parente.copy()
#             masque = ((role_representant == ENFANT) | (role_representant == PARENT)) & (degre_parente_represente >= i)
#             degre_parente[masque] = degre_parente_represente[masque] + 1
#             if (degre_parente == degre_parente_precedent).all():
#                 break

#         return degre_parente


# # class degre_parente_fiscal(Variable):
#     value_type = int
#     entity = Individu
#     label = 'Degré de parenté, en droit fiscal, avec le décédé'
#     definition_period = ETERNITY
#
#     def formula(succession, period, parameters):
#
#         return degre_parente



class droits_mutation(Variable):
    value_type = float
    entity = Individu
    label = 'Droits de mutation à titre gratuit sur parts taxables de donations et successions'
    definition_period = ETERNITY

    def formula(individu, period, parameters):
        droits_donation = individu.donation('droits_donation', period)
        droits_succession = individu.donation('droits_succession', period)
        
        return droits_donation + droits_succession


class droits_donation(Variable):
    value_type = float
    default_value = 0.0
    entity = Individu
    label = 'Droits de mutation à titre gratuit sur parts taxables de donation'
    definition_period = YEAR
    reference = 'https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000030061736'

    # TODO EN COURS - migration de la formule d'openfisca-france vers openfisca-france-inheritance
    def formula_2015_01_01(individu, period, parameters):
        part_taxable_donations = individu.donation('part_taxable_don', period)  # ( don - exonération ) - abattement
        
        role_representant = individu('role_representant', period)
        parametres_tarifs_droits = parameters(period).droits_mutation_titre_gratuit.bareme
        droits_donations_par_bareme = select(
            [
                (role_representant == LienParente.epoux),
                (role_representant == LienParente.pacs),
                (role_representant == LienParente.enfant),
                (role_representant == LienParente.petit_enfant),
                (role_representant == LienParente.arriere_petit_enfant),
                (role_representant == LienParente.ascendant),
                (role_representant == LienParente.adelphite)
            ],
            [
                parametres_tarifs_droits.conjoint.calc(part_taxable_donations),
                parametres_tarifs_droits.pacs.calc(part_taxable_donations),  # TODO vérifier différence avec époux
                parametres_tarifs_droits.ligne_directe.calc(part_taxable_donations),  # enfant
                parametres_tarifs_droits.ligne_directe.calc(part_taxable_donations),  # petit_enfant
                parametres_tarifs_droits.ligne_directe.calc(part_taxable_donations),  # arriere_petit_enfant
                parametres_tarifs_droits.ligne_directe.calc(part_taxable_donations),  # ascendant
                parametres_tarifs_droits.autres.adelphite.calc(part_taxable_donations),
            ]
        )

        droits_donations_par_taux = select(
            [
                (role_representant == LienParente.neveu), 
                (role_representant == LienParente.quatrieme_degre),
                (role_representant == LienParente.aucun) 
            ],
            [
                parametres_tarifs_droits.autres.taux_parents_degre4 * part_taxable_donations,
                parametres_tarifs_droits.autres.taux_parents_degre4 * part_taxable_donations,
                parametres_tarifs_droits.autres.taux_non_parents * part_taxable_donations
            ]
        )
    
        # Seul rôle non couvert : LienParente.inconnu
        # dans ce cas, droit de mutation attendu à zéro (et impossibilité de la donation)

        return droits_donations_par_bareme + droits_donations_par_taux

        ### ancienne formule en cours de migration :
        
        # don = individu('don', period)
        # lien_parente = individu('lien_parente', period)
        # droit_exoneration_familial = individu(
        #     'droit_exoneration_familial', period)
        # param = parameters(period).taxation_capital.donation
        # # à migrer vers : param = parameters(period).droits_mutation_titre_gratuit.abattement ?
        # 
        # def calc_droits(abattement, taux, bareme):
        #     exoneration_familial = param.exoneration_don_familial * droit_exoneration_familial
        #     base_imposable = max_(don - exoneration_familial - abattement, 0)
        #     if bareme:
        #         return bareme.calc(base_imposable)
        #     return taux * base_imposable
        #
        # montant_droits_donation = select(
        #     [
        #         (lien_parente == LienParente.aucun),
        #         (lien_parente == LienParente.quatrieme_degre), 
        #         (lien_parente == LienParente.neveu), 
        #         (lien_parente == LienParente.fratrie), 
        #         (lien_parente == LienParente.ascendant), 
        #         (lien_parente == LienParente.arriere_petit_enfant), 
        #         (lien_parente == LienParente.petit_enfant),
        #         (lien_parente == LienParente.enfant), 
        #         (lien_parente == LienParente.epoux_pacs), 
        #         ],
        #     [
        #         calc_droits(0, param.taux_marginal_non_parents_donation, None),
        #         calc_droits(0, param.taux_marginal_parents_degre4_donation, None),
        #         calc_droits(param.abattement_neveuxnieces_donation, param.taux_neveu, None),
        #         calc_droits(param.abattement_freres_soeurs, 0, param.bareme_fratrie), 
        #         calc_droits(param.ascendant, 0,
        #                     param.bareme_ligne_directe), 
        #         calc_droits(param.abattement_arr_petits_enfants_donation,
        #                     0, param.bareme_ligne_directe), 
        #         calc_droits(param.abattement_petits_enfants_donation,
        #                     0, param.bareme_ligne_directe), 
        #         calc_droits(param.abattement_enfants_donation, 0,
        #                     param.bareme_ligne_directe), 
        #         calc_droits(param.abattement_epoux_donation,  # ou, de même : abattement_pacs_donation
        #                     0, param.bareme_epoux_pacs), 
        #         ]
        #     )
        # return montant_droits_donation


class droits_succession(Variable):
    value_type = float
    entity = Individu
    label = 'Droits sur parts taxables de succession'
    definition_period = ETERNITY

    def formula(individu, period, parameters):
        part_taxable = individu.succession('part_taxable', period)
        dmtg = parameters(period).droits_mutation_titre_gratuit
        bareme = dmtg.bareme.ligne_directe
        droits = bareme.calc(part_taxable)
        return droits


class id(Variable):
    value_type = str
    entity = Individu
    label = "Identifiant de l'individu"
    definition_period = ETERNITY


class id_represente(Variable):
    value_type = str
    entity = Individu
    label = "Identifiant de l'individu représenté par cet individu"
    definition_period = ETERNITY


class iddon(Variable):
    value_type = int
    entity = Individu
    label = "Donation auquel appartient l'individu"
    definition_period = ETERNITY


class idsucc(Variable):
    value_type = int
    entity = Individu
    label = "Succession auquel appartient l'individu"
    definition_period = ETERNITY


class index_represente(Variable):
    value_type = int
    entity = Individu
    label = "Index de l'individu représenté par cet individu"
    definition_period = ETERNITY


class is_donateur(Variable):
    value_type = bool
    entity = Individu
    label = 'Est donateur'
    definition_period = ETERNITY

    def formula(individu, period, parameters):
        return individu.has_role(Donation.DONATEUR)


class is_enfant(Variable):
    value_type = bool
    entity = Individu
    label = 'Est un enfant'
    definition_period = ETERNITY

    def formula(individu, period, parameters):
        return individu.has_role(Succession.ENFANT_SURVIVANT)


class is_enfant_donataire(Variable):
    value_type = float
    entity = Individu
    label = 'Est un enfant donataire'
    definition_period = ETERNITY

    def formula(individu, period, parameters):
        return individu.has_role(Donation.ENFANT_DONATAIRE)


class is_petit_enfant_donataire(Variable):
    value_type = float
    entity = Individu
    label = 'Est un petit-enfant donataire'
    definition_period = ETERNITY

    def formula(individu, period, parameters):
        return individu.has_role(Donation.PETIT_ENFANT_DONATAIRE)


class is_arriere_petit_enfant_donataire(Variable):
    value_type = float
    entity = Individu
    label = 'Est un arrière-petit-enfant donataire'
    definition_period = ETERNITY

    def formula(individu, period, parameters):
        return individu.has_role(Donation.ARRIERE_PETIT_ENFANT_DONATAIRE)


class is_frere_soeur(Variable):
    value_type = bool
    entity = Individu
    label = 'Est une soeur ou un frère'
    definition_period = ETERNITY

    def formula(individu, period, parameters):
        return individu.has_role(Succession.FRERE_SOEUR)


class is_frere_soeur_donataire(Variable):
    value_type = bool
    entity = Individu
    label = 'Est une soeur ou un frère donataire'
    definition_period = ETERNITY

    def formula(individu, period, parameters):
        return individu.has_role(Donation.FRERE_SOEUR_DONATAIRE)


class is_autre(Variable):
    value_type = bool
    entity = Individu
    label = 'Est une personnes en dehors du cercle familiale (un tiers)'
    definition_period = ETERNITY

    def formula(individu, period, parameters):
        return individu.has_role(Succession.AUTRE_SURVIVANT)

# class quidon(Variable):
#     value_type = Enum
#     possible_values = TypesQUIDON
#     default_value = TypesQUIDON.donateur
#     entity = Individu
#     label = 'Role de l'individu dans la donation'
#


class exoneration_don_familial(Variable):
    value_type = float
    default_value = 0.0
    entity = Individu
    label = "Montant de l'exonération pour don familial théorique à laquelle est éligible le donataire"
    definition_period = YEAR
    reference = "https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000048838931/2023-12-31/"
    documentation = '''
    Les conditions d'âge de l'exonération s'appliquent au jour de la transmission
    d'après l'article 790 G du CGI.
    '''

    def formula_2015_01_01(individu, period, parameters):
        parametres_exoneration_period = parameters(period).droits_mutation_titre_gratuit.exoneration

        # l'individu est le donataire et il a l'âge minimal requis
        # non modélisé : le donataire a fait l'objet d'une mesure d'émancipation au jour de la transmission
        age = individu('age', period)
        is_donateur = individu('is_donateur', period)
        age_donataire_eligible = ~is_donateur * ( age >= parametres_exoneration_period.age_minimal_donataire )
        

        # le donateur d'un don dont bénéficie l'individu à un âge en dessous du maximal fixé par l'exonération
        is_donateur_individus_donations = individu.donation.members('is_donateur', period)
        age_donateur_eligible = is_donateur_individus_donations * ( age < parametres_exoneration_period.age_maximal_donateur )

        condition_lien_parente = (
            individu('is_enfant_donataire', period)
            + individu('is_petit_enfant_donataire', period)
            + individu('is_arriere_petit_enfant_donataire', period)
            )

        eligibilite_exoneration = age_donateur_eligible * age_donataire_eligible * condition_lien_parente
        plafond_exoneration_don_familial = parametres_exoneration_period.exoneration_don_familial

        # exonération théorique (à confronter au montant du don dans le calcul du droit de mutation)
        return eligibilite_exoneration * plafond_exoneration_don_familial


class taux_sur_part_recue(Variable):
    value_type = float
    entity = Individu
    label = "Taux d'imposition sur la part recue"
    definition_period = ETERNITY

    def formula(indvidu, period, parameters):
        droits = indvidu('droits', period)
        part_recue = indvidu('part_recue', period)
        taux_sur_part_recue = droits / part_recue
        return taux_sur_part_recue