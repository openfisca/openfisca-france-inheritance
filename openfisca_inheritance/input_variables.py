# -*- coding: utf-8 -*-


# OpenFisca -- A versatile microsimulation software
# By: OpenFisca Team <contact@openfisca.fr>
#
# Copyright (C) 2011, 2012, 2013, 2014, 2015 OpenFisca Team
# https://github.com/openfisca
#
# This file is part of OpenFisca.
#
# OpenFisca is free software; you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# OpenFisca is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


from datetime import date

from openfisca_core.columns import DateCol, EnumCol, FloatCol, IntCol, StrCol
from openfisca_core.enumerations import Enum
from openfisca_core.formulas import reference_input_variable

from .entities import Individus, Successions  # Donations


ROLE_REPRESENTANT = Enum([
    u'décédé',  # 0 cas spécial
    u'enfant',  # 1
    u'époux',  # 2
    u'parent',  # 3
    ])
DECEDE = ROLE_REPRESENTANT[u'décédé']
ENFANT = ROLE_REPRESENTANT[u'enfant']
EPOUX = ROLE_REPRESENTANT[u'époux']
PARENT = ROLE_REPRESENTANT[u'parent']

QUISUCC = Enum([
    'decede',
    'succedant',
    ])


#reference_input_variable(
#    column = FloatCol,
#    entity_class = Successions,
#    label = u"Actif de communauté",
#    name = u'actif_de_communaute',
#    )

#reference_input_variable(
#    column = FloatCol,
#    entity_class = Successions,
#    label = u"Passif de communauté",
#    name = u'passif_de_communaute',
#    )

reference_input_variable(
    column = FloatCol,
    entity_class = Successions,
    label = u"Actif de Communauté",
    name = u'actif_de_communaute',
    )

reference_input_variable(
    column = FloatCol,
    entity_class = Successions,
    label = u"Actif propre",
    name = u'actif_propre',
    )

reference_input_variable(
    column = FloatCol,
    entity_class = Successions,
    label = u"Assurance Vie",
    name = u'assurance_vie',
    )

reference_input_variable(
    column = DateCol(default = date(1, 1, 1)),
    entity_class = Individus,
    label = u"Date du décès",
    name = u'date_deces',
    )

# reference_input_variable(
#     column = IntCol,
#     entity_class = Donations,
#     label = u"Année de la donation",
#     name = u'date',
#     )

# reference_input_variable(
#     column = FloatCol,
#     entity_class = Donations,
#     label = u"Don",
#     name = u'don',
#     )

reference_input_variable(
    column = StrCol,
    entity_class = Individus,
    label = u"Identifiant de l'individu",
    name = u'id',
    )

reference_input_variable(
    column = StrCol,
    entity_class = Individus,
    label = u"Identifiant de l'individu représenté par cet individu",
    name = u'id_represente',
    )

reference_input_variable(
    column = IntCol,
    entity_class = Individus,
    label = u"Donation auquel appartient l'individu",
    name = u'iddon',
    )

reference_input_variable(
    column = IntCol,
    entity_class = Individus,
    label = u"Succession auquel appartient l'individu",
    name = u'idsucc',
    )

reference_input_variable(
    column = IntCol,
    entity_class = Individus,
    label = u"Index de l'individu représenté par cet individu",
    name = u'index_represente',
    )

reference_input_variable(
    column = FloatCol,
    entity_class = Successions,
    label = u"Part epoux",
    name = u'part_epoux',
    )

reference_input_variable(
    column = FloatCol,
    entity_class = Successions,
    label = u"Passif de Communauté",
    name = u'passif_de_communaute',
    )

reference_input_variable(
    column = FloatCol,
    entity_class = Successions,
    label = u"Passif propre",
    name = u'passif_propre',
    )

reference_input_variable(
    column = EnumCol(QUISUCC),
    entity_class = Individus,
    label = u"Role de l'individu dans la succession",
    name = u'quisucc',
    )

# reference_input_variable(
#     column = EnumCol(QUIDON),
#     entity_class = Individus,
#     label = u"Role de l'individu dans la donation",
#     name = u'quidon',
#     )

reference_input_variable(
    column = EnumCol(ROLE_REPRESENTANT),
    entity_class = Individus,
    label = u"Rôle de l'individu par rapport au représenté",
    name = u'role_representant',
    )


#reference_input_variable(
#    column = StrCol,
#    entity_class = Individus,
#    label = u"Identifiant de l'individu",
#    name = u'id',
#    )
