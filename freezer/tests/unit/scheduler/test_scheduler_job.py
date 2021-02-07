# (c) Copyright 2014,2015 Hewlett-Packard Development Company, L.P.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import tempfile
import unittest

from freezer.scheduler import scheduler_job
from unittest import mock

action = {"action": "backup", "storage": "local",
          "mode": "fs", "backup_name": "test",
          "container": "/tmp/backuped",
          "path_to_backup": "/tmp/to_backup"}


class TestSchedulerJob(unittest.TestCase):
    def setUp(self):
        self.job = scheduler_job.Job(None, None, {"job_schedule": {}})

    def test(self):
        scheduler_job.RunningState.stop(self.job, {})

    def test_save_action_to_disk(self):
        with tempfile.NamedTemporaryFile(mode='w',
                                         delete=False) as config_file:
            self.job.save_action_to_file(action, config_file)
            self.assertTrue(os.path.exists(config_file.name))

    def test_save_action_with_none_value_to_disk(self):
        action.update({"log_file": None})
        with tempfile.NamedTemporaryFile(mode='w',
                                         delete=False) as config_file:
            self.job.save_action_to_file(action, config_file)
            self.assertTrue(os.path.exists(config_file.name))

    def test_save_action_with_bool_value_to_disk(self):
        action.update({"no_incremental": False})
        with tempfile.NamedTemporaryFile(mode='w',
                                         delete=False) as config_file:
            self.job.save_action_to_file(action, config_file)
            self.assertTrue(os.path.exists(config_file.name))


class TestSchedulerJob1(unittest.TestCase):
    def setUp(self):
        self.scheduler = mock.MagicMock()
        self.job_schedule = {"event": "start", "status": "start",
                             "schedule_day": "1"}
        self.jobdoc = {"job_id": "test", "job_schedule": self.job_schedule}
        self.job = scheduler_job.Job(self.scheduler, None, self.jobdoc)

    def test_stopstate_stop(self):
        result = scheduler_job.StopState.stop(self.job, self.jobdoc)
        self.assertEqual(result, '')

    def test_stopstate_abort(self):
        result = scheduler_job.StopState.abort(self.job, self.jobdoc)
        self.assertEqual(result, '')

    def test_stopstate_start(self):
        result = scheduler_job.StopState.start(self.job, self.jobdoc)
        self.assertEqual(result, '')

    def test_stopstate_remove(self):
        result = scheduler_job.StopState.remove(self.job)
        self.assertEqual(result, '')

    def test_scheduledstate_stop(self):
        result = scheduler_job.ScheduledState.stop(self.job, self.jobdoc)
        self.assertEqual(result, 'stop')

    def test_scheduledstate_abort(self):
        result = scheduler_job.ScheduledState.abort(self.job, self.jobdoc)
        self.assertEqual(result, '')

    def test_scheduledstate_start(self):
        result = scheduler_job.ScheduledState.start(self.job, self.jobdoc)
        self.assertEqual(result, '')

    def test_scheduledstate_remove(self):
        result = scheduler_job.ScheduledState.remove(self.job)
        self.assertEqual(result, '')

    def test_runningstate_stop(self):
        result = scheduler_job.RunningState.stop(self.job, {})
        self.assertEqual(result, '')

    def test_runningstate_abort(self):
        result = scheduler_job.RunningState.abort(self.job, self.jobdoc)
        self.assertEqual(result, 'aborted')

    def test_runningstate_start(self):
        result = scheduler_job.RunningState.start(self.job, self.jobdoc)
        self.assertEqual(result, '')

    def test_runningstate_remove(self):
        result = scheduler_job.RunningState.remove(self.job)
        self.assertEqual(result, '')
