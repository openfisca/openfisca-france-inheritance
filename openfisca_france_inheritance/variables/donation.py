from openfisca_core.model_api import *

from openfisca_france_inheritance.entities import Individu, Donation

# class date(Variable):
#     value_type = int
#     entity = Donations
#     label = "Année de la donation"
#     definition_period = ETERNITY

# # class don_recu(Variable):
#     value_type = float
#     entity = Donations
#     label = "Don reçu"
#
# #    def function(self, actif_de_communaute, passif_de_communaute, actif_propre, passif_propre, assurance_vie):
# #        return (actif_de_communaute - passif_de_communaute) / 2 + actif_propre - passif_propre - assurance_vie
#     def formula(donation, period, parameters):
#
#         don = donation('don', period)
#         nombre_enfants_donataires = donation('nombre_enfants_donataires', period)
#         return don / nombre_enfants_donataires

# class nombre_enfants_donataires(Variable):
#     value_type = float
#     entity = Donations
#     label = "Nombre d'enfants donataires"
#
#     def formula(donation, period, parameters):
#
#         is_enfant_donataire_holder = donation('is_enfant_donataire', period)
#         return self.sum_by_entity(is_enfant_donataire_holder)


class actif_brut_donne(Variable):
    value_type = float
    entity = Donation
    label = "Montant de la part d'un actif brut donné à un unique donataire"
    definition_period = ETERNITY
    documentation = '''
    Ce qui est donné de l'actif propre du donateur
    et faisant l'objet d'une donation révélée à l'administration fiscale.

    Don représenté par sa valeur financière brute (avant application de toute éventuelle exonération).

    Le champ d'application des droits de mutation à titre gratuit est définie
    par les articles 750 ter à 757 C :    
    https://www.legifrance.gouv.fr/codes/section_lc/LEGITEXT000006069577/LEGISCTA000006191746/#LEGISCTA000006191746

    L'assiette des droits de mutation à titre gratuit est définie 
    par les articles 758 à 776 quater du Code général des impôts (CGI, 01/04/2025) : 
    https://www.legifrance.gouv.fr/codes/section_lc/LEGITEXT000006069577/LEGISCTA000006191747/
    '''


class actif_de_communaute_don(Variable):
    value_type = float
    entity = Donation
    label = 'Actif de Communauté'  # actif brut (à confirmer)
    definition_period = ETERNITY


class actif_imposable_don(Variable):
    value_type = float
    entity = Donation
    label = "Actif imposable transmis à donataire"
    definition_period = ETERNITY
    documentation = '''
    actif_imposable_don = actif imposable de l'individu donataire de la donation

    Hypothèse sur la structure de l'entité Donation : 
    1 seul rôle de donataire existe/est actif par Donation
    '''

    def formula(donation, period, parameters):
        # actif_imposable_don = don - exonération
        
        # part_epoux_don = donation('part_epoux_don', period)  # TODO devrait être l'actif imposable (don - exonération) de l'époux ?
        # actif_de_communaute_don = donation('actif_de_communaute_don', period)
        # passif_de_communaute_don = donation('passif_de_communaute_don', period)
        # actif_propre_don = donation('actif_propre_don', period)
        # passif_propre_don = donation('passif_propre_don', period)
        # assurance_vie_don = donation('assurance_vie_don', period)
        # return (
        #     (1 - part_epoux_don)
        #     * (
        #         (actif_de_communaute_don - passif_de_communaute_don) / 2
        #         + actif_propre_don
        #         - passif_propre_don
        #         - assurance_vie_don
        #         )
        #     )  
        # => équivalent montant du don ?!

        is_donataire = ~ donation.members('is_donateur', period)
        actif_imposable_donataire = is_donataire * donation.members("actif_imposable_donataire", period)
        actif_imposable_donation = donation.sum(actif_imposable_donataire)

        return actif_imposable_donation


class actif_propre_don(Variable):
    value_type = float
    entity = Donation  # ou individu puisque propre à 1 donateur ?
    label = "Actif propre d'un donateur"
    definition_period = ETERNITY
    documentation = '''
    Montant des biens qui appartiennent exclusivement à un donateur et qu'il peut trasmettre.
    Un actif propre peut être une part d'un actif commun.
    '''


class assurance_vie_don(Variable):
    value_type = float
    entity = Donation
    label = 'Assurance Vie'
    definition_period = ETERNITY


class epoux_donataire(Variable):
    value_type = bool
    entity = Donation
    label = "Présence d'un époux donataire"
    definition_period = ETERNITY

    def formula(donation, period, parameters):
        return donation.nb_persons(Donation.EPOUX_DONATAIRE)


class nombre_enfants_donataires(Variable):
    value_type = float
    entity = Donation
    label = "Nombre d'enfants donataires"
    definition_period = ETERNITY

    def formula(donation, period, parameters):
        return donation.sum(donation.members('is_enfant_donataire', period))


class nombre_freres_soeurs_donataires(Variable):
    value_type = float
    entity = Donation
    label = 'Nombre de frères et soeurs donataires'
    definition_period = ETERNITY

    def formula(donation, period, parameters):
        return donation.sum(donation.members('is_frere_soeur_donataire', period))


class existe_descendant_direct_donateur(Variable):
    value_type = bool
    entity = Donation
    label = "Le donateur a un descendant direct identifié"
    definition_period = ETERNITY

    def formula(donation, period, parameters):
       est_donateur = donation.members.has_role(Donation.DONATEUR) 

       # à améliorer : ici, pour toutes les donations, on consulte la descendance de tous les individus impliqués
       individus_connus_ont_descendants_directs = donation.members('existe_descendant_direct', period)

       donateur_a_descendant_direct = est_donateur * individus_connus_ont_descendants_directs
       return donation.sum(donateur_a_descendant_direct)


class part_epoux_don(Variable):
    value_type = float
    entity = Donation
    label = 'Part époux donataire'
    definition_period = ETERNITY


class part_taxable_don(Variable):
    value_type = float
    entity = Donation
    label = "Part taxable d'une donation à un donataire"
    definition_period = MONTH
    documentation = '''
    La part taxable du don transmis à un individu donataire
    selon le lien de parenté entre cet individu et le donateur.
    '''

    def formula(donation, period, parameters):
        actif_taxable_donataire = donation.members('actif_taxable_donataire', period)
        
        # TODO vérifier périmètre résidu ancienne formule : 
        # nombre_enfants_donataires = donation('nombre_enfants_donataires', period)
        # nombre_freres_soeurs_donataires = donation('nombre_freres_soeurs_donataires', period)
        # 
        # part_taxable_epoux_donataire = max_(actif_imposable_don - abattement_epoux_donataire, 0)
        # part_taxable_enfants_donataires = max_(actif_imposable_don / (nombre_enfants_donataires + 1 * (nombre_enfants_donataires == 0)) - abattement_enfants_donataires, 0)
        # part_taxable_freres_soeurs_donataires = max_(actif_imposable_don - abattement_freres_soeurs_donataires, 0)

        # Hypothèse sur la structure de l'entité Donation : 
        # 1 seul rôle de donataire existe/est actif par Donation
        return donation.sum(actif_taxable_donataire)


class passif_de_communaute_don(Variable):
    value_type = float
    entity = Donation
    label = 'Passif de communauté'
    definition_period = ETERNITY


class passif_propre_don(Variable):
    value_type = float
    entity = Donation
    label = 'Passif propre'
    definition_period = ETERNITY

