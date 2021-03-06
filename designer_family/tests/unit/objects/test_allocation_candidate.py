#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import mock

from designer_family import lib as placement_lib
from designer_family.objects import allocation_candidate as ac_obj
from designer_family.objects import research_context as res_ctx
from designer_family.tests.unit.objects import base


class TestAllocationCandidatesNoDB(base.TestCase):
    @mock.patch('designer_family.objects.research_context._has_provider_trees',
                new=mock.Mock(return_value=True))
    def test_limit_results(self):
        # Results are limited based on their root provider uuid, not uuid.
        # For a more "real" test of this functionality, one that exercises
        # nested providers, see the 'get allocation candidates nested limit'
        # test in the 'allocation-candidates.yaml' gabbit.
        aro_in = [
            mock.Mock(
                resource_requests=[
                    mock.Mock(resource_provider=mock.Mock(
                        root_provider_uuid=uuid))
                    for uuid in (1, 0, 4, 8)]),
            mock.Mock(
                resource_requests=[
                    mock.Mock(resource_provider=mock.Mock(
                        root_provider_uuid=uuid))
                    for uuid in (4, 8, 5)]),
            mock.Mock(
                resource_requests=[
                    mock.Mock(resource_provider=mock.Mock(
                        root_provider_uuid=uuid))
                    for uuid in (1, 7, 6, 4, 8, 5)]),
        ]
        sum1 = mock.Mock(resource_provider=mock.Mock(root_provider_uuid=1))
        sum0 = mock.Mock(resource_provider=mock.Mock(root_provider_uuid=0))
        sum4 = mock.Mock(resource_provider=mock.Mock(root_provider_uuid=4))
        sum8 = mock.Mock(resource_provider=mock.Mock(root_provider_uuid=8))
        sum5 = mock.Mock(resource_provider=mock.Mock(root_provider_uuid=5))
        sum7 = mock.Mock(resource_provider=mock.Mock(root_provider_uuid=7))
        sum6 = mock.Mock(resource_provider=mock.Mock(root_provider_uuid=6))
        sum_in = [sum1, sum0, sum4, sum8, sum5, sum7, sum6]
        rw_ctx = res_ctx.RequestWideSearchContext(
            self.context, placement_lib.RequestWideParams(limit=2), True)
        aro, sum = rw_ctx.limit_results(aro_in, sum_in)
        self.assertEqual(aro_in[:2], aro)
        self.assertEqual(set([sum1, sum0, sum4, sum8, sum5]), set(sum))

    def test_check_same_subtree(self):
        # Construct a tree that look like this
        #
        #  0 -+- 00 --- 000    1 -+- 10 --- 100
        #     |                   |
        #     +- 01 -+- 010       +- 11 -+- 110
        #     |      +- 011       |      +- 111
        #     +- 02 -+- 020       +- 12 -+- 120
        #            +- 021              +- 121
        #
        parent_by_rp = {"0": None, "00": "0", "000": "00",
                        "01": "0", "010": "01", "011": "01",
                        "02": "0", "020": "02", "021": "02",
                        "1": None, "10": "1", "100": "10",
                        "11": "1", "110": "11", "111": "11",
                        "12": "1", "120": "12", "121": "12"}
        same_subtree = [
            set(["0", "00", "01"]),
            set(["01", "010"]),
            set(["02", "020", "021"]),
            set(["02", "020", "021"]),
            set(["0", "02", "010"]),
            set(["000"])
        ]

        different_subtree = [
            set(["10", "11"]),
            set(["110", "111"]),
            set(["10", "11", "110"]),
            set(["12", "120", "100"]),
            set(["0", "1"]),
        ]

        for group in same_subtree:
            self.assertTrue(
                ac_obj._check_same_subtree(group, parent_by_rp))

        for group in different_subtree:
            self.assertFalse(
                ac_obj._check_same_subtree(group, parent_by_rp))
