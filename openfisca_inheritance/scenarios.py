from datetime import date
import logging
import numpy as np

from openfisca_core import periods, simulations

from openfisca_inheritance.individu import ROLE_REPRESENTANT

log = logging.getLogger(__name__)
N_ = lambda message: message


def add_member(entity, **variables_value_by_name):
    entity.count += 1
    entity.step_size += 1
    member_index = entity.count - 1
    simulation = entity.simulation

    # Add a cell to all arrays of all variables of entity.
    for variable_name, variable_holder in entity.holder_by_name.iteritems():
        value_type = variable_holder.column
        if column.is_permanent:
            variable_holder._array = np.hstack((variable_holder._array, [column.default]))
        else:
            array_by_period = variable_holder._array_by_period
            if array_by_period is None:
                variable_holder._array_by_period = array_by_period = {}
            for period, array in array_by_period.iteritems():
                array_by_period[period] = np.hstack((array, [column.default]))

    # When entity is a person, ensure that the index & role of the person in the other entities are set.
    value_by_name = variables_value_by_name.copy()
    if entity.is_persons_entity:
        for other_entity in simulation.entity_by_key_singular.itervalues():
            if not other_entity.is_persons_entity:
                assert other_entity.count > 0
                value_by_name.setdefault(other_entity.index_for_person_variable_name, other_entity.count - 1)
                if other_entity.role_for_person_variable_name is not None:
                    role = value_by_name.get(other_entity.role_for_person_variable_name)
                    assert role is not None, "Missing role {} in person arguments: {}".format(
                        other_entity.role_for_person_variable_name, value_by_name)
                    if role >= other_entity.roles_count:
                        other_entity.roles_count = role + 1

    # Set arguments in variables.
    for variable_name, value in value_by_name.iteritems():
        variable_holder = entity.get_or_new_holder(variable_name)
        value_type = variable_holder.column
        if isinstance(value, dict):
            for period, period_value in value.iteritems():
                array = variable_holder.get_array(period)
                if array is None:
                    array = np.empty(entity.count, dtype = column.dtype)
                    array.fill(column.default)
                    variable_holder.set_array(period, array)
                array[member_index] = period_value
        else:
            period = simulation.period
            array = variable_holder.get_array(period)
            if array is None:
                array = np.empty(entity.count, dtype = column.dtype)
                array.fill(column.default)
                variable_holder.set_array(period, array)
            array[member_index] = value

    return member_index


def init_single_succession(debug = False, trace = False, individus = None, succession = None, tax_benefit_system = None,
        year = None):
    assert isinstance(individus, list)
    individus = [
        individu.copy()
        for individu in individus
        ]
    succession = {} if succession is None else succession.copy()
    if id is None:
        succession['id'] = 'succ0'

    decede_count = 0
    individus_id = set()
    individu_index_by_id = {}
    for individu_index, individu in enumerate(individus):
        individu_id = individu.get('id')
        assert isinstance(individu_id, basestring) and individu_id not in individus_id
        individus_id.add(individu_id)
        individu_index_by_id[individu_id] = individu_index
        role_representant = individu.get('role_representant')
        assert role_representant in ROLE_REPRESENTANT._nums, "Individu {} a un rôle invalide: {}".format(
            individu, role_representant).encode('utf-8')
        if role_representant == 'décédé':
            decede_count += 1
            assert individu.get('id_represente') is None, "Le décédé ne doit représenter personne"
            individu['id_represente'] = individu_id
            date_deces = individu.get('date_deces')
            assert isinstance(date_deces, date), "Le décédé doit avoir une date de décés"
            individu['quisucc'] = 0  # 'decede'
        else:
            individu['quisucc'] = 1  # 'succedant'
        # Convert role to an integer.
        individu['role_representant'] = ROLE_REPRESENTANT[individu['role_representant']]
    assert decede_count == 1, "La simulation doit avoir un et un seul décédé au lieu de {}".format(decede_count)

    for individu in individus:
        id_represente = individu.get('id_represente')
        assert id_represente in individus_id, "La personne représentée par l'individu {} n'existe pas".format(
            individu).encode('utf-8')
        individu['index_represente'] = individu_index_by_id[id_represente]

    period = periods.period('year', year)
    simulation = simulations.Simulation(period = period, tax_benefit_system = tax_benefit_system,
        debug = debug, trace = trace)

    sucession_entity = simulation.entity_by_key_singular['succession']
    add_member(sucession_entity, **succession)

    individu_entity = simulation.entity_by_key_singular['individu']
    for individu in individus:
        add_member(individu_entity, **individu)

    return simulation
