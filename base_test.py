#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from home_page import CaseConductorHomePage
from run_tests_page import CaseConductorRunTestsPage
from create_case_page import CaseConductorCreateCasePage
from manage_cases_page import CaseConductorManageCasesPage
from create_suite_page import CaseConductorCreateSuitePage
from manage_suites_page import CaseConductorManageSuitesPage
from create_run_page import CaseConductorCreateRunPage
from manage_runs_page import CaseConductorManageRunsPage
from create_cycle_page import CaseConductorCreateCyclePage
from manage_cycles_page import CaseConductorManageCyclesPage
from create_product_page import CaseConductorCreateProductPage
from manage_products_page import CaseConductorManageProductsPage


class BaseTest(object):
    '''
    Base class for all Tests
    '''

    def create_product(self, mozwebqa):
        create_product_pg = CaseConductorCreateProductPage(mozwebqa)

        create_product_pg.go_to_create_product_page()
        product = create_product_pg.create_product()

        return product

    def delete_product(self, mozwebqa, product):
        manage_products_pg = CaseConductorManageProductsPage(mozwebqa)

        manage_products_pg.go_to_manage_products_page()
        manage_products_pg.filter_products_by_name(name=product['name'])
        manage_products_pg.delete_product(name=product['name'])

    def create_cycle(self, mozwebqa, activate=False, product=None):
        create_cycle_pg = CaseConductorCreateCyclePage(mozwebqa)

        if product is None:
            product = self.create_product(mozwebqa)

        create_cycle_pg.go_to_create_cycle_page()
        cycle = create_cycle_pg.create_cycle(product=product['name'])
        cycle['product'] = product

        if activate:
            manage_cycles_pg = CaseConductorManageCyclesPage(mozwebqa)
            manage_cycles_pg.filter_cycles_by_name(name=cycle['name'])
            manage_cycles_pg.activate_cycle(name=cycle['name'])

        return cycle

    def delete_cycle(self, mozwebqa, cycle, delete_product=False):
        manage_cycles_pg = CaseConductorManageCyclesPage(mozwebqa)

        manage_cycles_pg.go_to_manage_cycles_page()
        manage_cycles_pg.filter_cycles_by_name(name=cycle['name'])
        manage_cycles_pg.delete_cycle(name=cycle['name'])

        if delete_product:
            self.delete_product(mozwebqa, cycle['product'])

    def create_run(self, mozwebqa, activate=False, cycle=None, suite_name=None):
        create_run_pg = CaseConductorCreateRunPage(mozwebqa)

        if cycle is None:
            cycle = self.create_cycle(mozwebqa, activate=activate)

        create_run_pg.go_to_create_run_page()
        run = create_run_pg.create_run(cycle=cycle['name'], suite=suite_name)
        run['cycle'] = cycle

        if activate:
            manage_runs_pg = CaseConductorManageRunsPage(mozwebqa)
            manage_runs_pg.filter_runs_by_name(name=run['name'])
            manage_runs_pg.activate_run(name=run['name'])

        return run

    def delete_run(self, mozwebqa, run, delete_cycle=False, delete_product=False):
        manage_runs_pg = CaseConductorManageRunsPage(mozwebqa)

        manage_runs_pg.go_to_manage_runs_page()
        manage_runs_pg.filter_runs_by_name(name=run['name'])
        manage_runs_pg.delete_run(name=run['name'])

        if delete_cycle:
            self.delete_cycle(mozwebqa, run['cycle'], delete_product=delete_product)

    def create_suite(self, mozwebqa, activate=False, product=None):
        create_suite_pg = CaseConductorCreateSuitePage(mozwebqa)

        if product is None:
            product = self.create_product(mozwebqa)

        create_suite_pg.go_to_create_suite_page()
        suite = create_suite_pg.create_suite(product=product['name'])
        suite['product'] = product

        if activate:
            manage_suites_pg = CaseConductorManageSuitesPage(mozwebqa)
            manage_suites_pg.filter_suites_by_name(name=suite['name'])
            manage_suites_pg.activate_suite(name=suite['name'])

        return suite

    def delete_suite(self, mozwebqa, suite, delete_product=False):
        manage_suites_pg = CaseConductorManageSuitesPage(mozwebqa)

        manage_suites_pg.go_to_manage_suites_page()
        manage_suites_pg.filter_suites_by_name(name=suite['name'])
        manage_suites_pg.delete_suite(name=suite['name'])

        if delete_product:
            self.delete_product(mozwebqa, suite['product'])

    def create_case(self, mozwebqa, activate=False, product=None, suite_name=None):
        create_case_pg = CaseConductorCreateCasePage(mozwebqa)

        if product is None:
            product = self.create_product(mozwebqa)

        create_case_pg.go_to_create_case_page()
        case = create_case_pg.create_case(product=product['name'], suite=suite_name)
        case['product'] = product

        if activate:
            manage_cases_pg = CaseConductorManageCasesPage(mozwebqa)
            manage_cases_pg.filter_cases_by_name(name=case['name'])
            manage_cases_pg.activate_case(name=case['name'])

        return case

    def delete_case(self, mozwebqa, case, delete_product=False):
        manage_cases_pg = CaseConductorManageCasesPage(mozwebqa)

        manage_cases_pg.go_to_manage_cases_page()
        manage_cases_pg.filter_cases_by_name(name=case['name'])
        manage_cases_pg.delete_case(name=case['name'])

        if delete_product:
            self.delete_product(mozwebqa, case['product'])

    def create_and_run_test(self, mozwebqa):
        home_pg = CaseConductorHomePage(mozwebqa)
        manage_suites_pg = CaseConductorManageSuitesPage(mozwebqa)
        run_tests_pg = CaseConductorRunTestsPage(mozwebqa)

        suite = self.create_suite(mozwebqa)
        case = self.create_case(mozwebqa, activate=True, product=suite['product'], suite_name=suite['name'])

        manage_suites_pg.go_to_manage_suites_page()
        manage_suites_pg.filter_suites_by_name(name=suite['name'])
        manage_suites_pg.activate_suite(name=suite['name'])

        cycle = self.create_cycle(mozwebqa, activate=True, product=suite['product'])
        run = self.create_run(mozwebqa, activate=True, cycle=cycle, suite_name=suite['name'])

        home_pg.go_to_homepage_page()
        home_pg.go_to_run_test(product_name=run['cycle']['product']['name'], cycle_name=run['cycle']['name'], run_name=run['name'])

        return case
